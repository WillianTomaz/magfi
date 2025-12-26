# MAGFI API Endpoints Reference

## Base URLs

- **magfi-core**: http://localhost:8100
- **magfi-ingestor**: http://localhost:8200
- **magfi-predictor**: http://localhost:8300

---

## MAGFI-CORE Endpoints

### Health

```
GET /health
```

Returns service health status.

**Response:**

```json
{
  "status": "healthy",
  "app_name": "magfi-core",
  "environment": "development",
  "version": "1.0.0"
}
```

---

### Configuration Management

#### Get All Configurations

```
GET /config
```

Retrieves all stored configurations.

**Response:**

```json
{
  "success": true,
  "data": [
    { "id": "uuid", "config_name": "default_currency", "config_value": "BRL" },
    {
      "id": "uuid",
      "config_name": "last_update",
      "config_value": "2025-12-25..."
    }
  ],
  "message": "Configuration retrieved successfully"
}
```

#### Get Specific Configuration

```
GET /config?configName=last-update
```

**Query Parameters:**

- `configName` (required): Configuration key name

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "config_name": "last_update",
    "config_value": "2025-12-25T13:22:07.296Z"
  },
  "message": "Configuration retrieved successfully"
}
```

#### Update Configuration

```
PUT /config
```

**Body (JSON):**

```json
{
  "default_currency": "USD",
  "name": "My Financial Portfolio",
  "version": "1.0"
}
```

**Response:**

```json
{
  "success": true,
  "data": [
    { "id": "uuid", "config_name": "default_currency", "config_value": "USD" },
    {
      "id": "uuid",
      "config_name": "name",
      "config_value": "My Financial Portfolio"
    }
  ],
  "message": "Configuration updated successfully"
}
```

---

### Asset Management

#### Create Asset

```
POST /market/asset
```

**Body (JSON):**

```json
{
  "name": "AAPL",
  "currency_code": "USD",
  "current_price": 273.67,
  "target_price": 270.0,
  "drop_alert": true,
  "target_gap_percentage": 1.34,
  "sector": "Technology",
  "pl_ratio": 28.5,
  "pvpa_ratio": 42.8
}
```

**Required Fields:** `name`, `current_price`
**Optional Fields:** `currency_code` (default: "BRL"), `target_price`, `drop_alert`, etc.

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "ticker_symbol": "AAPL",
    "asset_name": "AAPL"
  },
  "message": "Asset created successfully"
}
```

#### Get All Assets

```
GET /market/assets
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "ticker_symbol": "AAPL",
      "asset_name": "AAPL",
      "currency_code": "USD",
      "current_price": 273.67,
      "target_price": 270.0,
      "drop_alert_enabled": true,
      "time_to_buy": false
    }
  ],
  "message": "Assets retrieved successfully"
}
```

#### Get Specific Asset

```
GET /market/asset?tickerSymbol=AAPL
```

**Query Parameters:**

- `tickerSymbol` (required): Stock ticker symbol

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "ticker_symbol": "AAPL",
    "asset_name": "AAPL",
    "currency_code": "USD",
    "current_price": 273.67,
    "target_price": 270.0,
    "drop_alert_enabled": true,
    "time_to_buy": false,
    "sector": "Technology",
    "pl_ratio": 28.5,
    "pvpa_ratio": 42.8
  },
  "message": "Asset retrieved successfully"
}
```

#### Update Asset

```
PUT /market/asset?tickerSymbol=AAPL
```

**Query Parameters:**

- `tickerSymbol` (required): Stock ticker symbol

**Body (JSON):**

```json
{
  "current_price": 275.0,
  "target_price": 272.0,
  "drop_alert": true
}
```

**Response:**

```json
{
  "success": true,
  "data": { "ticker_symbol": "AAPL" },
  "message": "Asset updated successfully"
}
```

#### Delete Asset

```
DELETE /market/asset?tickerSymbol=AAPL
```

**Query Parameters:**

- `tickerSymbol` (required): Stock ticker symbol

**Response:**

```json
{
  "success": true,
  "data": null,
  "message": "Asset deleted successfully"
}
```

---

### Currency Management

#### Create Currency

```
POST /market/currency
```

**Body (JSON):**

```json
{
  "name": "USD",
  "base_currency": "BRL",
  "current_price": 5.54,
  "target_price": 5.0,
  "drop_alert": true
}
```

**Required Fields:** `name`, `current_price`
**Optional Fields:** `base_currency`, `target_price`, `drop_alert`

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "currency_code": "USD"
  },
  "message": "Currency created successfully"
}
```

#### Get All Currencies

```
GET /market/currencies
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "currency_code": "USD",
      "currency_name": "USD",
      "base_currency": "BRL",
      "current_price": 5.54,
      "target_price": 5.0,
      "drop_alert_enabled": true,
      "time_to_buy": false
    }
  ],
  "message": "Currencies retrieved successfully"
}
```

