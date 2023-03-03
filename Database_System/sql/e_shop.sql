use app1;
CREATE TABLE Customer (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    CreditPoints FLOAT NOT NULL,
    IsActive BOOLEAN NOT NULL
);

CREATE TABLE Product (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Category ENUM('Electronics', 'Furniture', 'Clothing') NOT NULL,
    Price FLOAT NOT NULL
);

CREATE TABLE Orders (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
);

CREATE TABLE OrderItem (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(ID),
    FOREIGN KEY (ProductID) REFERENCES Product(ID)
);

CREATE TABLE Transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Date DATETIME NOT NULL,
    CreditPoints FLOAT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
);

INSERT INTO Customer (Name, City, CreditPoints, IsActive) VALUES ('John Smith', 'New York', 100, 1);
INSERT INTO Customer (Name, City, CreditPoints, IsActive) VALUES ('Jane Doe', 'Los Angeles', 50, 1);
INSERT INTO Customer (Name, City, CreditPoints, IsActive) VALUES ('Bob Johnson', 'Chicago', 25, 0);

INSERT INTO Product (Name, Type, Price) VALUES ('iPad', 'Electronics', 499);
INSERT INTO Product (Name, Type, Price) VALUES ('Sofa', 'Furniture', 999);
INSERT INTO Product (Name, Type, Price) VALUES ('T-Shirt', 'Clothing', 19);

INSERT INTO Orders (CustomerID, OrderDate) VALUES (1, '2022-01-01');
INSERT INTO Orders (CustomerID, OrderDate) VALUES (2, '2022-02-01');
INSERT INTO Orders (CustomerID, OrderDate) VALUES (1, '2022-03-01');

INSERT INTO OrderItem (OrderID, ProductID, Quantity) VALUES (1, 1, 2);
INSERT INTO OrderItem (OrderID, ProductID, Quantity) VALUES (1, 2, 1);
INSERT INTO OrderItem (OrderID, ProductID, Quantity) VALUES (2, 3, 5);

INSERT INTO Transaction (CustomerID, Date, CreditPoints) VALUES (1, '2022-01-05', 10);
INSERT INTO Transaction (CustomerID, Date, CreditPoints) VALUES (2, '2022-02-15', -5);
INSERT INTO Transaction (CustomerID, Date, CreditPoints) VALUES (1, '2022-03-20', 20);


select * from customes;







CREATE VIEW ActiveCustomers AS
    SELECT Name, City, CreditPoints
    FROM Customer
    WHERE IsActive = 1;
    
select * from ActiveCustomers;    

CREATE VIEW ProductSales AS
    SELECT Product.Name,Product.Type,SUM(OrderItem.Quantity * Product.Price) as TotalPrice, SUM(OrderItem.Quantity) as QuantitySold
    FROM Product
    JOIN OrderItem ON Product.ID = OrderItem.ProductID
    GROUP BY Product.Name,Product.Type;
    
 select * from ProductSales;   
    