/*
CS 121 Final Project
Part I
Jonathan Moul, Khanh Pham

Functions, stored routines, and triggers
*/

-- Drop functions, procedures, triggers if they exist
DROP FUNCTION IF EXISTS cart_cost;
DROP PROCEDURE IF EXISTS add_to_cart;
DROP PROCEDURE IF EXISTS delete_from_cart;
DROP PROCEDURE IF EXISTS check_out;
DROP PROCEDURE IF EXISTS update_product;
DROP PROCEDURE IF EXISTS inventory_chg;
DROP TRIGGER IF EXISTS purchase_insert_tr;

-- Functions:

-- cart_cost(): Get the total cost of the items in the cart
DELIMITER !
CREATE FUNCTION cart_cost(curr_user VARCHAR(20)) RETURNS NUMERIC(5,2) 
    DETERMINISTIC
BEGIN
    -- declare a variable to hold the total cost
    DECLARE total_cost NUMERIC(5,2);
    
    -- calculate and save the total cost of the items in the cart
    SELECT COALESCE(SUM(price * quantity), 0) INTO total_cost
    FROM cart JOIN products USING (product_id)
    WHERE username = curr_user;
    
    -- return the total cost
    RETURN total_cost;
END
!
DELIMITER ;


-- Procedures:


-- add_to_cart(): Moves an item to the cart
DELIMITER !
CREATE PROCEDURE add_to_cart(
    curr_user   VARCHAR(20),
    item_id     INT,
    item_qty    INT
)
BEGIN
    -- If the item is not already in the cart, add it
    DECLARE check_in TINYINT;
    SELECT COUNT(*) INTO check_in
    FROM cart 
    WHERE product_id = item_id
        AND username = curr_user;
    IF check_in = 0 THEN
        INSERT INTO cart VALUES (curr_user, item_id, item_qty);
    -- Otherwise, update the number of this item in the cart
    ELSE
        UPDATE cart
        SET quantity = quantity + item_qty
        WHERE username = curr_user
            AND product_id = item_id;
    END IF;
END
!
DELIMITER ;


-- delete_from_cart(): Removes an item completely from the cart
DELIMITER !
CREATE PROCEDURE delete_from_cart(
    curr_user   VARCHAR(20),
    item_id     INT
)
BEGIN
    -- Remove all of the specified item
    DELETE FROM cart
    WHERE username = curr_user
        AND product_id = item_id;
END
!
DELIMITER ;


-- check_out(): Purchases items in the cart. This includes updating the
-- purchases and bought tables, as well as deleting the purchased items
-- from the cart. This procedure does not update the inventory of the
-- purchased items, as this is left to the purchase_insert_tr trigger
-- on the bought table.
DELIMITER !
CREATE PROCEDURE check_out(
    curr_user VARCHAR(20)
)
BEGIN
    -- Declare variables
    DECLARE curr_pur_id INT;
    
    -- Record this purchase
    INSERT INTO purchases(username, purchase_ts) VALUES(curr_user, NOW());
    -- Get the ID of this purchase
    SET curr_pur_id = (SELECT MAX(purchase_id) FROM purchases);
    
    -- Record the items purchased in this purchase
    INSERT INTO bought(purchase_id, product_id, bought_quantity, bought_price)
        SELECT curr_pur_id, product_id, quantity, 0.00
        FROM cart;
    
    -- Update the prices in the new rows in bought
    
    UPDATE bought AS b, products AS p
    SET b.bought_price = p.price
    WHERE p.product_id = b.product_id
        AND b.purchase_id = curr_pur_id;
    
    
    -- Delete the purchased items from the cart
    DELETE FROM cart
    WHERE username = curr_user;
END
!
DELIMITER ;


-- update_product(): Changes the price or inventory of the given product.
DELIMITER !
CREATE PROCEDURE update_product (
    curr_id         INT,
    new_price       NUMERIC(5,2),
    new_inventory   INT
)
BEGIN
    -- Update the product price and inventory
    UPDATE products
    SET price = new_price, inventory = new_inventory
    WHERE product_id = curr_id;
END
!
DELIMITER ;


-- inventory_chg(): Changes the inventory of an item by the given amount.
DELIMITER !
CREATE PROCEDURE inventory_chg (
    curr_id INT,
    num_chg INT
)
BEGIN
    -- Update the product inventory
    UPDATE products
    SET inventory = inventory + num_chg
    WHERE product_id = curr_id;
END
!
DELIMITER ;


-- Triggers:


-- purchase_insert: Automatically updates the inventory of an item in the
-- products table when the product is purchased (i.e. added to the bought
-- table).
DELIMITER !
CREATE TRIGGER purchase_insert_tr AFTER INSERT
    ON bought FOR EACH ROW
BEGIN
    CALL inventory_chg(NEW.product_id, -1 * NEW.bought_quantity);
END
!
DELIMITER ;