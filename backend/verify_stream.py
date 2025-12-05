import httpx
import asyncio
import json
import time

async def test_stream():
    url = "http://localhost:8000/api/depth"
    payload = {
        "track": "FinTech",
        "problem_statement": "Simplify taxes",
        "threshold": 7,
        "max_iterations": 2
    }
    
    print(f"Connecting to {url}...")
    start_time = time.time()
    
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=payload, timeout=60.0) as response:
            print(f"Response status: {response.status_code}")
            async for chunk in response.aiter_lines():
                if chunk:
                    elapsed = time.time() - start_time
                    print(f"[{elapsed:.2f}s] Received: {chunk[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_stream())
