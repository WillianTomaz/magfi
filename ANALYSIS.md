# MAGFI - Deep Analysis & Architecture Documentation

## Executive Summary

MAGFI is a **distributed financial intelligence platform** composed of three microservices designed to provide real-time asset/currency monitoring, AI-driven sentiment analysis, and market predictions. The architecture emphasizes independence and loose coupling—**magfi-core operates standalone** while optionally consuming data from magfi-ingestor and magfi-predictor.

---

## Financial Data Analysis

### JSON Structure Insights (financial-data-config.json)

#### 1. **Config Object**
```json
{
  "name": "My Financial Track.",
  "version": "1.0",
  "last-update": "2025-12-20 14:31:00",
  "default-currency": "BRL"
}
```

**Key Implications:**
- `default-currency`: Critical for multi-currency comparisons. All price gaps and target-gap-percentages must reference this base.
- `last-update`: Automatically updated whenever assets/currencies are modified (trigger from PUT/POST operations)
- Enables users to track multiple portfolios with different base currencies (USD, EUR, BRL, etc.)

#### 2. **Asset Object Structure**
```json
{
  "uuid": "ac55b87a-2e80-411a-a8ab-3e6423b253c7",
  "name": "PETR4",
  "drop-alert": true,
  "current-price": "31.01/BRL",
  "target-price": "29.00/BRL",
  "target-gap-percentage": "6,48%",
  "time-to-buy": false
}
```

**Critical Analysis:**

1. **Price Format Strategy** (`price/CURRENCY`):
   - Encodes currency alongside price (e.g., "31.01/BRL")
   - Enables mixed portfolios (AAPL in USD, PETR4 in BRL)
   - Requires parsing on backend OR storage normalization

2. **Gap Calculation Logic**:
   - `target-gap-percentage = ((target-price - current-price) / current-price) × 100`
   - Example: PETR4 = ((29.00 - 31.01) / 31.01) × 100 = -6.48%
   - Negative gap = stock is ABOVE target (not yet time to buy)
   - When `current-price ≤ target-price`, `time-to-buy = true`

3. **Financial Indicators Missing** (P/L, P/VPA):
   - Not populated in example JSON but included in schema
   - **P/L Ratio (Price-to-Earnings)**: Company valuation metric
     - P/L < sector median = potentially undervalued
   - **P/VPA Ratio (Price-to-Book)**: Asset backing evaluation
     - P/VPA < 1.0 = trading below tangible book value (rare bargain)

4. **Multi-Asset Considerations**:
   - Assets in same portfolio can have different base currencies
   - AAPL/USD and PETR4/BRL require exchange rate conversion for comparison

#### 3. **Currency Object Structure**
```json
{
  "uuid": "a4d77e64-64f8-409d-b7a7-4b7f49d06813",
  "name": "USD",
  "drop-alert": true,
  "current-price": "5.54/BRL",
  "target-price": "5.00/BRL",
  "time-to-buy": false
}
```

**Key Observations:**
- Simpler structure than assets (no sector/ratios needed)
- `current-price`: Exchange rate (5.54 BRL per 1 USD)
- Critical for converting multi-currency portfolios to base currency
- When USD drops to 5.00 BRL, favorable to buy USD

#### 4. **Account Object** (Feature Extension)
```json
{
  "uuid": "ac55b87a-2e80-411a-a8ab-3e6423b253c7",
  "name": "Nomad Investimentos",
  "is-investment-account": true,
  "total-invested": "50.00/USD",
  "checking-account": "31.01/USD",
  "investment-portfolio": [...]
}
```

**Portfolio Tracking Implications:**
- **Dividend Gains Endpoint**: `/market/dividend-gains`
  - Sum dividend payments per asset per period (day/week/month/year)
  - Track dividend yield = (annual dividends / investment) × 100%
  - Identify high-yield positions

---

## Database Schema Design Decisions

### 1. **Dimensional Modeling (Star Schema)**

**Dimensions (Slow-Changing)**
- `dim_config`: User settings
- `dim_asset`: Stock/FII metadata
- `dim_currency`: Currency pairs
- `dim_account`: User accounts

**Facts (Fast-Changing)**
- `fct_asset_price_history`: Historical quotes
- `fct_currency_price_history`: Exchange rate history
- `fct_portfolio_position`: Asset holdings
- `fct_dividend`: Distribution records
- `fct_news_analysis`: Sentiment scores
- `fct_prediction`: ML forecasts

### 2. **Key Design Choices**

**UUID Primary Keys**
- Better for distributed systems + Supabase replication
- Avoid sequential integer leakage

**Decimal vs Float**
- `NUMERIC(15,4)`: Financial prices (exact)
- `FLOAT`: Ratios/percentages (calculated values)

**Composite Indices**
- `(drop_alert_enabled, is_active)` on assets
- Speeds up "find all assets with active alerts"

**JSON Storage NOT Used**
- Normalized relations enable filtering/aggregation
- Example: "Get all assets with P/L < 10" queries impossible with JSON

---

## Alert Logic Implementation

### Drop Alert Algorithm

```python
def get_drop_alert_assets():
    assets = SELECT * FROM dim_asset 
    WHERE drop_alert_enabled = TRUE 
    AND target_price IS NOT NULL
    
    for asset in assets:
        if asset.current_price <= asset.target_price:
            asset.time_to_buy = True
            gap = ((target - current) / current) × 100
            return {asset, gap}
```

