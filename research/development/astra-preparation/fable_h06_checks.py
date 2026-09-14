"""Check specific Fable objections against pinned public HTTPX; no model calls."""
import argparse
import asyncio
import gc
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    manifest_path = Path(__file__).parent.parent / "h06-guidance-assessment/source-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest["files"].items():
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == expected, name
    sys.path.insert(0, str(source))
    import httpx
    assert Path(httpx.__file__).resolve().is_relative_to(source)

    class SyncBody(httpx.SyncByteStream):
        def __iter__(self):
            yield b"body"

    class AsyncBody(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b"body"

    class FollowUp(httpx.Auth):
        requires_request_body = True

        def auth_flow(self, request):
            assert request.content == b"body", "Initial body was not loaded"
            yield request
            later = httpx.Request("POST", "https://example.invalid/", content=iter([b"later"]))
            later.content
            yield later

    class ReadContent(httpx.Auth):
        def auth_flow(self, request):
            assert request.content == b"body"
            yield request

    class DocRejection(httpx.Auth):
        async def async_auth_flow(self, request):
            raise RuntimeError("Cannot use a sync authentication class with httpx.AsyncClient")

    class GeneratorRejection(httpx.Auth):
        async def async_auth_flow(self, request):
            raise RuntimeError("Cannot use a sync authentication class with httpx.AsyncClient")
            yield request

    async def body_case(mode, later=False, preloaded=False):
        request = httpx.Request("POST", "https://example.invalid/",
                                stream=SyncBody() if mode == "sync" else AsyncBody())
        if preloaded:
            if mode == "sync":
                request.read()
            else:
                await request.aread()
        auth = FollowUp() if later else ReadContent()
        flow = auth.sync_auth_flow(request) if mode == "sync" else auth.async_auth_flow(request)
        try:
            next(flow) if mode == "sync" else await anext(flow)
            if later:
                response = httpx.Response(200, content=b"ok")
                flow.send(response) if mode == "sync" else await flow.asend(response)
            return "body available"
        finally:
            if mode == "sync":
                flow.close()
            else:
                await flow.aclose()

    async def streamed_response(mode, flag):
        auth = httpx.Auth()
        auth.requires_response_body = flag
        def respond(request):
            return httpx.Response(200, stream=SyncBody() if mode == "sync" else AsyncBody())
        transport = httpx.MockTransport(respond)
        if mode == "sync":
            with httpx.Client(transport=transport, auth=auth, trust_env=False) as client:
                with client.stream("GET", "https://example.invalid/") as response:
                    return {"consumed": response.is_stream_consumed, "closed": response.is_closed}
        async with httpx.AsyncClient(transport=transport, auth=auth, trust_env=False) as client:
            async with client.stream("GET", "https://example.invalid/") as response:
                return {"consumed": response.is_stream_consumed, "closed": response.is_closed}

    async def rejection(auth):
        async with httpx.AsyncClient(auth=auth, trust_env=False,
                                     transport=httpx.MockTransport(lambda r: httpx.Response(200))) as client:
            await client.get("https://example.invalid/")
        return "unexpected success"

    async def run():
        rows = []
        async def check(name, operation, expected):
            details = {}
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                try:
                    actual = await operation
                except Exception as exc:
                    actual = type(exc).__name__
                    details = {"message": str(exc), "context": str(exc.__context__) if exc.__context__ else None}
                gc.collect()
                warning_text = [str(w.message) for w in caught]
            rows.append({"check": name, "expected": expected, "observed": actual,
                         "details": details, "warnings": warning_text, "passed": actual == expected})

        for mode in ("sync", "async"):
            await check(f"{mode}: flag loads initial body but not new request in flow",
                        body_case(mode, later=True), "RequestNotRead")
            await check(f"{mode}: previously streamed body loaded explicitly needs no flag",
                        body_case(mode, preloaded=True), "body available")
            await check(f"{mode}: unread body without flag still fails",
                        body_case(mode), "RequestNotRead")
            for flag in (False, True):
                await check(f"{mode}: stream response with body flag {flag}",
                            streamed_response(mode, flag), {"consumed": flag, "closed": flag})
        await check("async: documented rejection without yield", rejection(DocRejection()), "AttributeError")
        await check("async: rejection preserving generator contract", rejection(GeneratorRejection()), "RuntimeError")
        return rows

    rows = asyncio.run(run())
    result = {"status": "Investigator checks of Fable objections, not model qualification",
              "source_commit": manifest["source_commit"],
              "source_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": platform.python_version(),
              "dependencies": {n: importlib.metadata.version(n) for n in ("httpcore", "anyio", "certifi", "idna")},
              "network": "Local adapters and mock transport only; no outbound requests",
              "checks": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(result, indent=2) + "\n")
    print(f"{sum(row['passed'] for row in rows)}/{len(rows)} checks passed")
    if not all(row["passed"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
