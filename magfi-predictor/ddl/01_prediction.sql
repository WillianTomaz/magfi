-- Predictions fact table
CREATE TABLE IF NOT EXISTS app_magfi.fct_prediction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID,
    prediction_type VARCHAR(50) NOT NULL,
    predicted_price NUMERIC(15, 4),
    confidence_score FLOAT NOT NULL,
    prediction_date TIMESTAMP NOT NULL,
    analysis_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES app_magfi.dim_asset(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_prediction_asset ON app_magfi.fct_prediction(asset_id);
CREATE INDEX IF NOT EXISTS idx_prediction_date ON app_magfi.fct_prediction(prediction_date);
CREATE INDEX IF NOT EXISTS idx_prediction_created ON app_magfi.fct_prediction(created_at);
