"Task8 :ADDING primary keys"

ALTER TABLE dim_users
    ADD CONSTRAINT pk_user_uuid PRIMARY KEY (user_uuid)

ALTER TABLE dim_store_details
    ADD CONSTRAINT pk_store_code PRIMARY KEY (store_code)

ALTER TABLE dim_products
    ADD CONSTRAINT pk_product_code PRIMARY KEY (product_code)

ALTER TABLE dim_date_times
    ADD CONSTRAINT pk_date_uuid PRIMARY KEY (date_uuid)

ALTER TABLE dim_card_details
    ADD CONSTRAINT pk_card_number PRIMARY KEY (card_number)