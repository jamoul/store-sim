/*
CS 121 Final Project
Part F
Jonathan Moul, Khanh Pham

Create users and grant permissions for online store simulation application
*/

-- Create client and admin users
CREATE USER IF NOT EXISTS 'storeadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER IF NOT EXISTS 'storeclient'@'localhost' IDENTIFIED BY 'clientpw';

-- Grant all permissions to the admin
GRANT ALL PRIVILEGES ON *.* TO 'storeadmin'@'localhost';

-- Grant relevant permissions to the client
GRANT SELECT ON storedb.* TO 'storeclient'@'localhost';
GRANT EXECUTE ON FUNCTION storedb.authenticate TO 'storeclient'@'localhost';
GRANT EXECUTE ON PROCEDURE storedb.add_to_cart TO 'storeclient'@'localhost';
GRANT EXECUTE ON PROCEDURE storedb.delete_from_cart 
    TO 'storeclient'@'localhost';
GRANT EXECUTE ON PROCEDURE storedb.check_out TO 'storeclient'@'localhost';