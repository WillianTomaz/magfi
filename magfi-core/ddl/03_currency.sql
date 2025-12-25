-- Currency dimension table
CREATE TABLE IF NOT EXISTS app_magfi.dim_currency (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    currency_code VARCHAR(3) NOT NULL UNIQUE,
    currency_name VARCHAR(100) NOT NULL,
    base_currency VARCHAR(3) NOT NULL DEFAULT 'BRL',
    current_price NUMERIC(15, 4) NOT NULL,
    target_price NUMERIC(15, 4),
    drop_alert_enabled BOOLEAN DEFAULT FALSE,
    time_to_buy BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_currency_code ON app_magfi.dim_currency(currency_code);
CREATE INDEX idx_currency_active ON app_magfi.dim_currency(is_active);
CREATE INDEX idx_currency_alert ON app_magfi.dim_currency(drop_alert_enabled, is_active);

-- Currency price history fact table
CREATE TABLE IF NOT EXISTS app_magfi.fct_currency_price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    currency_id UUID NOT NULL,
    price NUMERIC(15, 4) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currency_id) REFERENCES app_magfi.dim_currency(id) ON DELETE CASCADE
);

CREATE INDEX idx_currency_history ON app_magfi.fct_currency_price_history(currency_id, recorded_at);
