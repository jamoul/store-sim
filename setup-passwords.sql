/*
CS 121 Final Project
Part E
Jonathan Moul, Khanh Pham

Password and security setup
*/

-- Create the database if it doesn't exist (since we run this first)
CREATE DATABASE IF NOT EXISTS storedb;
USE storedb;


-- Drop things if they exist
DROP FUNCTION IF EXISTS make_salt;
DROP TABLE IF EXISTS user_info;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP FUNCTION IF EXISTS authenticate;


-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT) 
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Provided (you may modify if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you 
-- have admin or other roles for users in your application 
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL,
	
	is_admin TINYINT NOT NULL 
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(
    new_username VARCHAR(20), 
    password VARCHAR(20),
    is_admin TINYINT
)
BEGIN
  DECLARE salt CHAR(8);
  DECLARE pw_hash BINARY(64);
  SET salt = make_salt(8);
  SET pw_hash  = SHA2(CONCAT(salt, password), 256);
  INSERT INTO user_info
  VALUES (new_username, salt, pw_hash, is_admin);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(
    claimed_name VARCHAR(20), 
    claimed_password VARCHAR(20),
    claimed_admin TINYINT
)
RETURNS TINYINT DETERMINISTIC
BEGIN
  DECLARE username_exist TINYINT;
  DECLARE ex_salt CHAR(8);
  DECLARE pw_hash BINARY(64);
  DECLARE check_hash TINYINT;
  DECLARE admin_check TINYINT;
  
  SELECT COUNT(username) INTO username_exist
  FROM user_info 
  WHERE username = claimed_name
  AND is_admin = claimed_admin;
  IF (username_exist = 0) THEN
    RETURN 0;
  END IF;
  
  
  SELECT salt INTO ex_salt
  FROM user_info 
  WHERE username = claimed_name;
  
  SET pw_hash  = SHA2(CONCAT(ex_salt, claimed_password), 256);
  
  
  SELECT COUNT(username) INTO check_hash
  FROM user_info 
  WHERE username = claimed_name AND
  password_hash IN (
        SELECT SHA2(concat(ex_salt, claimed_password), 256)
  );

  RETURN check_hash;
  -- TODO
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
CALL sp_add_user('ManagerJeff', 'ILoveMyWife', 1);
CALL sp_add_user('Luis55', 'f1forlyfe', 0);
CALL sp_add_user('BellasComputer', 'p4ckersf4n', 0);


-- [Problem 1d]
-- Optional: Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
