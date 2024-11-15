"Task2: Changing datatypes in dim_users table
first_name,last_name,country_code -->Text to VARCHAR,
date_of_birth,join_date --> TEXT to DATE
user_uuid -->Text to UUID,"

SELECT * FROM dim_users

ALTER TABLE dim_users
DROP COLUMN index;

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
    ALTER COLUMN country_code TYPE VARCHAR(10),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN join_date TYPE DATE USING join_date::DATE;