-- Predictions fact table
CREATE TABLE IF NOT EXISTS fct_prediction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_ticker VARCHAR(20),
    prediction_type VARCHAR(50) NOT NULL,
    predicted_price FLOAT,
    confidence_score FLOAT NOT NULL,
    prediction_date TIMESTAMP NOT NULL,
    horizon_days INTEGER,
    analysis_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prediction_ticker ON fct_prediction(asset_ticker);
CREATE INDEX idx_prediction_date ON fct_prediction(prediction_date);
CREATE INDEX idx_prediction_created ON fct_prediction(created_at);
