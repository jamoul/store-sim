/*
SELECT COUNT(username)
    FROM user_info 
	WHERE username = 'ManagerJeff'
    AND is_admin = 1;


SELECT salt
    FROM user_info 
	WHERE username = 'ManagerJeff';


SELECT COUNT(username)
    FROM user_info 
	WHERE username = claimed_name AND
    password_hash = SHA2(CONCAT(salt, claimed_password), 256);
    
*/

SELECT * FROM user_info WHERE password_hash IN (SELECT SHA2(concat('`f`1tr_f', 'ILoveMyWife'), 256));