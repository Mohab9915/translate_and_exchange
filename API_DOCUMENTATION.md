# API Documentation - Translate and Exchange Service

This service provides AI-powered translation and real-time currency exchange.

## Security
All requests must include the following header:
- **Header Name**: `X-API-KEY`
- **Static Key**: `eWSttTwmsJjna00R0TGMjy7NCqP7QOWgpDy86yooMhs`

---

## Endpoints

### 1. AI Translation
Translates key-value pairs into a target language.

- **URL**: `/translate`
- **Method**: `POST`
- **Body**: Flat JSON object containing the keys to translate and a `target_language` field.
- **Example Request**:
  ```bash
  curl -X POST https://translateandexchange-production.up.railway.app/translate \
    -H "X-API-KEY: eWSttTwmsJjna00R0TGMjy7NCqP7QOWgpDy86yooMhs" \
    -H "Content-Type: application/json" \
    -d '{"title": "Good product", "target_language": "arabic"}'
  ```
- **Example Response**:
  ```json
  {"title": "منتج جيد"}
  ```

### 2. Currency Exchange
Converts an amount from one currency to another using real-time rates.

- **URL**: `/exchange`
- **Method**: `GET`
- **Parameters**:
  - `from_currency` (e.g., USD)
  - `to_currency` (e.g., ILS)
  - `amount` (e.g., 1000)
- **Example Request**:
  ```bash
  curl "https://translateandexchange-production.up.railway.app/exchange?from_currency=USD&to_currency=ILS&amount=1000" \
    -H "X-API-KEY: eWSttTwmsJjna00R0TGMjy7NCqP7QOWgpDy86yooMhs"
  ```
- **Example Response**:
  ```json
  {
    "from": "USD",
    "to": "ILS",
    "amount": 1000.0,
    "rate": 3.1461,
    "converted_amount": 3146.1
  }
  ```

---