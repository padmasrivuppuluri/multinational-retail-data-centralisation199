SELECT * FROM dim_date_times

"Task 7: update the datatypes:
month,year,day,timeperiod-->Text to VARCHAR,
date_uuid -->Text to UUID"
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(10),
    ALTER COLUMN year TYPE VARCHAR(10),
    ALTER COLUMN day TYPE VARCHAR(10),
    ALTER COLUMN time_period TYPE VARCHAR(50),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;
