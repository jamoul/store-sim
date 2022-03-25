/*
CS 121 Final Project
Part D
Jonathan Moul, Khanh Pham

Load data into tables
*/

-- Load products into products table
INSERT INTO products(price, name, product_desc, inventory, category) VALUES
    (4.99, 'Red Onion', 'Whole red onion', 54, 'grocery'),
    (5.99, 'Vidalia Onion', 'Whole Vidalia onion', 45, 'grocery'),
    (8.99, 'Hummus', 'Fresh garlic hummus, 16 oz', 25, 'grocery'),
    (8.99, 'Chicken Breast', '1/4 lb chicken breast', 20, 'grocery'),
    (4.99, 'Fortunate Trinkets Cereal', '32 oz Fortunate Trinkets cereal',
        20, 'grocery'),
    (10.99, 'Hoisin Sauce', '12 oz Hoisin sauce', 14, 'grocery'),
    (6.99, 'Extra Firm Tofu', '12 oz extra firm organic tofu', 18, 'grocery'),
    (3.99, 'Whole Wheat Bread', 'Whole loaf of whole wheat bread', 35,
        'grocery'),
    (6.99, 'Dozen Eggs', 'One dozen AAA eggs', 28, 'grocery'),
    (5.99, 'Dr. Pepper', '2 liter Dr. Pepper', 50, 'grocery'),
    (7.99, 'Artichoke', 'Whole raw organic artichoke', 16, 'grocery'),
    (6.99, 'Rutabaga', 'Fresh whole rutabaga', 5, 'grocery'),
    (27.99, 'Salmon', 'Fresh wild Alaska salmon', 7, 'grocery'),
    (14.99, 'Watermelon', 'Whole fresh watermelon', 34, 'grocery'),
    
    (24.99, 'Gray Throw Pillow', '24x24 inch gray throw pillow', 15, 'home'),
    (16.99, 'Spongebob plush', '79 inch Spongebob plush', 24, 'home'),
    (11.99, 'Silver doorknob', 'Silver-colored doorknob', 13, 'home'),
    (15.99, 'Yellow dish towel', '8x24 inch yellow dish towel', 27, 'home'),
    (7.99, 'BTS Fan Poster', '4x6 foot BTS fan poster', 7, 'home'),
    (49.99, 'Roomba', 'Roomba vacuum robot', 49, 'home'),
    (14.99, 'Live Laugh Love Welcome Mat', 
        '24x48 inch Live Laugh Love welcome mat', 12, 'home'),
    (5.99, 'Spatula', 'Large plastic spatula', 29, 'home'),
    (5.99, 'Onion Storage Pod', 'Plastic onion storage pod', 17, 'home'),
    (7.99, 'Hammer', 'Steel hammer with plastic handle', 22, 'home'),
    
    (299.99, 'iPhone 6s', 'New iPhone 6s with bigger screen', 34, 
        'electronics'),
    (799.99, 'Samsung 72 inch TV', '72 inch plasma HDTV', 6, 'electronics'),
    (16.99, 'Wireless mouse', 'Wireless battery powered mouse', 11, 
        'electronics'),
    (299.99, 'Nintendo Switch', 'Nintendo Switch console with 2 controllers',
        19, 'electronics'),
    (5.99, 'USB to MicroUSB cable', '30 inch USB to MicroUSB cable', 15, 
        'electronics'),
    (49.99, 'Google Home Mini', 'Google Home Mini assistant', 16, 
        'electronics'),
    (49.99, 'Digital Camera', 'Waterproof digital camera', 17, 'electronics'),
    (19.99, '20 ft Extension Cord', '20 ft female-male exension cord',
        29, 'electronics'),
    
    (3.99, 'Paper Towels', '200 ct roll of paper towels', 56, 'hygeine'),
    (8.99, 'Mint Toothpaste', '8 oz mint toothpaste tube', 40, 'hygeine'),
    (12.99, 'Womens Deodorant', 'Unscented womens deodorant stick', 20,
        'hygeine'),
    (2.99, 'Dental Floss', '200 ft mint dental floss', 30, 'hygeine'),
    (5.99, 'Comb', 'Fine toothed 4 inch comb', 14, 'hygeine'),
    (24.99, 'Razor 3pk', '3pk triple-blade faical razor', 16, 
        'hygeine'),
    (5.99, 'Facial Tissue', '100 ct 1-ply facial tissue box', 33, 'hygeine'),
    (16.99, 'Bar soap 8pk', '8pk unscented shower bar soap', 20, 'hygeine');


-- Load some purchases into the purchases table
INSERT INTO purchases(username, purchase_ts) VALUES
    ('Luis55', DATE_SUB(NOW(), INTERVAL 30 DAY)),
    ('BellasComputer', DATE_SUB(NOW(), INTERVAL 13 DAY)),
    ('Luis55', DATE_SUB(NOW(), INTERVAL 2 HOUR));


-- Add what was purchased in the above purchases
INSERT INTO bought(purchase_id, product_id, bought_quantity, bought_price) 
    VALUES
    (1, 2, 2, 5.99),
    (1, 3, 1, 8.99),
    (1, 8, 1, 3.99),
    (1, 9, 2, 6.99),
    (2, 12, 5, 14.99),
    (2, 16, 1, 49.99),
    (2, 20, 1, 7.99),
    (3, 23, 1, 16.99),
    (3, 34, 1, 24.99);
