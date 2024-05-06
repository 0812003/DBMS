CREATE DATABASE IF NOT EXISTS restaurant_management;

USE restaurant_management;

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
    customer VARCHAR(100) NOT NULL,
    table_no INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    order_time DATETIME NOT NULL,
    FOREIGN KEY (item_id) REFERENCES menu_items(id)
);

-- insert into menu_items values(1,'Paneer Masala','Veg',100);
-- insert into menu_items values(2,'Paneer Angar','Veg',150);
-- insert into menu_items values(3,'Veg Cofta','Veg',130);
-- insert into menu_items values(4,'Buttar Chiken','Non-Veg',200);
-- insert into menu_items values(5,'Rice','Veg',60);

SET SQL_SAFE_UPDATES = 0;


DELETE FROM orders;
-- WHERE id = 5;

-- drop database restaurant_management;