#### Get Specific Currency

```
GET /market/currency?currencyCode=USD
```

**Query Parameters:**

- `currencyCode` (required): Currency code (e.g., USD, EUR, AUD)

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "currency_code": "USD",
    "currency_name": "USD",
    "base_currency": "BRL",
    "current_price": 5.54,
    "target_price": 5.0,
    "drop_alert_enabled": true,
    "time_to_buy": false
  },
  "message": "Currency retrieved successfully"
}
```

#### Update Currency

```
PUT /market/currency?currencyCode=USD
```

**Query Parameters:**

- `currencyCode` (required): Currency code

**Body (JSON):**

```json
{
  "current_price": 5.4,
  "target_price": 5.0,
  "drop_alert": true
}
```

**Response:**

```json
{
  "success": true,
  "data": { "currency_code": "USD" },
  "message": "Currency updated successfully"
}
```

#### Delete Currency

```
DELETE /market/currency?currencyCode=USD
```

**Query Parameters:**

- `currencyCode` (required): Currency code

**Response:**

```json
{
  "success": true,
  "data": null,
  "message": "Currency deleted successfully"
}
```

---

### Market Alerts & Analysis

#### Get Drop Alert Assets

```
GET /market/drop-alert/assets
```

Returns assets that have reached or fallen below their target price (ready to buy).

**Requirements:**

- Asset must have `drop_alert` = true
- Asset must have `target_price` defined
- Current price ≤ target price

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "ticker_symbol": "AAPL",
      "asset_name": "AAPL",
      "current_price": 269.5,
      "target_price": 270.0,
      "time_to_buy": true,
      "gap_percentage": 0.18
    }
  ],
  "message": "Found 1 assets ready to buy"
}
```

#### Get Drop Alert Currencies

```
GET /market/drop-alert/currencies
```

Returns currencies that have reached or fallen below their target price.

**Requirements:**

- Currency must have `drop_alert` = true
- Currency must have `target_price` defined
- Current price ≤ target price

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "currency_code": "USD",
      "currency_name": "USD",
      "current_price": 4.98,
      "target_price": 5.0,
      "time_to_buy": true,
      "gap_percentage": 0.4
    }
  ],
  "message": "Found 1 currencies ready to buy"
}
```

#### Get Market Prediction Report

```
GET /market/report/prediction
```

Fetches AI-powered market predictions from magfi-predictor service.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "ticker": "AAPL",
      "current_price": 273.67,
      "predicted_price": 275.5,
      "confidence": 0.72,
      "direction": "bullish"
    },
    {
      "ticker": "IBM",
      "current_price": 180.0,
      "predicted_price": 177.25,
      "confidence": 0.65,
      "direction": "bearish"
    }
  ],
  "message": "Generated predictions for 2 assets"
}
```

---

### Account & Portfolio Management

#### Create Account

```
POST /market/account
```

**Body (JSON):**

```json
{
  "account_name": "Nomad Investimentos",
  "is_investment_account": true,
  "is_payroll_account": false,
  "total_invested": 50.0,
  "monthly_salary": null,
  "checking_account_balance": 31.01,
  "default_currency": "USD"
}
```

**Required Fields:** `account_name`
**Optional Fields:** Account type flags, balances

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "account_name": "Nomad Investimentos"
  },
  "message": "Account created successfully"
}
```

#### Get All Accounts

```
GET /market/accounts
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "account_name": "Nomad Investimentos",
      "is_investment_account": true,
      "is_payroll_account": false,
      "total_invested": 50.0,
      "default_currency": "USD"
    }
  ],
  "message": "Accounts retrieved successfully"
}
```

#### Get Dividend Gains

```
GET /market/dividend-gains
```

Returns all dividend payments recorded in the system.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "asset_id": "uuid",
      "dividend_amount": 10.5,
      "dividend_type": "dividend",
      "ex_dividend_date": "2025-12-15T00:00:00",
      "payment_date": "2025-12-25T00:00:00"
    }
  ],
  "message": "Dividend gains retrieved successfully"
}
```

---

## MAGFI-INGESTOR Endpoints

### Health

```
GET /health
```

### Ingest News

```
POST /ingest/news
```

Triggers news collection from RSS feeds and AI sentiment analysis.

**Response:**

```json
{
  "success": true,
  "data": { "ingested_count": 15 },
  "message": "Successfully ingested 15 news items"
}
```

### Get Raw News

```
GET /ingest/news/raw?limit=100
```

**Query Parameters:**

