SELECT * FROM orders_table

"Task1:Changing datatypes in orders table 
date_uuid,user_uuid -->Text to UUID,
card_number,store_code, product code -->Text to VARCHAR(255),
product_quantity -->Text to SMALLINT"

ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN card_number TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(255),
    ALTER COLUMN product_code TYPE VARCHAR(255),
    ALTER COLUMN product_quantity TYPE SMALLINT USING product_quantity::SMALLINT;


"Task2: Changing datatypes in dim_users table
first_name,last_name,country_code -->Text to VARCHAR,
date_of_birth,join_date --> TEXT to DATE
user_uuid -->Text to UUID,"

"Remove invalid date values in date_of_birth column"
DELETE FROM dim_users
WHERE NOT(date_of_birth ~ '^\d{4}-\d{2}-\d{2}$') "Removed 42 rows"

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
    ALTER COLUMN country_code TYPE VARCHAR(10),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN join_date TYPE DATE USING join_date::DATE;

"Task3: There are two latitude columns in the store details table. Using SQL, merge one of the columns into the other so you have one latitude column."


SELECT * FROM dim_store_details
"Update the latitude column with the merged data"
UPDATE dim_store_details
SET latitude = COALESCE(latitude, lat);

"Drop the redundant lat column"
ALTER TABLE dim_store_details
DROP COLUMN lat;

"Updating datatypes in dim_store_details_table"
ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE NUMERIC USING longitude::NUMERIC,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(20),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
    ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE NUMERIC USING latitude::NUMERIC,
    ALTER COLUMN country_code TYPE VARCHAR(10),
    ALTER COLUMN continent TYPE VARCHAR(255);

SELECT locality FROM dim_store_details WHERE locality = 'N/A' "no data"

Task 4:
"Removing $ character befor product price"
SELECT * FROM dim_products
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')
WHERE product_price LIKE '£%'
"To add new column weight_class"
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(255)

UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >=2 AND weight <40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight <140 THEN 'Heavy'
    WHEN weight >=140 THEN 'Truck_Required'
END;

"Task5 :            
1:Rename the removed column to still_available "
ALTER TABLE dim_products
RENAME COLUMN removed to still_available;
"2.Changing the datatype"
ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE NUMERIC USING product_price::NUMERIC,
    ALTER COLUMN weight TYPE NUMERIC USING weight::NUMERIC,
    ALTER COLUMN "EAN" TYPE VARCHAR(20),
    ALTER COLUMN product_code TYPE VARCHAR(20),
    ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    ALTER COLUMN still_available TYPE BOOLEAN USING
        CASE
            WHEN still_available IN ('yes', 'true', '1') THEN TRUE
            WHEN still_available IN ('no', 'false', '0') THEN FALSE
            ELSE NULL 
        END,
    ALTER COLUMN weight_class TYPE VARCHAR(20);

"Task 7:
"
SELECT * FROM dim_date_times
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(10),
    ALTER COLUMN year TYPE VARCHAR(10),
    ALTER COLUMN day TYPE VARCHAR(10),
    ALTER COLUMN time_period TYPE VARCHAR(50),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

"Task 8:"

SELECT * FROM dim_card_details 
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(100),
    ALTER COLUMN expiry_date TYPE VARCHAR(100),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;

"Task 9:ADDING primary keys"
SELECT * FROM dim_users
"SELECT Null values in dim_users users_uuid"
SELECT * FROM dim_users WHERE user_uuid IS NULL;
"Delete "
DELETE FROM dim_users WHERE user_uuid is NULL;

ALTER TABLE dim_users
    ADD CONSTRAINT pk_user_uuid PRIMARY KEY (user_uuid)

SELECT * FROM dim_store_details
ALTER TABLE dim_store_details
    ADD CONSTRAINT pk_store_code PRIMARY KEY (store_code)

SELECT * FROM dim_products
ALTER TABLE dim_products
    ADD CONSTRAINT pk_product_code PRIMARY KEY (product_code)

SELECT * FROM dim_date_times
ALTER TABLE dim_date_times
    ADD CONSTRAINT pk_date_uuid PRIMARY KEY (date_uuid)

SELECT * FROM dim_card_details
"TO check duplicate card_numbers"
SELECT card_number, COUNT(*)
FROM dim_card_details
GROUP BY card_number
HAVING COUNT(*) > 1;   "output is 2..so we have 2 duplicate card numbers"
"To remove duplicate values:"
DELETE FROM dim_card_details
WHERE card_number IN (
    SELECT card_number
    FROM dim_card_details
    GROUP BY card_number
    HAVING COUNT(*) > 1
)
AND ctid NOT IN (
    SELECT min(ctid)
    FROM dim_card_details
    GROUP BY card_number
);

ALTER TABLE dim_card_details
    ADD CONSTRAINT pk_card_number PRIMARY KEY (card_number)

"Task 9: ADDing foreign keys"

ALTER TABLE orders_table
    ADD CONSTRAINT FK_user_uuid
    FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE orders_table
    ADD CONSTRAINT FK_date_uuid
    FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE orders_table
    ADD CONSTRAINT FK_store_code
    FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE orders_table
    ADD CONSTRAINT FK_card_number
    FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE orders_table
    ADD CONSTRAINT FK_product_code
    FOREIGN KEY (product_code) REFERENCES dim_products(product_code)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
"Create a left join which are not matching"
SELECT pc.product_code
FROM orders_table pc
LEFT JOIN dim_products dp ON pc.product_code = dp.product_code
WHERE dp.product_code is NULL;