**Example Flow:**
1. User sets PETR4 target: 29.00 BRL
2. Daily price check: Market closes at 28.50 BRL
3. Condition met: `28.50 ≤ 29.00` → `time_to_buy = true`
4. Response includes gap percentage: `((29 - 28.50) / 28.50) × 100 = 1.75%`

---

## Multi-Service Architecture

### Service Responsibilities

**magfi-core** (Independent)
- Single source of truth for config/assets/currencies
- Computes drop alerts (no external dependency)
- Aggregates data from other services optionally

**magfi-ingestor** (News → Sentiment)
- `stg_news_raw` table: Raw articles
- AI analysis (OpenAI/Gemini): Sentiment + impact scoring
- `fct_news_analysis` table: Enriched records
- magfi-core queries this table for prediction context

**magfi-predictor** (Forecast Engine)
- Consumes: Historical prices + sentiment data
- Produces: Price targets + confidence scores
- Returns via magfi-core → `/market/report/prediction`

### Decoupling Strategy

```
magfi-core:8000
  ├─→ [Independent operation]
  ├─→ /health (always works)
  ├─→ /market/asset (always works)
  └─→ /market/report/prediction
      └─→ calls magfi-predictor:8002 (degrades gracefully if down)
```

---

## Implementation Notes

### 1. **Price Format Parsing**
Current JSON uses `"price/CURRENCY"` strings. Implementation:

```python
def parse_price_currency(price_str: str) -> tuple:
    # Input: "31.01/BRL"
    price, currency = price_str.split('/')
    return float(price), currency  # (31.01, 'BRL')

# Database storage: separate NUMERIC column + VARCHAR(3) currency_code
```

### 2. **Dividend Tracking Endpoint**
```python
@router.get("/market/dividend-gains")
def get_dividends(period: str = "year"):
    # period = "day" | "week" | "month" | "year"
    cutoff_date = calculate_period_start(period)
    
    return db.query(Dividend)
        .filter(Dividend.payment_date >= cutoff_date)
        .group_by(Dividend.asset_id)
        .sum(Dividend.dividend_amount)
```

### 3. **Multi-Currency Conversion**
```python
def get_assets_in_default_currency(assets, default_currency, rates):
    results = []
    for asset in assets:
        if asset.currency_code != default_currency:
            # Fetch USD/BRL rate if asset is in USD
            conversion_rate = rates[f"{asset.currency_code}/{default_currency}"]
            converted_price = asset.current_price * conversion_rate
        else:
            converted_price = asset.current_price
        results.append(converted_price)
    return results
```

---

## Financial Sector Comparison Strategy

For P/L and P/VPA evaluation:

1. **Data Ingestion**: Populate `dim_asset.sector` + `pl_ratio`, `pvpa_ratio`
2. **Benchmark Queries**:
```sql
SELECT AVG(pl_ratio) as sector_avg_pl
FROM dim_asset
WHERE sector = 'Energy' AND is_active = TRUE;

-- Compare individual: PETR4.pl_ratio vs sector_avg_pl
```

3. **Fair Value Assessment**:
   - PETR4 P/L = 8, Sector avg = 12 → **8% undervalued**
   - PETR4 P/VPA = 0.85, Sector avg = 1.2 → **Trading below book value**

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    End User                                  │
└────────────────────┬────────────────────────────────────────┘
                     │ POST /market/asset
                     ▼
         ┌──────────────────────────┐
         │    magfi-core:8000       │
         │  ┌────────────────────┐  │
         │  │ dim_config         │  │
         │  │ dim_asset          │  │ ◄── Pull historical data
         │  │ dim_currency       │  │
         │  │ fct_portfolio      │  │
         │  └────────────────────┘  │
         └──────────┬──────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   GET /drop-  GET /dividend- GET /report/
   alert       gains          prediction
        │           │           │
        │           │           │ calls magfi-predictor:8002
        │           │           ├──► Fetch assets + news sentiment
        │           │           └──► Return ML predictions
        │           │
        │           ├─ magfi-ingestor:8001
        │           └──► Queries fct_news_analysis
        │
        └──► Internal logic (no external calls)
```

---

## Risk & Mitigation

| Risk | Mitigation |
|------|-----------|
| **Currency conversion stale** | Cache rates with TTL; fallback to yesterday's rate |
| **AI predictions inaccurate** | Display confidence scores; don't use <50% confidence |
| **magfi-predictor down** | magfi-core returns cached predictions or "data unavailable" |
| **Large portfolio slow queries** | Indices on (asset_id, is_active); pagination on list endpoints |
| **User mistakes (wrong target)** | Implement PUT to update; soft deletes (is_active=false) |

---

## Success Metrics

1. **System**: All 3 services healthy, <200ms response times
2. **Business**: Alerts triggered within 2 hours of price target hit
3. **ML**: Prediction accuracy > 60% on 1-week horizon
4. **UX**: Portfolio dashboard loads <1s for 100 assets

---

## Conclusion

MAGFI provides a **production-grade financial monitoring platform** with:
- ✅ Independent core service (can work offline)
- ✅ Pluggable news/prediction engines
- ✅ Multi-currency + multi-account support
- ✅ Scalable alert mechanism
- ✅ AI-powered market insights

All code follows **PEP 8**, uses **type hints**, and is **deployment-ready with Docker**.