- `limit` (optional): Maximum number of news items (default: 100)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "Apple Q4 Earnings Beat Expectations",
      "source": "https://feeds.bloomberg.com/markets/news.rss",
      "created_at": "2025-12-25T13:22:07"
    }
  ],
  "message": "Raw news retrieved"
}
```

### Get Analyzed News

```
GET /ingest/news/analyzed?limit=100
```

Returns AI-processed news with sentiment analysis.

**Query Parameters:**

- `limit` (optional): Maximum number of news items (default: 100)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "Apple Q4 Earnings Beat Expectations",
      "sentiment": "positive",
      "impact_score": 0.85,
      "ticker": "AAPL"
    }
  ],
  "message": "Analyzed news retrieved"
}
```

---

## MAGFI-PREDICTOR Endpoints

### Health

```
GET /health
```

### Get Market Predictions

```
GET /predict
```

Generates market-wide predictions based on sentiment analysis.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "ticker": "AAPL",
      "current_price": 273.67,
      "predicted_price": 275.5,
      "confidence": 0.72,
      "direction": "bullish",
      "analysis_based_on_news_items": 3
    }
  ],
  "message": "Generated predictions for 5 assets"
}
```

### Get Asset-Specific Prediction

```
GET /predict/{ticker}
```

**Path Parameters:**

- `ticker` (required): Stock ticker symbol (e.g., AAPL, IBM)

**Response:**

```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "current_price": 273.67,
    "predicted_price": 275.5,
    "confidence": 0.72,
    "direction": "bullish",
    "analysis_based_on_news_items": 3
  },
  "message": "Prediction generated successfully"
}
```

---

## Error Responses

All services return consistent error format:

```json
{
  "success": false,
  "error": "error_code",
  "message": "Detailed error description"
}
```

### Common HTTP Status Codes

- `200`: Success
- `400`: Bad request (missing required fields)
- `404`: Resource not found
- `500`: Internal server error

### Common Errors

```json
{
  "success": false,
  "error": "not_found",
  "message": "Asset not found"
}
```

```json
{
  "success": false,
  "error": "validation_error",
  "message": "Asset name is required"
}
```

```json
{
  "success": false,
  "error": "service_unavailable",
  "message": "Unable to fetch predictions at the moment"
}
```

---

## Rate Limits & Notes

- No rate limiting in current version
- All monetary values are stored as NUMERIC(15,4) in database
- Prices use format "value/CURRENCY" in JSON
- Responses include pagination for list endpoints
- All timestamps in UTC (ISO 8601 format)

---

## Testing Endpoints

### Using cURL

```bash
# GET request
curl http://localhost:8100/health

# POST request
curl -X POST http://localhost:8100/market/asset \
  -H "Content-Type: application/json" \
  -d '{"name":"AAPL","current_price":273.67}'

# PUT request
curl -X PUT "http://localhost:8100/market/asset?tickerSymbol=AAPL" \
  -H "Content-Type: application/json" \
  -d '{"current_price":275.00}'

# DELETE request
curl -X DELETE "http://localhost:8100/market/asset?tickerSymbol=AAPL"
```

### Using Swagger UI

1. Go to http://localhost:8100/docs (magfi-core)
2. Click on endpoint
3. Click "Try it out"
4. Fill parameters/body
5. Click "Execute"

### Using Python

```python
import requests

# Get all assets
response = requests.get("http://localhost:8100/market/assets")
assets = response.json()["data"]

# Create asset
response = requests.post(
    "http://localhost:8100/market/asset",
    json={
        "name": "MSFT",
        "current_price": 410.50,
        "target_price": 400.00,
        "drop_alert": True
    }
)
print(response.json())
```

---

## Endpoint Summary Table

| Method | Path                          | Purpose              |
| ------ | ----------------------------- | -------------------- |
| GET    | /health                       | Service health       |
| GET    | /config                       | All configs          |
| GET    | /config?configName=X          | Specific config      |
| PUT    | /config                       | Update config        |
| POST   | /market/asset                 | Create asset         |
| GET    | /market/assets                | All assets           |
| GET    | /market/asset                 | Specific asset       |
| PUT    | /market/asset                 | Update asset         |
| DELETE | /market/asset                 | Delete asset         |
| POST   | /market/currency              | Create currency      |
| GET    | /market/currencies            | All currencies       |
| GET    | /market/currency              | Specific currency    |
| PUT    | /market/currency              | Update currency      |
| DELETE | /market/currency              | Delete currency      |
| GET    | /market/drop-alert/assets     | Buy-ready assets     |
| GET    | /market/drop-alert/currencies | Buy-ready currencies |
| GET    | /market/report/prediction     | Market predictions   |
| POST   | /market/account               | Create account       |
| GET    | /market/accounts              | All accounts         |
| GET    | /market/dividend-gains        | Dividends            |
| POST   | /ingest/news                  | Collect news         |
| GET    | /ingest/news/raw              | Raw news             |
| GET    | /ingest/news/analyzed         | Analyzed news        |
| GET    | /predict                      | Market predictions   |
| GET    | /predict/{ticker}             | Asset prediction     |
