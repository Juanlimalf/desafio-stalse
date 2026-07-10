from collections.abc import Generator

import httpx


def get_http_client() -> Generator[httpx.Client]:
    client = httpx.Client()

    yield client

    client.close()
