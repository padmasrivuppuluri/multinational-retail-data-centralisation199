SELECT * FROM orders_table

ALTER TABLE orders_table
DROP COLUMN level_0,
DROP COLUMN index;

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