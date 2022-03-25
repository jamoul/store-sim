"""
CS 121 Final Project
Part J
Jonathan Moul, Khanh Pham

Command-line Application Online Store Simulation
"""

"""
This application simulates the function of an online store, with users able
to view items. Customers can view items, add items to cart or remove them,
or check out their cart to purchase items. Administrators may view customer
activities or adjust item inventory or prices.
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = False


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------

# Get connection to the database with client privileges
def get_conn():
    """"
    Returns a connected MySQL connector instance with client privileges, 
    if connection is successful. If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='storeclient',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='clientpw',
          database='storedb'
        )
        print('Connected to database.')
        return conn
    except mysql.connector.Error as err:
        # In case of database connection error
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            print('Incorrect username or password when connecting to DB.', 
                file = sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            print('Database does not exist.', file = sys.stderr)
        elif DEBUG:
            print(err, file = sys.stderr)
        else:
            print('An error occurred, please contact the administrator.', 
                file = sys.stderr)
        sys.exit(1)


# Get connection to the database with admin privileges
def get_admin_conn():
    """"
    Returns a connected MySQL connector instance with admin privileges, 
    if connection is successful. If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='storeadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='adminpw',
          database='storedb'
        )
        print('Connected to database.')
        return conn
    except mysql.connector.Error as err:
        # In case of database connection error
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            print('Incorrect username or password when connecting to DB.',
                file = sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            print('Database does not exist.', file = sys.stderr)
        elif DEBUG:
            print(err, file = sys.stderr)
        else:
            print('An error occurred, please contact the administrator.',
                file = sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def example_query():
    param1 = ''
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    sql = 'RE col2 = \'%s\';' % (param1, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            # do stuff with row data
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('An error occurred, give something useful for clients...',
                file = sys.stderr)


# Get the name, inventory, and price of an item by id
def item_id_facts(curr_id):
    '''
    Returns the name, inventory, and price of the item with the
    given id.
    '''
    param1 = curr_id
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    sql = 'SELECT * FROM products WHERE product_id = %s;' % (param1, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (product_id, price, name, product_desc, inventory, category) = (row) # tuple unpacking!
            return product_id, price, name, product_desc, inventory, category
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to fetch item info.', file = sys.stderr)


# get the items that are out of stock
def check_stock(upper = '500000', lower = '0'):
    '''
    Returns a list of items where inventory is zero.
    '''
    cursor = conn.cursor()
    sql = ('SELECT * FROM products WHERE inventory BETWEEN %s AND %s;'
        % (lower, upper ))
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        items = cursor.fetchall()
        for i in items:
            (product_id, price, name, product_desc, inventory, category) = (i)
            print(product_id, name,'x', inventory) 
    # In case of error connecting to the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to fetch items.', file = sys.stderr)


# Alter the price and inventory of an item
def item_chg(item_id, new_price, new_inventory):
    '''
    Assigns the given item the given price and inventory.
    '''
    param1 = item_id
    param2 = new_price
    param3 = new_inventory
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    sql = 'CALL update_product(%s, %s, %s);' % (param1, param2, param3, )
    try:
        cursor_result = cursor.execute(sql)
        conn.commit()
        '''
        rows = cursor.fetchall()
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            # I don't think we actually need to do any of this here
        '''
    # In case of error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Item update failed.', file = sys.stderr)


# Print customer purchase history.
def pur_history(cust = None):
    '''
    Prints the purchase history of the given customer over the past 14 days.
    If no customer is specified, prints the purchase history of all customers
    over that period.
    '''
    param1 = cust
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    # If we are getting history for all customers
    if cust is None:
        sql = ('SELECT purchase_id, username, purchase_ts, SUM(bought_price) as tot_price '
        + 'FROM purchases JOIN bought USING (purchase_id) '
        + 'WHERE purchase_ts > DATE_SUB(NOW(), INTERVAL 14 DAY) '
        + 'GROUP BY purchase_id;')
    # If we are getting history for a specific customer
    else:
        sql = ('SELECT purchase_id, purchase_ts, SUM(bought_price) as tot_price '
        + 'FROM purchases JOIN bought USING (purchase_id) '
        + 'WHERE purchase_ts > DATE_SUB(NOW(), INTERVAL 14 DAY) '
        + 'AND username = \'%s\' ' % (cust, )
        + 'GROUP BY purchase_id;')
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            # Print the purchase history, with customer name if we are viewing
            # the history of multiple customers
            if cust is None:
                (purchase_id, curr_cust, purchase_ts, tot_price) = (row)
                print(purchase_id, curr_cust, purchase_ts, tot_price)
            else:
                (purchase_id, purchase_ts, tot_price) = (row)
                print(purchase_id, purchase_ts, tot_price)
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to display purchase history.', file = sys.stderr)

def search_products(category, lower_price, upper_price):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT * FROM products WHERE category IN (\'%s\') AND price BETWEEN %s AND %s;' % (category, lower_price, upper_price)
    try:
        cursor.execute(sql)
        products = cursor.fetchall()
        for p in products:
            (product_id, price, name, product_desc, inventory, category) = (p)
            print(product_id, name, '          $', price, 'x', inventory)       
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('An error occurred,  couldn\'t serach for items',
                file = sys.stderr)

# Print cart contents.
def show_cart(cust = None):
    '''
    Prints the contents of the given customer's cart. If no customer is 
    specified, prints the current contents of every customer's cart.
    '''
    param1 = cust
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    # If we are showing the contents of all customers' carts
    if cust is None:
        sql = ('SELECT username, product_id, name, quantity FROM cart '
        + 'JOIN products USING (product_id);')
    # If we are showing the contents of a specific customer's cart
    else:
        sql = ('SELECT product_id, name, quantity FROM cart NATURAL '
        + 'LEFT JOIN products '
        + 'WHERE username = \'%s\';' % (param1))
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
        for row in rows:
            # Return the contents of the cart, with customer names if we are
            # looking at the carts of multiple customers
            if cust is None:
                (username, p_id, name, qty) = (row)
                print(username, p_id, name, qty)
            else:
                (p_id, name, qty) = (row) # tuple unpacking!
                print(p_id, name, qty)
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to display cart.', file = sys.stderr)


# Add the given item and quantity to the cart.
def add_cart(cust, p_id, qty):
    '''
    Adds the given amount of the given item to the given customer's cart.
    '''
    param1 = cust
    param2 = p_id
    param3 = qty
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    # Call the add_to_cart procedure to add to the cart.
    sql = 'add_to_cart'
    try:
        cursor.callproc(sql, [param1, param2, param3])
        conn.commit()
        '''
        rows = cursor.fetchall()
        for row in rows:
            if cust is None:
                (username, product_id, name, quantity) = (row)
                print(username, product_id, name, quantity)
            else:
                (product_id, name, quantity) = (row) # tuple unpacking!
                print(product_id, name, quantity)
        '''
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to add item to cart.', file = sys.stderr)


# Remove the given item from the cart.
def remove_cart(cust, p_id):
    '''
    Removes all of the given item from the given customer's cart.
    '''
    param1 = cust
    param2 = p_id
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # Call the delete_from_cart procedure to delete from the cart.
    sql = 'CALL delete_from_cart(\'%s\', %s);' % (param1, param2, )
    try:
        cursor_result = cursor.execute(sql)
        conn.commit()
        # TODO: What if the given item is not in the cart?

        '''
        rows = cursor.fetchall()
        for row in rows:
            if cust is None:
                (username, p_id, name, qty) = (row)
                print(username, p_id, name, qty)
            else:
                (p_id, name, qty) = (row) # tuple unpacking!
                print(p_id, name, qty)
        '''
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to remove item from cart.', file = sys.stderr)


# Purchase the current cart contents.
def check_out_cart(cust):
    '''
    Purchases the given customer's cart.
    '''
    param1 = cust
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.
    # TODO: What if the customer tries to check out too many of an item?

    # Call the check_out procedure to check out the cart.
    sql = 'CALL check_out(\'%s\');' % (param1, )
    try:
        cursor_result = cursor.execute(sql)
        conn.commit()
        # TODO: What if the given item is not in the cart?

        '''
        rows = cursor.fetchall()
        for row in rows:
            if cust is None:
                (username, p_id, name, qty) = (row)
                print(username, p_id, name, qty)
            else:
                (p_id, name, qty) = (row) # tuple unpacking!
                print(p_id, name, qty)
        '''
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to check out cart.', file = sys.stderr)


# Add a new account.
def add_account(new_user, new_pw, new_admin = 0):
    '''
    Queries the database to add the given account to the app.
    '''
    param1 = new_user
    param2 = new_pw
    param3 = new_admin
    cursor = conn.cursor()
    # Pass arguments as a tuple like so to prevent SQL injection.

    # Call the sp_add_user function to add a new user.
    sql = 'CALL sp_add_user(\'%s\', \'%s\', %s);' % (param1, param2, param3, )
    try:
        cursor_result = cursor.execute(sql)
        conn.commit()
        '''
        rows = cursor.fetchall()
        for row in rows:
            if cust is None:
                (username, p_id, name, qty) = (row)
                print(username, p_id, name, qty)
            else:
                (p_id, name, qty) = (row) # tuple unpacking!
                print(p_id, name, qty)
        '''
        return 1
    # If there is an error communicating with the database
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('Unable to add user.', file = sys.stderr)
        return 0


# -------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------


# Login a user
def login_user(curr_user, password, user_type):
    '''
    Logs in a user of the given user_type (0 = client, 1 = admin). If
    the user does not exist or is of the wrong type, gives an error.
    '''
    param1 = curr_user
    param2 = password
    param3 = user_type
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT authenticate(\'%s\', \'%s\', %s);' % (param1, param2, param3, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == 1:
                return 1
            else:
                print('Wrong username or password.', file = sys.stderr)
                return 0
    except mysql.connector.Error as err:
        if DEBUG:
            print(err, file = sys.stderr)
            sys.exit(1)
        else:
            print('User authentication failed.', file = sys.stderr)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------


# Login options
def login_options():
    '''
    Displays options for a user to log in as an administrator or client.
    '''
    print('What would you like to do? ')
    print('  (c) - login as customer')
    print('  (a) - login as administrator')
    print('  (n) - register a new account')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    global conn
    global username
    # If the user wants to log in
    if ans == 'c' or ans == 'a':
        username = input('Enter username: ')
        password = input('Enter password: ')
        if ans == 'c':
            # Get a connection of the correct type and try to log in
            conn = get_admin_conn()
            authenticated = login_user(username, password, 0)
            # If there is no error, go to the client options page
            if authenticated:
                print()
                show_options()
            else:
                print()
                login_options()
        elif ans == 'a':
            # Get a connection of the correct type and try to log in
            conn = get_admin_conn()
            authenticated = login_user(username, password, 1)
            # If there is no error, go to the admin options page
            if authenticated:
                show_admin_options()
            else:
                print()
                login_options()
    elif ans == 'n':
        # Get a connection and create a new account
        username = input('Enter username for new account: ')
        password = input('Enter password for new account: ')
        conn = get_admin_conn()
        # Add a new user
        succ = add_account(username, password)
        if succ:
            print('Account successfully added.')
            print('Welcome user %s!' % username)
            print()
            show_options()
        else:
            print('Account creation unsuccessful.')
            print('Returning to login menu.')
            print()
            login_options()
        
    elif ans == 'q':
        # Leave the UI
        quit_ui()
    else:
        print('Command not recognized.')
        print()
        login_options()


# Client option menu
def show_options():
    """
    Displays options client users can choose in the application, such as
    searching for a product or viewing their cart or recent purchase history.
    """
    print('What would you like to do? ')
    print('  (f) - Find product')
    print('  (c) - view cart')
    print('  (p) - view recent purchase history')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        # Leave the UI
        quit_ui()
    elif ans == 'p':
        # View recent purchases
        print('Showing recent purchase history for %s:' % username)
        print()
        pur_history(username)
        print()
        show_options()
    elif ans == 'c':
        # Show the client's cart
        print('Showing cart contents for %s:' % username)
        curr_cart = show_cart(username)
        if curr_cart is None:
            print('Your cart is empty.')
        else:
            for cart_row in curr_cart:
                print(cart_row)
        print()
        cart_options()
    elif ans == 'f':
        # Go to the search options menu
        print()
        search_options()
    else:
        print('Command not recongized.')
        print()
        show_options()


# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as managing customer accounts,
    viewing the carts or purchase histories of customers, or adjusting the
    prices or inventories of items.
    """
    print('What would you like to do? ')
    print('  (m) - manage accounts')
    print('  (c) - view customer cart contents')
    print('  (p) - view recent customer purchases')
    print('  (i) - adjust item price or inventory')
    print('  (n) - check inventory')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        # Leave the UI
        quit_ui()
    elif ans == 'i':
        prod_id = input('Enter product id: ')
        if prod_id == '':
            show_admin_options()
        print(item_id_facts(prod_id))
        # TODO: What if the given id doesn't match any items?

        # Check if this is the correct item
        ans = input('Is this the desired item? [y/n] ').lower()
        if ans == 'y':
            new_inventory = input('Enter desired inventory: ')
            new_price = input('Enter desired price: ')
            item_chg(prod_id, new_price, new_inventory)
            print('Item successfully updated. Returning to menu.')
            print()
            show_admin_options()
        elif ans == 'n':
            print('Returning to menu.')
            print()
            show_admin_options()
        else:
            print('Command not recognized.')
            print()
            show_admin_options()
    elif ans == 'p':
        # View recent purchases for all customers
        print('Showing recent purchase history for all customers:')
        print()
        pur_history()
        print()
        show_admin_options()
    elif ans == 'c':
        # View cart contents for all customers
        print('Showing current cart contents for all customers:')
        curr_cart = show_cart()
        if curr_cart is None:
            print('All customer carts are empty.')
        else:
            for cart_row in curr_cart:
                print(cart_row)
        print()
        show_admin_options()
    elif ans == 'm':
        print()
        manage_options()
    elif ans == 'n':
        print()
        inventory_options()
    else:
        print('Command not recognized.')
        print()
        show_admin_options()

def inventory_options():
    print('What would you like to do? ')
    print('  (o) - out of stock')
    print('  (i) - in stock')
    print('  (l) - low stock')
    print('  (s) - search by stock')
    print('  (m) - main menu')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'o':
        check_stock(upper = '0')
        inventory_options()
        print()
    elif ans == 'i':
        check_stock(lower = '1')
        inventory_options()
        print()
    elif ans == 'l':
        check_stock(upper = '5')
        inventory_options()
        print()
    elif ans == 's':
        print('Search by stock. Press enter to skip')
        u = input('Less than x units: ')
        if u == '': 
            u = '500000'
        l = input('More than x units: ')
        if l == '': 
            l = '0'
        print()
        check_stock(upper = u, lower = l)
        print()
        inventory_options()
    elif ans == 'm':
        print()
        show_admin_options()
    else:
        print('Command not recognized')
        print()
        inventory_options()


# Cart options for clients
def cart_options():
    '''
    Displays options for a client to view and edit their cart or to purchase items.
    '''
    print('What would you like to do? ')
    print('  (v) - view cart contents')
    print('  (a) - add item to cart')
    print('  (r) - remove item from cart')
    print('  (c) - check out cart')
    print('  (m) - back to main menu')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'v':
        curr_cart = show_cart(username)
        if curr_cart is None:
            print('Your cart is empty.')
        else:
            for cart_row in curr_cart:
                print(cart_row)
        print()
        cart_options()
    elif ans == 'a':
        prod_id = input('Enter product id: ')
        # name, inventory, price = item_id_facts(prod_id)
        curr_facts = item_id_facts(prod_id)
        if curr_facts is None:
            print('No item found.')
            print()
            cart_options()
        print(item_id_facts(prod_id))
        # What if the id doesn't match any item? Handle this case later

        # Check if this is the correct item
        ans = input('Is this the desired item? [y/n] ').lower()
        if ans == 'y':
            num_add = input('Enter number to add to cart: ')
            add_cart(username, prod_id, num_add)
            print('Item successfully added to cart. Returning to cart menu.')
            print()
        elif ans == 'n':
            print('Returning to cart menu.')
        print()
        cart_options()
    if ans == 'r':
        prod_id = input('Enter product id: ')
        # name, inventory, price = item_id_facts(prod_id)
        print(item_id_facts(prod_id))
        # What if the id doesn't match any item? Handle this case later

        # Check if this is the correct item
        ans = input('Is this the desired item? [y/n] ').lower()
        if ans == 'y':
            remove_cart(username, prod_id)
            print('Item successfully removed from cart. Returning to cart menu.')
            print()
        elif ans == 'n':
            print('Returning to cart menu.')
        print()
        cart_options()
    elif ans == 'c':
        ans = input('Are you sure you want to check out? [y/n] ')
        if ans == 'y':
            check_out_cart(username)
            print('Successfully checked out cart. Returning to main menu.')
            print()
            show_options()
        else:
            print('Returning to cart menu.')
            print()
            cart_options()
    elif ans == 'm':
        print()
        show_options()
    else:
        print('Command not recognized.')
        print()
        cart_options()


# Search options for clients
def search_options():
    '''
    Displays options for a client to search for an item.
    '''
    print('What would you like to do? ')
    print('  (a) - show all items')
    print('  (x) - advanced search')
    print('  (m) - back to main menu')
    print()
    all_cat ='grocery\', \'home\', \'electronics\', \'hygeine'
    ans = input('Enter an option: ').lower()
    if ans == 'a':
        # TODO: 'grocery, home, electronics, hygeine'Displaying all items (dependent on display_products function)
        search_products(all_cat, '0', '99999.99')
        print()
        product_options()
    elif ans == 'x':
        print('Search by categories: grocery, home, electronics, hygeine. Press enter to skip')
        cat = input('Enter a category: ').lower()
        if cat == '': 
            cat = all_cat
        print('Search by price. Press enter to skip')
        up = input('Less than: $')
        if up == '': 
            up = '99999.99'
        lp = input('More than: $')
        if lp == '': 
            lp = '0.00'
        search_products(cat, lp, up)
        print()
        product_options()
    elif ans == 'm':
        print()
        show_options()
    else:
        print('Command not recognized.')
        print()
        search_options()

def product_options():
    print('What would you like to do? ')
    print('  (a) - add item to cart')
    print('  (v) - view item details')
    print('  (s) - back to search menu')
    ans = input('Enter an option: ').lower()
    if ans == 'a':
        prod_id = input('Enter product id: ')
        prod_id, price, name, product_desc, inventory, category = item_id_facts(prod_id)
        # What if the id doesn't match any item? Handle this case later

        # Check if this is the correct item
        ans = input('Is this the desired item? [y/n] ').lower()
        if ans == 'y':
            num_add = input('Enter number to add to cart: ')
            add_cart(username, prod_id, num_add)
            print('Item successfully added to cart. Returning to search menu.')
            print()
        elif ans == 'n':
            
            print('Returning to serch menu.')
        print()
        product_options()
    elif ans == 'v':
        prod_id = input('Enter product id: ')
        print(item_id_facts(prod_id))
        product_options()
    elif ans == 's':
        search_options()
    else:
        print('Command not recognized.')
        print()
        product_options()

# Account management options for admins
def manage_options():
    '''
    Displays options for managing client accounts for administrators.
    '''
    print('What would you like to do? ')
    print('  (a) - add an account')
    print('  (m) - back to main menu')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'a':
        new_user = input('Enter username for new user: ')
        new_pw = input('Enter password for new user: ')
        new_admin = input('Is the new user an admin? [y/n]')
        if new_admin[0] == 'y':
            new_admin = 1
        elif new_admin[9] == 'n':
            new_admin = 0
        else:
            print('Command not understood. Returning to user management menu.')
            print()
            manage_options()
        succ = add_account(new_user, new_pw, new_admin)
        if succ == 1:
            print('User %s successfully added. Returning to main menu.' 
                % new_user)
        else:
            print('Returning to menu.')
        print()
        show_admin_options()
    elif ans == 'm':
        show_admin_options()
    else:
        print('Command not recognized.')
        print()
        manage_options()



def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    conn.close()
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    login_options()
    

if __name__ == '__main__':
    main()


# Old main function (if we wish to remove login screen, go back to using this)
'''
def main():
    """
    Main function for starting things up.
    """
    show_options()
    

if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()

'''