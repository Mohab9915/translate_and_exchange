# AI Content Generation API Spec

## Endpoint

```
POST /v1/completions
Authorization: Bearer {API_TOKEN}
Content-Type: application/json
```

## Request Payload

```json
{
  "product_name": "iPhone 15 Pro Max",
  "small_details": "256GB storage, titanium frame, A17 Pro chip",
  "product_category": "electronics",
  "max_tokens": 512,
  "temperature": 0.7,
  "stream": false,
  "output_format": "paragraph",
  "max_chars": 500
}
```

| Field              | Type    | Required | Description                                |
|--------------------|---------|----------|--------------------------------------------|
| `product_name`     | string  | Yes      | Product name / main prompt                 |
| `small_details`    | string  | No       | Additional details about the product       |
| `product_category` | string  | Yes      | Category key from the list below           |
| `max_tokens`       | integer | No       | Max tokens to generate (default: 512)      |
| `temperature`      | float   | No       | Creativity level 0.0-1.0 (default: 0.7)   |
| `stream`           | boolean | No       | Stream response (default: false)           |
| `output_format`    | string  | No       | Output format (default: "paragraph")       |
| `max_chars`        | integer | No       | Max characters in response (optional)      |

## Expected Response

```json
{
  "text": "Generated product description content here..."
}
```

Response field priority: `text` > `content` > `choices[0].message.content`

## Readiness Check

```
GET /ready
Authorization: Bearer {API_TOKEN}
```

Returns `200 OK` when the model is ready to accept requests.

## Categories

| Key                    | English              | Arabic (عربي)         |
|------------------------|----------------------|-----------------------|
| `general`              | General              | عام                   |
| `clothing`             | Clothing             | ملابس                 |
| `fashion`              | Fashion              | أزياء                 |
| `clothing_fashion`     | Clothing & Fashion   | ملابس_وأزياء          |
| `clothing_accessories` | Clothing & Accessories | ملابس_و_اكسسوارات   |
| `dress`                | Dress                | فستان                 |
| `skin_care`            | Skin Care            | بشرة                  |
| `makeup`               | Makeup               | مكياج                 |
| `beauty`               | Beauty               | تجميل                 |
| `food`                 | Food                 | طعام                  |
| `beverages`            | Beverages            | مشروبات               |
| `food_items`           | Food Items           | مأكولات               |
| `electronics`          | Electronics          | إلكترونيات            |
| `technology`           | Technology           | تقنيات                |
| `devices`              | Devices              | أجهزة                 |
| `furniture`            | Furniture            | أثاث                  |
| `decor`                | Decor                | ديكور                 |
| `home`                 | Home                 | منزلي                 |
| `kitchen`              | Kitchen              | مطبخ                  |
| `sports`               | Sports               | رياضة                 |
| `jewelry`              | Jewelry              | مجوهرات               |
| `books`                | Books                | كتب                   |
| `pets`                 | Pets                 | حيوانات               |
| `handmade`             | Handmade             | يدوي                  |
| `kids`                 | Kids                 | اطفال                 |
