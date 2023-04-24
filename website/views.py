from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from src.db_connect import DbConnection
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    return redirect(url_for('views.index'))

@views.route('/login')
def login():
    return render_template('login.php')

@views.route('/register')
def register():
    return render_template('sign_up.php')

@views.route('/',
              methods=['GET', 'POST'])
def index():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)

    if request.method == 'POST':
        min_price = request.form.get('min-price')
        max_price = request.form.get('max-price')
        price_order = request.form.get('price')
        
        query = 'SELECT * FROM product WHERE Price >= %s AND Price <= %s'
        params = (min_price, max_price)

        if price_order == 'asc':
            query += ' ORDER BY Price ASC'
        elif price_order == 'desc':
            query += ' ORDER BY Price DESC'
        
        cursor.execute(query, params)
        products = cursor.fetchall()
    else:
        cursor.execute('SELECT * FROM product')
        products = cursor.fetchall()

    cursor.execute('SELECT DISTINCT Type FROM product')
    types = [row['Type'] for row in cursor.fetchall()]

    username = session.get('username')
    return render_template('base.php', products=products, types=types, username=username)


@views.route('/products')
def products():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    return render_template('products.php', products=products, category='All Products Available')

@views.route('/products_by_type/<string:type>')
def products_by_type(type):
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM product WHERE Type=%s', (type,))
    products = cursor.fetchall()
    return render_template('products.php', products=products, category=type)

@views.route('/search')
def search():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)

    # Get the search term from the query parameters
    search_term = request.args.get('q')

    # Build the SQL query to search for products
    sql = "SELECT * FROM product WHERE Name LIKE %s "
    search_term = f"%{search_term}%"
    cursor.execute(sql, (search_term,))

    # Fetch the search results
    products = cursor.fetchall()

    return render_template('search.php', products=products, search_term=search_term)

@views.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')

    if product_id:
        db_conn = DbConnection.get_instance()
        cursor = db_conn.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM product WHERE ID=%s', (product_id,))
        product = cursor.fetchone()
        if product:
            cart = session.get('cart')
            if cart is None:
                cart = []
            if isinstance(cart, dict):
                cart = list(cart.keys())  # Convert the cart from a dictionary to a list of product IDs
            cart.append(int(product_id))
            session['cart'] = cart
            # Get the current page URL and redirect to it
            return redirect(request.referrer)

    flash('Product not found', 'error')
    return redirect(url_for('views.index'))

@views.route('/cart')
def cart():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)

    product_ids = session.get('cart', [])
    quantities = {}  # dictionary to keep track of quantities of each product
    total_price = 0
    products = []

    for product_id in product_ids:
        # update quantity for the product in the quantities dictionary
        quantities[product_id] = quantities.get(product_id, 0) + 1

    for product_id, quantity in quantities.items():
        cursor.execute('SELECT * FROM product WHERE id=%s', (product_id,))
        product = cursor.fetchone()
        if product:
            product['Quantity'] = quantity
            product['Total_price'] = product['Price'] * quantity
            total_price += product['Total_price']
            products.append(product)

    return render_template('cart.php', products=products, total_price=total_price)
@views.route('/buy', methods=['POST'])
def buy():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)
    if 'username' not in session:
        flash('You need to log in to place an order!', 'error')
        return redirect(url_for('views.login'))
    username = session['username']
    query = "SELECT ID, CreditPoints FROM customer WHERE Name=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        customer_id = result['ID']
        credit_points = result['CreditPoints']
    else:
        flash('Could not retrieve customer information from database', 'error')
        return redirect(url_for('views.index'))
    order_date = datetime.now()
    products = []
    total_price = 0
    for product_id in session.get('cart', []):
        cursor.execute('SELECT * FROM product WHERE ID=%s', (product_id,))
        product = cursor.fetchone()
        if product:
            product['quantity'] = session['cart'].count(product_id)
            products.append(product)
            total_price += product['Price'] * product['quantity']
    if products:
        # check if there's enough credit points to cover the total price
        if total_price > credit_points:
            flash('You do not have enough credit points to place this order!', 'error')
            return redirect(url_for('views.cart'))
        # deduct the total price from customer's credit points
        credit_points -= total_price
        query = "UPDATE customer SET CreditPoints=%s WHERE ID=%s"
        cursor.execute(query, (credit_points, customer_id))
        # insert the order into the orders table
        query = "SELECT COALESCE(MAX(ID), 0) AS max_id FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()
        order_id = result['max_id'] + 1
        query = "INSERT INTO orders (ID, CustomerID, OrderDate) VALUES (%s, %s, %s)"
        cursor.execute(query, (order_id, customer_id, order_date))
        # insert the order items into the orderitem table
        for product in products:
            query = "SELECT COALESCE(MAX(ID), 0) AS max_id FROM orders"
            cursor.execute(query)
            result = cursor.fetchone()
            order_it_id = result['max_id'] + 1
            query = "INSERT INTO orderitem (ID, OrderID, ProductID, Quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (order_it_id , order_id, product['ID'], product['quantity']))
        # insert the transaction into the transaction table
        query = "SELECT COALESCE(MAX(ID), 0) AS max_id FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()
        trans_id = result['max_id'] + 1
        query = "INSERT INTO transaction (ID, CustomerID, Date, CreditPoints) VALUES (%s, %s, %s,%s)"
        cursor.execute(query, (trans_id,customer_id, order_date, -total_price))
        db_conn.connection.commit()
        session['cart'] = []
        flash('Your order has been placed!', 'success')
        return redirect(url_for('views.index'))
    flash('Your cart is empty!', 'error')
    return redirect(url_for('views.cart'))





@views.route('/cart/remove/<int:id>', methods=['POST'])
def remove_from_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    # Check if product ID exists in the cart
    if id not in session['cart']:
        flash('Product not found in cart', 'error')
        return redirect(url_for('views.cart'))

    # Remove product ID from the cart
    session['cart'].remove(id)
    flash('Product removed from cart', 'success')
    return redirect(url_for('views.cart'))




@views.route('/order_history')
def order_history():
    db_conn = DbConnection.get_instance()
    cursor = db_conn.connection.cursor(dictionary=True)

    if 'username' not in session:
        flash('You need to log in to view your order history!', 'error')
        return redirect(url_for('views.login'))

    username = session['username']
    query = '''
        SELECT o.ID, o.OrderDate, oi.ProductID, oi.Quantity, t.CreditPoints
        FROM orders o
        INNER JOIN orderitem oi ON o.ID = oi.OrderID
        INNER JOIN transaction t ON oi.ID = t.ID
        INNER JOIN customer c ON o.CustomerID = c.ID
        WHERE c.Name = %s
    '''
    cursor.execute(query, (username,))
    order_history = cursor.fetchall()

    return render_template('order_history.php', order_history=order_history)