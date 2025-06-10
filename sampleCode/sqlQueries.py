"""
Stuff
"""

# SQL Query Templates

SQL_CREATE_DATABASE_TEMPLATE = """
    CREATE DATABASE IF NOT EXISTS {}
"""

SQL_DROP_TABLE_TEMPLATE = """
    DROP TABLE IF EXISTS {}
"""

SQL_CREATE_TABLE_TEMPLATE = """
CREATE TABLE {} (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    signup_date DATE,
    last_active_date DATE,
    is_retained BOOLEAN,
    plan_type VARCHAR(50),
    region VARCHAR(50),
    total_spent DECIMAL(10,2),
    last_purchase_date DATE,
    feedback_score FLOAT,
    account_manager VARCHAR(100),
    referral_source VARCHAR(100),
    login_count INT,
    support_tickets INT
)
"""

SQL_INSERT_DATA_TEMPLATE = """
INSERT INTO {} (
    customer_id, customer_name, email, signup_date, last_active_date,
    is_retained, plan_type, region, total_spent, last_purchase_date,
    feedback_score, account_manager, referral_source, login_count, 
    support_tickets
) VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""