-- Analyzed news fact table
CREATE TABLE IF NOT EXISTS app_magfi.fct_news_analysis (
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
    FOREIGN KEY (asset_id) REFERENCES app_magfi.dim_asset(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_news_asset ON app_magfi.fct_news_analysis(asset_id);
CREATE INDEX IF NOT EXISTS idx_news_created ON app_magfi.fct_news_analysis(created_at);
