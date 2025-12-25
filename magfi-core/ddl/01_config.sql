-- Configuration table
CREATE TABLE IF NOT EXISTS dim_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_name VARCHAR(255) NOT NULL UNIQUE,
    config_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_config_name ON dim_config(config_name);

-- Insert default configurations
INSERT INTO dim_config (config_name, config_value) 
VALUES 
    ('app_name', 'magfi-core'),
    ('version', '1.0.0'),
    ('default_currency', 'BRL'),
    ('last_update', CURRENT_TIMESTAMP::TEXT)
ON CONFLICT (config_name) DO NOTHING;
