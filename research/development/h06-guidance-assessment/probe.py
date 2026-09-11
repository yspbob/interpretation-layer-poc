"""Investigator development checks of pinned HTTPX, not model assessment."""
import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    manifest = json.loads(Path(__file__).with_name("source-manifest.json").read_text())
    for name, expected in manifest["files"].items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Pinned source mismatch: {name}")
    sys.path.insert(0, str(source))
    import httpx
    if not Path(httpx.__file__).resolve().is_relative_to(source):
        raise SystemExit("Did not import the pinned source")

    class SyncBody(httpx.SyncByteStream):
        def __iter__(self):
            yield b"first"
            yield b"second"

    class AsyncBody(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b"first"
            yield b"second"

    class RequestBodyAuth(httpx.Auth):
        def auth_flow(self, request):
            request.headers["X-Probe"] = request.content.decode()
            yield request

    class ResponseBodyAuth(httpx.Auth):
        def auth_flow(self, request):
            response = yield request
            request.headers["X-Probe"] = response.content.decode()
            yield request

    class OverrideBodyAuth(httpx.Auth):
        requires_request_body = True

        def sync_auth_flow(self, request):
            request.headers["X-Probe"] = request.content.decode()
            yield request

        async def async_auth_flow(self, request):
            request.headers["X-Probe"] = request.content.decode()
            yield request

    class SharedAuth(httpx.Auth):
        def auth_flow(self, request):
            request.headers["X-Probe"] = "shared"
            yield request

    class SpecialAuth(httpx.Auth):
        def auth_flow(self, request):
            raise AssertionError("Specialised dispatch must not use this fallback")
            yield request

        def sync_auth_flow(self, request):
            request.headers["X-Probe"] = "sync"
            yield request

        async def async_auth_flow(self, request):
            request.headers["X-Probe"] = "async"
            yield request

    class SyncOnlyAuth(SpecialAuth):
        async def async_auth_flow(self, request):
            raise RuntimeError("This development example supports sync clients only")
            yield request

    def echo(request):
        return httpx.Response(200, text=request.headers["X-Probe"])

    async def public_dispatch(mode, auth):
        transport = httpx.MockTransport(echo)
        if mode == "sync":
            with httpx.Client(transport=transport, auth=auth, trust_env=False) as client:
                return client.get("https://example.invalid/").text
        async with httpx.AsyncClient(transport=transport, auth=auth, trust_env=False) as client:
            return (await client.get("https://example.invalid/")).text

    async def body_probe(mode, kind, declared):
        body_type = SyncBody if mode == "sync" else AsyncBody
        auth = {"request": RequestBodyAuth, "response": ResponseBodyAuth,
                "override": OverrideBodyAuth}[kind]()
        if kind == "request":
            auth.requires_request_body = declared
        if kind == "response":
            auth.requires_response_body = declared
        request = httpx.Request("POST", "https://example.invalid/", stream=body_type())
        response = httpx.Response(200, stream=body_type())
        flow = auth.sync_auth_flow(request) if mode == "sync" else auth.async_auth_flow(request)
        try:
            outgoing = next(flow) if mode == "sync" else await anext(flow)
            if kind == "response":
                outgoing = flow.send(response) if mode == "sync" else await flow.asend(response)
            return outgoing.headers["X-Probe"]
        finally:
            if mode == "sync":
                flow.close()
                response.close()
            else:
                await flow.aclose()
                await response.aclose()

    async def run():
        rows = []
        async def check(name, operation, expected):
            try:
                actual = await operation
            except (httpx.RequestNotRead, httpx.ResponseNotRead, RuntimeError) as exc:
                actual = type(exc).__name__
            rows.append({"check": name, "expected": expected, "observed": actual,
                         "passed": actual == expected})

        for mode in ("sync", "async"):
            await check(f"{mode}: shared flow through client", public_dispatch(mode, SharedAuth()), "shared")
            await check(f"{mode}: specialised flow through client", public_dispatch(mode, SpecialAuth()), mode)
            for kind in ("request", "response"):
                await check(f"{mode}: {kind} body declared", body_probe(mode, kind, True), "firstsecond")
                await check(f"{mode}: {kind} body undeclared", body_probe(mode, kind, False),
                            "RequestNotRead" if kind == "request" else "ResponseNotRead")
            await check(f"{mode}: override bypasses base body read", body_probe(mode, "override", True), "RequestNotRead")
        await check("async: explicit unsupported mode", public_dispatch("async", SyncOnlyAuth()), "RuntimeError")
        return rows

    rows = asyncio.run(run())
    result = {
        "status": "Investigator development probes; no model calls, semantic grading or isolation validation",
        "source_commit": manifest["source_commit"],
        "source_manifest_sha256": hashlib.sha256(Path(__file__).with_name("source-manifest.json").read_bytes()).hexdigest(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "httpx_version_from_pinned_source": httpx.__version__,
        "dependencies": {name: importlib.metadata.version(name) for name in ("httpcore", "anyio", "certifi", "idna")},
        "network": "MockTransport and local flow generators only; no outbound requests or provider calls",
        "limits": "Body checks exercise base adapters directly; dispatch checks use real Client and AsyncClient with a mock transport. No event loop blocking, real authentication service, concurrency, cryptographic security or full upstream suite was tested.",
        "checks": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{sum(row['passed'] for row in rows)}/{len(rows)} development checks matched their declared expectations")
    if not all(row["passed"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
