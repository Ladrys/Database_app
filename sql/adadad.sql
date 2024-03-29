-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: app1
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `City` varchar(255) NOT NULL,
  `CreditPoints` float NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telephone` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'ladra','Praha',7587,'ladra','ladra@spsejecna.cz','+420 773 615 534'),(2,'pablo','Pablov',10000,'pablo','pablo@jouda.com',NULL),(3,'vankat','unknown',10000,'jouda','vankat@jouda.cz',NULL),(4,'blbec','unknown',10000,'ladra','michalladra11@gmail.com',NULL),(5,'mandik','unknown',6305,'mandik','manidk@spsejecna.cz','unknown'),(6,'John Doe','New York',100,'password','john.doe@example.com',NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `OrderID` int NOT NULL,
  `ProductID` int NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `OrderID` (`OrderID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`ID`),
  CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
INSERT INTO `orderitem` VALUES (2,1,14,1),(3,2,1,5),(4,3,1,5);
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `OrderDate` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2023-04-20 04:44:33'),(2,1,'2022-01-01 00:00:00'),(3,1,'2022-01-01 00:00:00');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Type` enum('Food','Clothing','Furniture','Electronics','Cars','Gaming','Sport') NOT NULL,
  `Price` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Beef Burger','Food',63),(2,'Pizza Margherita','Food',128),(3,'Tomato Soup','Food',52),(4,'Bread','Food',18),(5,'Chicken Curry','Food',83),(6,'Taco','Food',45),(7,'Cheese Sandwich','Food',29),(8,'Salmon Sushi Roll','Food',110),(9,'Spaghetti Bolognese','Food',74),(10,'Roast Beef','Food',105),(11,'Chocolate Cake','Food',41),(12,'Cotton T-Shirt','Clothing',207),(13,'Leather Boots','Clothing',705),(14,'Denim Jeans','Clothing',347),(15,'Sunglasses','Clothing',248),(16,'Sweatpants','Clothing',192),(17,'Leather Jacket','Clothing',951),(18,'Running Shoes','Clothing',399),(19,'Swim Shorts','Clothing',134),(20,'Winter Hat','Clothing',89),(21,'Casual Shirt','Clothing',164),(22,'Coffee Table','Furniture',3829),(23,'Armchair','Furniture',2617),(24,'Bookcase','Furniture',4737),(25,'Dining Table','Furniture',5186),(26,'Wardrobe','Furniture',8263),(27,'Bedside Table','Furniture',1608),(28,'Sofa','Furniture',5741),(29,'Bean Bag Chair','Furniture',1679),(30,'Ottoman','Furniture',2149),(31,'TV Stand','Furniture',2547),(32,'Smartphone','Electronics',14359),(33,'Laptop','Electronics',19877),(34,'Bluetooth Speaker','Electronics',2359),(35,'Smart Watch','Electronics',9292),(36,'Tablet','Electronics',8456),(37,'Wireless Earbuds','Electronics',3267),(38,'Gaming Mouse','Gaming',1204),(39,'Gaming Keyboard','Gaming',1673),(40,'Gaming Headset','Gaming',2579),(41,'Gaming Chair','Gaming',4836),(42,'Gaming Monitor','Gaming',6412),(43,'PS5','Gaming',18399),(44,'Xbox Series X','Gaming',18762),(45,'Nintendo Switch','Gaming',9491),(46,'Soccer Ball','Sport',476),(47,'Basketball','Sport',803),(48,'Tennis Racket','Sport',2279),(49,'Running Shoes','Sport',1212),(50,'Swim Goggles','Sport',605),(51,'Dumbbells','Sport',3527),(52,'Yoga Mat','Sport',820),(53,'Resistance Bands','Sport',1474),(54,'Jump Rope','Sport',409),(55,'Exercise Bike','Sport',9903),(56,'SUV','Cars',856052),(57,'Sedan','Cars',735159),(58,'Pickup Truck','Cars',999393),(59,'Hatchback','Cars',531236),(60,'Sports Car','Cars',2556200),(61,'Convertible','Cars',1925640),(62,'Minivan','Cars',600478),(63,'Motorcycle','Cars',321124),(64,'Electric Car','Cars',1237750);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `Date` datetime NOT NULL,
  `CreditPoints` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (2,1,'2023-04-20 04:44:33',-347),(7,1,'2022-01-01 00:00:00',-315),(8,1,'2022-01-01 00:00:00',-315);
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-20  8:50:44
