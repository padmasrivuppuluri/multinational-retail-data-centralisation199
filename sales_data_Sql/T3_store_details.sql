SELECT * FROM dim_store_details
ALTER TABLE dim_store_details
DROP COLUMN index;

"Task3: There are two latitude columns in the store details table. Using SQL, merge one of the columns into the other so you have one latitude column."
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
    ALTER COLUMN store_code TYPE VARCHAR(255),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
    ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE NUMERIC USING latitude::NUMERIC,
    ALTER COLUMN country_code TYPE VARCHAR(10),
    ALTER COLUMN continent TYPE VARCHAR(255);

SELECT locality FROM dim_store_details WHERE locality = 'N/A' "no data"
