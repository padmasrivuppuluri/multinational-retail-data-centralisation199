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

ALTER TABLE orders_table
DROP CONSTRAINT FK_product_code; 



