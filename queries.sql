-- out of stock
SELECT * 
FROM products 
WHERE inventory = 0;

-- low on stock
SELECT * 
FROM products 
WHERE inventory < 5;

-- make into function
SELECT * 
FROM products 
WHERE category = 'electronics' 
    AND price BETWEEN 20.00 AND 100.00;

-- view a purchase detail
SELECT name, bought_quantity, bought_price 
FROM bought NATURAL JOIN products 
WHERE purchase_id = 2;

/*
-- make a materialized view
CREATE VIEW purchase_info AS
  SELECT 
    purchase_id,
	purchase ts,
    total  
  FROM mv_branch_account_stats;
*/

-- view all purchases in descending order of total spent
SELECT purchase_id, SUM(bought_price * bought_quantity) AS total_spend 
FROM bought NATURAL JOIN purchases  
GROUP BY purchase_id
ORDER BY total_spend DESC;

/*
-- view product IDs and quantities in a single account's cart
SELECT * FROM cart WHERE username = 'Luis55';
*/

-- view names, prices, and quantities in a single account's cart
SELECT name, price, quantity 
FROM cart NATURAL LEFT JOIN products 
WHERE username = 'Luis55';


-- total revenue for the month
SELECT SUM(bought_price * bought_quantity) AS month_revenue
FROM bought JOIN purchases USING (purchase_id)
WHERE purchase_ts > DATE_SUB(NOW(), INTERVAL 1 MONTH);