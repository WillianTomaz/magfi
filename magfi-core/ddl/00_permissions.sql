-- Grant permissions to postgres user on app_magfi schema
GRANT USAGE ON SCHEMA app_magfi TO postgres;

-- Grant SELECT, INSERT, UPDATE, DELETE on all existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app_magfi TO postgres;

-- Grant USAGE and SELECT on all sequences for auto-increment
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app_magfi TO postgres;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA app_magfi GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_magfi GRANT USAGE, SELECT ON SEQUENCES TO postgres;
