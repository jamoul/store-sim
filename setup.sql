/*
CS 121 Final Project
Part B
Jonathan Moul, Khanh Pham

DDL and database setup
*/

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS storedb;
USE storedb;

-- Drop tables if they exist
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS bought;
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS products;

-- products: Info about the store's products
CREATE TABLE products (
    -- unique identifier for products
    product_id    INT AUTO_INCREMENT, 
    -- price of a single unit of this product
    price         NUMERIC(5,2) NOT NULL,
    -- product name
    name          VARCHAR(50) NOT NULL, 
    -- short description of the product
    product_desc  TEXT NOT NULL, 
    -- number of units of this product in stock
    inventory     INT NOT NULL, 
    -- type of product (e.g. grocery, electronics)
    category      VARCHAR(20) NOT NULL,
    PRIMARY KEY (product_id),
    -- ensure that inventory and price make sense
    CHECK (inventory >= 0),
    CHECK (price > 0)
);
-- Create an index on product category for quick recall
CREATE INDEX prod_cat ON products (category);

-- purchases: Info about purchases by customers. One purchase is the
-- simultaneous buying of at least one product by a single user.
CREATE TABLE purchases (
    -- unique identifier for purchases
    purchase_id     INT AUTO_INCREMENT NOT NULL,
    -- username of the user who made the purchase
    username        VARCHAR(20) NOT NULL, 
    -- timestamp of the purchase
    purchase_ts     TIMESTAMP NOT NULL,
    PRIMARY KEY (purchase_id),
    -- username must be a recognized user for the app
    FOREIGN KEY (username) REFERENCES user_info(username)
);

-- bought: Info about which products were bought in which purchases.
CREATE TABLE bought (
    -- unique identifier for purchases (from purchases table)
    purchase_id       INT,
    -- unique identifier for products (from products table)
    product_id        INT,
    -- unit price at which the product was bought
    bought_price      NUMERIC(5,2) NOT NULL,
    -- quantity of the given product that was purchased in the transaction
    bought_quantity   INT NOT NULL,
    PRIMARY KEY (purchase_id, product_id),
    -- must be a recognized purchase
    FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id),
    -- must be a recognized product
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    -- quantity and price must make sense
    CHECK (bought_quantity > 0),
    CHECK (bought_price >= 0)
);

-- cart: Info about which products are in the cart of various users
CREATE TABLE cart (
    -- unique identifier for users
    username VARCHAR(20) NOT NULL,
    -- unique identifier for products (from products table)
    product_id INT NOT NULL, 
    -- quantity of product in the user's cart
    quantity INT NOT NULL,
    PRIMARY KEY (username, product_id),
    -- username must be a recognized user
    FOREIGN KEY (username) REFERENCES user_info(username),
    -- product_id must be a recognized product
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    -- there must be a nonzero amount in the cart
    CHECK (quantity > 0)
);

