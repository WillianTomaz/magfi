-- Raw news staging table
CREATE TABLE IF NOT EXISTS app_magfi.stg_news_raw (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    feed_source VARCHAR(500) NOT NULL,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    link VARCHAR(500),
    published_date TIMESTAMP,
    raw_data TEXT,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_news_raw_source ON app_magfi.stg_news_raw(feed_source);
CREATE INDEX idx_news_raw_processed ON app_magfi.stg_news_raw(is_processed);
