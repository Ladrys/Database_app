
from db_connect import DbConnection
import mysql


class CustomerFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()
        self.cursor = self.db_conn.connection.cursor()

    def create_customer(self, name, city, credit_points, is_active):

        cursor = self.db_conn.cursor()
        query = "SELECT MAX(ID) FROM Customer"
        cursor.execute(query)
        result = cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1
        query = "INSERT INTO Customer (ID, Name, City, CreditPoints, IsActive) VALUES (%s, %s, %s, %s, %s)"
        credit_points = float(credit_points)
        cursor.execute(query, (next_id, name, city, credit_points, is_active))
        self.db_conn.connection.commit()
        cursor.close()
        return True

    def read_customer(self, customer_id):
        self.cursor.execute(
            "SELECT * FROM Customer WHERE ID = %s",
            (customer_id,)
        )
        return self.cursor.fetchone()

    def update_customer(self, customer_id, name, city, credit_points, is_active):
        self.cursor.execute(
            "UPDATE Customer SET Name = %s, City = %s, CreditPoints = %s, IsActive = %s WHERE ID = %s",
            (name, city, credit_points, is_active, customer_id)
        )
        self.db_conn.connection.commit()

    def delete_customer(self, id):

        cursor = self.db_conn.cursor()
        try:
            query = "DELETE FROM Customer WHERE ID=%s"
            cursor.execute(query, (id,))
            self.db_conn.connection.commit()
            rowcount = cursor.rowcount
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == 1451:
                raise Exception(
                    "Cannot delete customer, there are orders associated with it.")
            else:
                raise e
        cursor.close()
        return rowcount > 0


class ProductFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()

    def add_product(self, name, type, price):

        cursor = self.db_conn.cursor()
        query = "SELECT MAX(ID) FROM Product"
        cursor.execute(query)
        result = cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1

        query = "INSERT INTO Product(ID, Name, Type, Price) VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (next_id, name, type, price))
        self.db_conn.connection.commit()
        cursor.close()
        return True

    def get_product(self, product_id: int):

        cursor = self.db_conn.cursor()
        query = "SELECT * FROM Product WHERE ID = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return product

    def update_product(self, id, name=None, type=None, price=None):

        cursor = self.db_conn.cursor()
        query = "UPDATE Product SET Name=%s, Type=%s, Price=%s WHERE ID=%s"
        cursor.execute(query, (name, type, price, id))
        self.db_conn.connection.commit()
        cursor.close()

    def delete_product(self, id):

        cursor = self.db_conn.cursor()

        query = "SELECT * FROM Product WHERE ID=%s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return False

        query = "DELETE FROM OrderItem WHERE ProductID=%s"
        cursor.execute(query, (id,))
        self.db_conn.connection.commit()

        query = "DELETE FROM Product WHERE ID=%s"
        cursor.execute(query, (id,))
        self.db_conn.connection.commit()
        cursor.close()
        return True


class OrdersFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()

    def create_order(self, customer_id, order_date, products):
        cursor = self.db_conn.cursor()
        query = "SELECT MAX(ID) FROM Orders"
        cursor.execute(query)
        result = cursor.fetchone()
        next_order_id = 1 if result[0] is None else result[0] + 1
        query = "INSERT INTO orders (ID, CustomerID, OrderDate) VALUES (%s, %s, %s)"
        cursor.execute(query, (next_order_id, customer_id, order_date))
        self.db_conn.connection.commit()

        total_price = 0
        for product in products:
            product_id = product['id']
            quantity = product['quantity']
            query = "SELECT Price FROM product WHERE ID=%s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            product_price = result[0]
            total_price += product_price * quantity

            query = "SELECT MAX(ID) FROM OrderItem"
            cursor.execute(query)
            result = cursor.fetchone()
            next_item_id = 1 if result[0] is None else result[0] + 1

            query = "INSERT INTO OrderItem (ID, OrderID, ProductID, Quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                query, (next_item_id, next_order_id, product_id, quantity))

        query = "SELECT CreditPoints FROM Customer WHERE ID=%s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        current_credit_points = result[0]
        updated_credit_points = current_credit_points - total_price
        query = "UPDATE Customer SET CreditPoints=%s WHERE ID=%s"
        cursor.execute(query, (updated_credit_points, customer_id))

        query = "INSERT INTO Transaction (CustomerID, Date, CreditPoints) VALUES (%s, %s, -%s)"
        cursor.execute(query, (customer_id, order_date, total_price))

        self.db_conn.connection.commit()
        cursor.close()
        return next_order_id

    def update_order(self, order_id: int, customer_id: int, order_date: str) -> bool:
        cursor = self.db_conn.cursor()
        query = "UPDATE orders SET CustomerID = %s, OrderDate = %s WHERE ID = %s"
        cursor.execute(query, (customer_id, order_date, order_id))
        self.db_conn.connection.commit()
        return cursor.rowcount == 1

    def delete_order(self, id):
        cursor = self.db_conn.cursor()

        query = "SELECT * FROM Orders WHERE ID=%s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return False

        query = "DELETE FROM OrderItem WHERE OrderID=%s"
        cursor.execute(query, (id,))
        self.db_conn.connection.commit()

        query = "DELETE FROM Orders WHERE ID=%s"
        cursor.execute(query, (id,))
        self.db_conn.connection.commit()

        cursor.close()
        return True

    def get_order(self, order_id: int) -> dict:
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM Orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        if result:
            return {"id": result[0], "customer_id": result[1], "order_date": result[2]}
        else:
            return None


class OrderItemFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()

    def create_order_item(self, order_id, product_id, quantity):
        cursor = self.db_conn.cursor()
        query = "SELECT MAX(ID) FROM OrderItem"
        cursor.execute(query)
        result = cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1
        cursor.execute(
            "INSERT INTO OrderItem (ID, OrderID, ProductID, Quantity) VALUES (%s, %s, %s, %s)",
            (next_id, order_id, product_id, quantity)
        )
        self.db_conn.connection.commit()
        cursor.close()
        return next_id

    def read_order_item(self, order_item_id):
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT * FROM OrderItem WHERE ID = %s",
            (order_item_id,)
        )
        return cursor.fetchone()

    def update_order_item(self, order_item_id, order_id, product_id, quantity):
        cursor = self.db_conn.cursor()
        cursor.execute(
            "UPDATE OrderItem SET OrderID = %s, ProductID = %s, Quantity = %s WHERE ID = %s",
            (order_id, product_id, quantity, order_item_id)
        )
        self.db_conn.connection.commit()

    def delete_order_item(self, order_item_id):
        cursor = self.db_conn.cursor()

        query = "SELECT * FROM OrderItem WHERE ID=%s"
        cursor.execute(query, (order_item_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return False

        query = "DELETE FROM OrderItem WHERE ID=%s"
        cursor.execute(query, (order_item_id,))
        self.db_conn.connection.commit()

        cursor.close()
        return True


class TransactionFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()
        self.cursor = self.db_conn.connection.cursor()

    def create_transaction(self, customer_id, credit_points, date):
        query = "SELECT MAX(ID) FROM Transaction"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        next_id = 1 if result[0] is None else result[0] + 1
        self.cursor.execute(
            "INSERT INTO Transaction (CustomerID, CreditPoints, Date) VALUES (%s, %s, %s)",
            (next_id, customer_id, credit_points, date)
        )
        self.db_conn.connection.commit()

    def read_transaction(self, transaction_id):
        self.cursor.execute(
            "SELECT * FROM Transaction WHERE ID = %s",
            (transaction_id,)
        )
        return self.cursor.fetchone()

    def update_transaction(self, transaction_id, customer_id, date, credit_points):
        self.cursor.execute(
            "UPDATE Transaction SET CustomerID = %s, Date = %s, CreditPoints = %s WHERE ID = %s",
            (customer_id, date, credit_points, transaction_id)
        )
        self.db_conn.connection.commit()

    def delete_transaction(self, transaction_id):

        query = "SELECT * FROM Transaction WHERE ID=%s"
        self.cursor.execute(query, (transaction_id,))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.close()
            return False

        self.cursor.execute(
            "DELETE FROM Transaction WHERE ID = %s",
            (transaction_id,)
        )
        self.db_conn.connection.commit()


class GenerateReportFactory:
    def __init__(self):
        self.db_conn = DbConnection.get_instance()
        self.cursor = self.db_conn.connection.cursor()

    def generate_report(self):

        self.cursor.execute("SELECT City, SUM(CreditPoints) AS TotalCreditPoints, COUNT(*) AS TotalCustomers "
                            "FROM Customer "
                            "GROUP BY City")
        customer_data = self.cursor.fetchall()

        self.cursor.execute("SELECT Type, SUM(Price * Quantity) AS TotalSales "
                            "FROM OrderItem "
                            "JOIN Product ON OrderItem.ProductID = Product.ID "
                            "GROUP BY Type")
        product_data = self.cursor.fetchall()

        report = "-----------------------------\n"
        report += "Summary Report\n"
        report += "-----------------------------\n\n"

        report += "Customer Data:\n"
        report += "City, Total Credit Points, Total Customers\n"
        for row in customer_data:
            report += f"{row[0]}, {row[1]}, {row[2]}\n"
        report += "\n"

        report += "Product Data:\n"
        report += "Type, Total Sales\n"
        for row in product_data:
            report += f"{row[0]}, {row[1]}\n"

        report += "-----------------------------\n"
        report += "End of Report\n"
        report += "-----------------------------\n"

        self.cursor.close()

        return report
