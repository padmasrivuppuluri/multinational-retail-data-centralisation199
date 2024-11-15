"Task1:"

SELECT country_code,
       COUNT(*) as total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY
    total_no_stores DESC;

"Task2:"
SELECT locality, 
       COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

"Task3:"
SELECT dt.month,
       SUM(ot.product_quantity*dp.product_price) AS total_sales
FROM orders_table ot
JOIN dim_products dp ON dp.product_code = ot.product_code
JOIN dim_date_times dt ON dt.date_uuid = ot.date_uuid
GROUP BY dt.month
ORDER BY total_sales DESC
LIMIT 6;

"Task 4:"

SELECT 
    COUNT(*) AS numbers_of_sales,
    SUM(ot.product_quantity) AS product_quantity_count,
    CASE 
        WHEN ds.store_type IN ('Web Portal') THEN 'Online'
        ELSE 'Offline'
    END AS location
FROM 
    orders_table ot
JOIN 
    dim_store_details ds ON ot.store_code = ds.store_code
GROUP BY 
    location
ORDER BY 
    numbers_of_sales DESC;

"Task 5:"

SELECT ds.store_type,
       SUM(ot.product_quantity*dp.product_price) as total_sales,
	   round((SUM(ot.product_quantity * dp.product_price) * 100.0 / 
      SUM(SUM(ot.product_quantity * dp.product_price)) OVER ()),2) AS sales_made
FROM orders_table ot
JOIN dim_store_details ds ON ds.store_code=ot.store_code
JOIN dim_products dp ON dp.product_code = ot.product_code
GROUP BY store_type
ORDER BY total_sales DESC;

"Task 6:"

SELECT SUM(ot.product_quantity*dp.product_price) AS total_sales,
       dt.year,
	   dt.month	   
FROM orders_table ot
JOIN dim_products dp ON dp.product_code = ot.product_code
JOIN dim_date_times dt ON dt.date_uuid = ot.date_uuid
GROUP BY dt.month,dt.year
ORDER BY total_sales DESC
LIMIT 10;

"Task 7:"
SELECT 
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM dim_store_details
GROUP BY 
    country_code
ORDER BY 
    total_staff_numbers DESC;

"Task 8:"
SELECT SUM(ot.product_quantity*dp.product_price) AS total_sales,
       ds.store_type,
       ds.country_code       
FROM orders_table ot
JOIN dim_store_details ds ON ds.store_code = ot.store_code
JOIN dim_products dp ON dp.product_code = ot.product_code
WHERE ds.country_code = 'DE'
GROUP BY ds.store_type,ds.country_code
ORDER BY total_sales;

"Task9"

WITH sales_with_next AS (
    SELECT 
        ot.date_uuid,
        dt.year,
        -- Construct the full timestamp from year, month, day, and time
        TO_TIMESTAMP(dt.year || '-' || LPAD(dt.month::text, 2, '0') || '-' || LPAD(dt.day::text, 2, '0') || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp,
        LEAD(
            TO_TIMESTAMP(dt.year || '-' || LPAD(dt.month::text, 2, '0') || '-' || LPAD(dt.day::text, 2, '0') || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS')
        ) OVER (PARTITION BY dt.year ORDER BY dt.year, dt.month, dt.day, dt.timestamp) AS next_timestamp
    FROM orders_table ot
    JOIN dim_date_times dt ON dt.date_uuid = ot.date_uuid
),
time_differences AS (
    SELECT 
        year,
        AVG(EXTRACT(EPOCH FROM next_timestamp) - EXTRACT(EPOCH FROM timestamp)) AS time_diff_seconds
    FROM sales_with_next
    WHERE next_timestamp IS NOT NULL
    GROUP BY year
)
SELECT 
    year,
    CONCAT(
        '"hours": ', FLOOR(time_diff_seconds / 3600), ', ',
        '"minutes": ', FLOOR((time_diff_seconds % 3600) / 60), ', ',
        '"seconds": ', FLOOR(time_diff_seconds % 60), ', ',
        '"millise...": ', ROUND((time_diff_seconds * 1000) % 1000)
    ) AS actual_time_taken
FROM time_differences
ORDER BY year DESC;
