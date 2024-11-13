"Task9:Creating Foreign Keys"

ALTER TABLE orders_table
    ADD CONSTRAINT FK_user_uuid
    FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid)

ALTER TABLE orders_table
    ADD CONSTRAINT FK_date_uuid
    FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid)

ALTER TABLE orders_table
    ADD CONSTRAINT FK_card_number
    FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number)

ALTER TABLE orders_table
    ADD CONSTRAINT FK_store_code
    FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code)

SELECT DISTINCT(ord.store_code)
FROM orders_table ord
WHERE NOT EXISTS
(SELECT * FROM dim_store_details t2
WHERE t2.store_code = ord.store_code);

"one store_code row is missing."
INSERT INTO dim_store_details (store_code)
VALUES ('WEB-1388012W'); 

ALTER TABLE orders_table
DROP CONSTRAINT FK_store_code;  -- Replace `fk_store_code` with your actual constraint name


ALTER TABLE orders_table
    ADD CONSTRAINT FK_product_code
    FOREIGN KEY (product_code) REFERENCES dim_products(product_code)

SELECT DISTINCT(ord.product_code)
FROM orders_table ord
WHERE NOT EXISTS
(SELECT * FROM dim_products t2
WHERE t2.product_code = ord.product_code);

INSERT INTO dim_products (product_code)
VALUES ('A8-4686892S')



