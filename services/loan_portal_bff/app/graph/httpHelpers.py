import httpx

TIMEOUT = httpx.Timeout(3.0)

async def post_json(base_url: str, path: str, payload: dict, headers: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(f"{base_url}{path}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

async def get_json(base_url: str, path: str, headers: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(f"{base_url}{path}", headers=headers)
        response.raise_for_status()
        return response.json()