CREATE DATABASE web_scraping;

USE web_scraping;

CREATE TABLE website_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    contact_email VARCHAR(255),
    contact_address TEXT,
    contact_number VARCHAR(50),
    language VARCHAR(50),
    cms_mvc VARCHAR(50),
    category VARCHAR(100)
);