import os
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Header, Body, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from google import genai
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Translate and Exchange Service")

# Security Configuration
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-flash-latest"

# Currency API Configuration
CURRENCY_API_PRIMARY = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"
CURRENCY_API_FALLBACK = "https://latest.currency-api.pages.dev/v1/currencies"

@app.post("/translate", dependencies=[Depends(verify_api_key)])
async def translate(request_data: Dict[str, str] = Body(...)):
    try:
        target_language = request_data.get("target_language")
        if not target_language:
            raise HTTPException(status_code=400, detail="target_language is required")
        
        # Filter out target_language from data to translate
        data_to_translate = {k: v for k, v in request_data.items() if k != "target_language"}
        
        # Prepare the prompt for Gemini
        prompt = (
            f"Translate the following key-value pairs into {target_language}. "
            "Return ONLY a JSON object with the same keys and the translated values. "
            "Do not include any other text or formatting.\n\n"
            f"{json.dumps(data_to_translate, ensure_ascii=False)}"
        )
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        # Clean up the response text
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        translated_data = json.loads(content)
        return translated_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/exchange", dependencies=[Depends(verify_api_key)])
async def exchange(
    from_currency: str,
    to_currency: str,
    amount: float
):
    from_curr = from_currency.lower()
    to_curr = to_currency.lower()
    
    async def fetch_rate(base_url: str):
        url = f"{base_url}/{from_curr}.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                # The structure is { "date": "...", "eur": { "usd": ... } }
                rates = data.get(from_curr)
                if rates and to_curr in rates:
                    return rates[to_curr]
            return None

    try:
        # Try primary URL
        conversion_rate = await fetch_rate(CURRENCY_API_PRIMARY)
        
        # Try fallback if primary fails
        if conversion_rate is None:
            conversion_rate = await fetch_rate(CURRENCY_API_FALLBACK)
            
        if conversion_rate is None:
            raise HTTPException(status_code=404, detail=f"Could not find exchange rate for {from_currency} to {to_currency}")
            
        converted_amount = amount * conversion_rate
        
        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "rate": conversion_rate,
            "converted_amount": converted_amount
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exchange failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
