# Fetch a small preview

Implement `async def preview(client, url, consume)` in `preview.py` for an application that borrows a long-lived HTTPX AsyncClient. Issue a GET request, reject an unsuccessful HTTP status using `raise_for_status()`, and obtain only the first available decoded byte chunk. Await `consume(chunk)` once and return that chunk. For an empty body, call the consumer with `b""` and return it. Do not read the remainder of a nonempty response. Preserve HTTP, stream and consumer errors.

Release any response acquired by the function before it returns or raises. Leave the borrowed client open. Either context-managed or manual streaming is acceptable if it meets these requirements. Cancellation during cleanup and failing cleanup operations are outside this development task. No network service is needed for local checks.
