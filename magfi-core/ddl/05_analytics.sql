-- Dividend fact table
CREATE TABLE IF NOT EXISTS fct_dividend (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    dividend_amount NUMERIC(15, 4) NOT NULL,
    dividend_type VARCHAR(50) NOT NULL,
    ex_dividend_date TIMESTAMP NOT NULL,
    payment_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES dim_asset(id) ON DELETE CASCADE
);

CREATE INDEX idx_dividend_asset ON fct_dividend(asset_id);
CREATE INDEX idx_dividend_payment_date ON fct_dividend(payment_date);

-- News analysis fact table
CREATE TABLE IF NOT EXISTS fct_news_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID,
    news_title VARCHAR,
    news_content TEXT,
    sentiment VARCHAR(20) NOT NULL,
    impact_score FLOAT NOT NULL,
    ai_analysis TEXT,
    source_url VARCHAR,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES dim_asset(id) ON DELETE SET NULL
);

CREATE INDEX idx_news_asset ON fct_news_analysis(asset_id);
CREATE INDEX idx_news_created ON fct_news_analysis(created_at);

-- Prediction fact table
CREATE TABLE IF NOT EXISTS fct_prediction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID,
    prediction_type VARCHAR(50) NOT NULL,
    predicted_price NUMERIC(15, 4),
    confidence_score FLOAT NOT NULL,
    prediction_date TIMESTAMP NOT NULL,
    analysis_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES dim_asset(id) ON DELETE SET NULL
);

CREATE INDEX idx_prediction_asset ON fct_prediction(asset_id);
CREATE INDEX idx_prediction_date ON fct_prediction(prediction_date);
