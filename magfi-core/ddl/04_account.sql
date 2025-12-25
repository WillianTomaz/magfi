-- Account dimension table
CREATE TABLE IF NOT EXISTS dim_account (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_name VARCHAR(255) NOT NULL,
    is_investment_account BOOLEAN DEFAULT FALSE,
    is_payroll_account BOOLEAN DEFAULT FALSE,
    total_invested NUMERIC(15, 4),
    monthly_salary NUMERIC(15, 4),
    checking_account_balance NUMERIC(15, 4),
    default_currency VARCHAR(3) NOT NULL DEFAULT 'BRL',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_account_type ON dim_account(is_investment_account, is_payroll_account);

-- Portfolio position fact table
CREATE TABLE IF NOT EXISTS fct_portfolio_position (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    asset_id UUID NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    average_cost NUMERIC(15, 4) NOT NULL,
    acquisition_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES dim_account(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES dim_asset(id) ON DELETE CASCADE
);

CREATE INDEX idx_portfolio_account ON fct_portfolio_position(account_id);
CREATE INDEX idx_portfolio_asset ON fct_portfolio_position(asset_id);
