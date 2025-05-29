-- Create targeting_engine database
CREATE DATABASE IF NOT EXISTS targeting_engine;
USE targeting_engine;

-- Create campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(1024) NOT NULL,
    cta VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create targeting_rules table
CREATE TABLE IF NOT EXISTS targeting_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id VARCHAR(255) NOT NULL,
    include_country VARCHAR(1024),
    exclude_country VARCHAR(1024),
    include_os VARCHAR(1024),
    exclude_os VARCHAR(1024),
    include_app VARCHAR(1024),
    exclude_app VARCHAR(1024),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_campaign_status ON campaigns(status);
CREATE INDEX idx_targeting_campaign_id ON targeting_rules(campaign_id);

-- Create test database
CREATE DATABASE IF NOT EXISTS targeting_engine_test;
