"""Public investigator-authored development candidates, never blinded outputs."""


async def context_managed(client, url, consume):
    async with client.stream("GET", url) as response:
        response.raise_for_status()
        chunk = await anext(response.aiter_bytes(), b"")
        await consume(chunk)
        return chunk


async def manual_finally(client, url, consume):
    request = client.build_request("GET", url)
    response = await client.send(request, stream=True)
    try:
        response.raise_for_status()
        chunk = await anext(response.aiter_bytes(), b"")
        await consume(chunk)
        return chunk
    finally:
        await response.aclose()


async def missing_close(client, url, consume):
    request = client.build_request("GET", url)
    response = await client.send(request, stream=True)
    response.raise_for_status()
    chunk = await anext(response.aiter_bytes(), b"")
    await consume(chunk)
    return chunk


async def normal_only_close(client, url, consume):
    request = client.build_request("GET", url)
    response = await client.send(request, stream=True)
    response.raise_for_status()
    chunk = await anext(response.aiter_bytes(), b"")
    await consume(chunk)
    await response.aclose()
    return chunk


async def incomplete(client, url, consume):
    raise NotImplementedError
