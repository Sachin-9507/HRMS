CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE INDEX IF NOT EXISTS idx_user_otps_user_id ON users_otps(user_id);

CREATE INDEX IF NOT EXISTS idx_user_otps_expires_at ON users_otps(expires_at);

CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id);

CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);