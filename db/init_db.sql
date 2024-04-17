-- init_db.sql
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    xp INTEGER DEFAULT 0
);