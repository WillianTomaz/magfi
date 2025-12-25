-- Analyzed news fact table
CREATE TABLE IF NOT EXISTS fct_news_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_ticker VARCHAR(20),
    news_title VARCHAR NOT NULL,
    news_content TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    impact_score FLOAT NOT NULL,
    ai_analysis TEXT,
    source_url VARCHAR(500),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_news_analysis_ticker ON fct_news_analysis(asset_ticker);
CREATE INDEX idx_news_analysis_sentiment ON fct_news_analysis(sentiment);
CREATE INDEX idx_news_analysis_created ON fct_news_analysis(created_at);
