-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    pan_number VARCHAR(20) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    ifsc_code VARCHAR(20) NOT NULL,
    kyc_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the analytics table (optional)
CREATE TABLE kyc_analytics (
    total_attempted INT DEFAULT 0,
    total_successful INT DEFAULT 0,
    total_failed INT DEFAULT 0,
    total_failed_due_to_pan INT DEFAULT 0,
    total_failed_due_to_bank INT DEFAULT 0
);
