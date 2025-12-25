-- Asset dimension table
CREATE TABLE IF NOT EXISTS app_magfi.dim_asset (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker_symbol VARCHAR(20) NOT NULL UNIQUE,
    asset_name VARCHAR(255) NOT NULL,
    currency_code VARCHAR(3) NOT NULL,
    current_price NUMERIC(15, 4) NOT NULL,
    target_price NUMERIC(15, 4),
    drop_alert_enabled BOOLEAN DEFAULT FALSE,
    target_gap_percentage FLOAT,
    time_to_buy BOOLEAN DEFAULT FALSE,
    sector VARCHAR(100),
    pl_ratio FLOAT,
    pvpa_ratio FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ticker_symbol ON app_magfi.dim_asset(ticker_symbol);
CREATE INDEX idx_asset_active ON app_magfi.dim_asset(is_active);
CREATE INDEX idx_asset_alert ON app_magfi.dim_asset(drop_alert_enabled, is_active);

-- Asset price history fact table
CREATE TABLE IF NOT EXISTS app_magfi.fct_asset_price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    price NUMERIC(15, 4) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES app_magfi.dim_asset(id) ON DELETE CASCADE
);

CREATE INDEX idx_asset_history ON app_magfi.fct_asset_price_history(asset_id, recorded_at);
