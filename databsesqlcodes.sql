CREATE DATABASE IF NOT EXISTS void;
USE void;

CREATE TABLE customer (
    c_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    number VARCHAR(15) NOT NULL,
    gmail VARCHAR(100) NOT NULL,
    secret_key VARCHAR(100) NOT NULL,
    image VARCHAR(100) NULL
);

CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    color VARCHAR(50),
    size VARCHAR(20),
    product_available INT,
    costing DECIMAL(10, 2),
    rating DECIMAL(3, 2),
    image VARCHAR(100)
);

CREATE TABLE history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    time_order DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_delivery DATETIME NULL,
    status VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    c_id INT NOT NULL,
    product_id INT NOT NULL,
    product_quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (c_id) REFERENCES customer(c_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
