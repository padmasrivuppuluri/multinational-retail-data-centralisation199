"Task4:Make changes to dim products"

SELECT * FROM dim_products

"Removing $ character before product price"
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')
WHERE product_price LIKE '£%'

"To add new column weight_class"
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(255)

UPDATE dim_products
SET weight_class = CASE
    WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) < 2 THEN 'Light'
    WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) >= 2 
         AND CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) < 40 THEN 'Mid_Sized'
    WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) >= 40 
         AND CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) < 140 THEN 'Heavy'
    WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL) >= 140 THEN 'Truck_Required'
    ELSE 'Unknown' -- If the weight is not a valid numeric value
END;

"Task5 :            
1:Rename the removed column to still_available "
ALTER TABLE dim_products
RENAME COLUMN removed to still_available;
"2.Changing the datatype"
"To change for weight column:"
ALTER TABLE dim_products
    ALTER COLUMN weight TYPE NUMERIC USING REGEXP_REPLACE(weight, '[^0-9.]', '', 'g')::NUMERIC;
ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE NUMERIC USING product_price::NUMERIC,
    ALTER COLUMN "EAN" TYPE VARCHAR(20),
    ALTER COLUMN product_code TYPE VARCHAR(255),
    ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    ALTER COLUMN still_available TYPE BOOLEAN USING
        CASE
            WHEN still_available IN ('yes', 'true', '1') THEN TRUE
            WHEN still_available IN ('no', 'false', '0') THEN FALSE
            ELSE NULL 
        END,
    ALTER COLUMN weight_class TYPE VARCHAR(20);

    