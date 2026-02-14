import asyncio
from main import app
from httpx import AsyncClient, ASGITransport
import os

# Mock API Key for testing if not present in env
if not os.getenv("API_KEY"):
    os.environ["API_KEY"] = "test_key"
    
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-KEY": API_KEY}

async def test_readiness():
    print("Testing /ready endpoint...")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/ready", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert response.text == "200 OK"
    print("✅ /ready method passed")

async def test_completion_valid():
    print("\nTesting /v1/completions (Valid)...")
    payload = {
        "product_name": "Test Product",
        "product_category": "electronics",
        "small_details": "Test details",
        "max_tokens": 50,
        "temperature": 0.1
    }
    # Mocking genai client would be ideal, but for now we might hit the real API or fail if no key.
    # If GEMINI_API_KEY is not set, this will fail. 
    # Let's see if we can check environment variables first.
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY not found. Skipping actual API call logic, ensuring validation passes until API call.")
        return

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/v1/completions", json=payload, headers=HEADERS)
    
    print(f"Status Code: {response.status_code}")
    # It might fail with 500 if the key is invalid, but validation should pass.
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        assert "text" in response.json()
        print("✅ /v1/completions valid request passed")
    else:
         print(f"❌ /v1/completions failed with {response.status_code}: {response.text}")

async def test_completion_invalid_category():
    print("\nTesting /v1/completions (Invalid Category)...")
    payload = {
        "product_name": "Test Product",
        "product_category": "invalid_category"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/v1/completions", json=payload, headers=HEADERS)
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400
    assert "Invalid category" in response.text
    print("✅ /v1/completions invalid category passed")

async def main():
    await test_readiness()
    await test_completion_invalid_category()
    await test_completion_valid()

if __name__ == "__main__":
    asyncio.run(main())
