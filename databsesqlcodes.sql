CREATE DATABASE void;
USE DATABASE void;



CREATE TABLE Customer (
    c_id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255),
    number VARCHAR(15),
    gmail VARCHAR(100),
    secret_key VARCHAR(100),
    image VARCHAR(100)
);


CREATE TABLE Product (
    product_name VARCHAR(100),
    product_id INT PRIMARY KEY,
    price DECIMAL(10, 2),
    color VARCHAR(50),
    size VARCHAR(20),
    product_available INT,
    costing DECIMAL(10, 2),
    rating DECIMAL(3, 2),
    image VARCHAR(100)
);


CREATE TABLE History (
    history_id INT PRIMARY KEY,
    product_id INT,
    time_order DATETIME,
    time_delivery DATETIME,
    status VARCHAR(50),
    price DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);



CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    c_id INT,
    product_id INT,
    price DECIMAL(10, 2),
    order_time DATETIME,
    
    FOREIGN KEY (c_id) REFERENCES Customer(c_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

