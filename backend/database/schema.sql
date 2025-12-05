-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    plan VARCHAR(50) DEFAULT 'free'
);

-- analyses table
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT,
    analysis_duration_seconds DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- usage table
CREATE TABLE usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    analyses_count INT DEFAULT 0,
    storage_used_bytes BIGINT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT NOW()
);
