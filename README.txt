CS 121 Final Project
Part K: README
Jonathan Moul, Khanh Pham


INTRODUCTION:
This project is a command-line simulation of an online store interface. By navigating through the user interface and entering commands, users may simulate viewing and purchasing items if customers or viewing customer activity and setting item prices and inventories if administrators.

DATA SOURCE:
The data for this application is synthetic. It was generated from scratch for use in this project. All of the data is contained in the load-data.sql file. Entering the "source load-data.sql" statement as usual during setup suffices to populate all of the data in the correct tables.

RUNNING THE PROGRAM:
Command-line arguments are not supported with running the program. Once setup is complete, simply execute "python3 app.py" to enter the login menu.

In the login menu, users may create new customer accounts. Only administrators can create additional administrator accounts. To create an admin account for testing purposes, users can log into the existing admin account (username 'ManagerJeff', password 'ILoveMyWife').

SETUP INSTRUCTIONS:
To setup the program, call the following commands in the following order in the SQL command line:
1. 'source setup-passwords.sql;'
2. 'source setup.sql;'
3. 'source load-data.sql;'
4. 'source setup-routines.sql;'
5. 'source grant-permissions.sql;'
Then, the program can be started with 'python3 app.py' from the command line.