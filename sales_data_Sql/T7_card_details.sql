SELECT * FROM dim_card_details 

"Task7: update the datatypes:
card_number,expiry_date-->Text to VARCHAR
date_payment_confirmed -->Text to Date"

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(255),
    ALTER COLUMN expiry_date TYPE VARCHAR(100),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;
