Aplha3 - Database System    

published_date= 5.2 2023
name = Michal Ladra 
class = C4b
phone = +420773615534
email = ladra@spsejecna.cz
school = SPŠE Ječná, Praha 2
Desc = This is a school project.


The program is a data management system for a e-shop. The system allows you to add and retrieve data about customers, products, orders, order items, and transactions.
The program uses several classes, each representing a different type of data in the store.
The Customer class represents a customer in the store. It has properties such as name, address, city, and credit points.
The Product class represents a product in the store. It has properties such as name, type, and price.
The Order class represents an order placed by a customer. It has properties such as customer ID, order date, and order ID.
The OrderItem class represents a single item in an order. It has properties such as order ID, product ID, and quantity.
The Transaction class represents a transaction between the store and a customer. It has properties such as transaction ID, order ID, and amount.
The data for each of these classes is stored in a database. The program also includes several factory classes, each representing a different type of data in the store, to interact with the database. The factories are responsible for adding, retrieving, and modifying data in the database.
The GenerateReportFactory class allows you to generate a summary report of the data in the store, including information about customers and products. 
There is also a possibility to import csv files.
To use the program, you will need to create instances of the different classes and factory classes, and use their methods to add, retrieve, and modify data in the store.

Functions: 

create_customer: creates a new customer and inserts it into the "Customer" table.
read_customer: retrieves a specific customer by ID from the "Customer" table.
update_customer: updates the information of an existing customer in the "Customer" table.
delete_customer: deletes a customer from the "Customer" table.
ProductFactory: A class that adds, retrieves, updates, and deletes products in the database.

add_product: adds a new product and inserts it into the "Product" table.
get_product: retrieves a specific product by ID from the "Product" table.
update_product: updates the information of an existing product in the "Product" table.
delete_product: deletes a product from the "Product" table.
OrdersFactory: A class for creating, reading, updating, and deleting orders in the database.

create_order: creates a new order and inserts it into the "Orders" table.
read_order: retrieves a specific order by ID from the "Orders" table.
update_order: updates the information of an existing order in the "Orders" table.
delete_order: deletes an order from the "Orders" table.
OrderItemFactory: A class for creating, reading, updating, and deleting order items in the database.

create_order_item: creates a new order item and inserts it into the "OrderItem" table.
read_order_item: retrieves a specific order item by ID from the "OrderItem" table.
update_order_item: updates the information of an existing order item in the "OrderItem" table.
delete_order_item: deletes an order item from the "OrderItem" table.
Transaction Factory: A class for creating, reading, updating, and deleting transactions in the database.

create_transaction: creates a new transaction and inserts it into the "Transaction" table.
read_transaction: retrieves a specific transaction by ID from the "Transaction" table.
update_transaction: updates the information of an existing transaction in the "Transaction" table.
delete_transaction: deletes a transaction from the "Transaction" table.¨¨


generate_report:  generates a report that summarizes the data in a database.


menu function: This function likely displays the main menu of the program and provides options for accessing other parts of the program.

customer_menu function: This function is likely related to customer management and may provide options for adding, modifying, and retrieving information about customers.

product_menu function: This function is likely related to product management and may provide options for adding, modifying, and retrieving information about products.

order_menu function: This function is likely related to order management and may provide options for creating, modifying, and retrieving information about orders.

order_item_menu function: This function is likely related to managing items within orders and may provide options for adding, modifying, and retrieving information about items in orders.

transaction_menu function: This function is likely related to transaction management and may provide options for creating, modifying, and retrieving information about transactions.


import_data function : its purpose is to import data into the program from a CSV file. The function prompts the user to enter the file format, which must be "csv", and the name of the file and the name of the table to import data to. 


Exceptions : 

mysql.connector.errors.IntegrityError: This error occurs when you try to delete a customer that has associated orders. This error will have an errno attribute equal to 1451. In this case, you raise a custom exception "Cannot delete customer, there are orders associated with it.".

AttributeError: This error occurs when an object doesn't have an attribute that you're trying to access. For example, you may get this error if the DbConnection object doesn't have the attribute connection.

TypeError: This error occurs when you pass the wrong type of argument to a function or try to perform an operation on an object of an incompatible type. For example, you may get this error if credit_points is not a valid float value.

IndexError: This error occurs when you try to access an index in a list or tuple that doesn't exist. For example, you may get this error if the result of the query SELECT MAX(ID) FROM Customer returns an empty result.

ProgrammingError: This error occurs when you try to execute an invalid SQL statement. For example, you may get this error if you have a typo in your SQL query or if the table name doesn't exist.


How to setup this program? 
1. Download MySQL and install it with all adons.
2. Create a localhost connection with parrametrs : 
    Hostname  = 127.0.0.1
    Port = 3306
    Username = app1user
    Password = student
3. Cerate new querry and copy everything from the e-shop.sql file into the querry. 
4. Firstly create and use the database and then create the tables. After that you can insert some data if you want and then exucute the create views statements.

Now you are ready to start your e-shop. 

In viusal studio code terminal change the directory to src folder. Use command : cd  Database_System\src
then type: python main.py 
Now you program will be started .


Your main activity will be probably creating orders for the customers, so i implemented a functionality in a  Create new order option, which will create the order and fill all the tables with the corespondent data. Such us product data, orderitem data and also transaction data, whitch will show you how much has the customer spent etc. Obviously the customers credit will be deducted after creating the order based on the price of a product and its quantity.


Program still observe some exceptions. Let me know on my email if you find any.

Thanks for reading the doc and happy usage :)


