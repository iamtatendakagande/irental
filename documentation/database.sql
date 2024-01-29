SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+02:00";

-- Create the database
CREATE DATABASE irental;

-- Use the database
USE irental;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    email VARCHAR(35) NOT NULL UNIQUE,
    password VARCHAR(45) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create the properties table
CREATE TABLE properties (
    id int AUTO_INCREMENT PRIMARY KEY,
	email varchar(35) NOT NULL,
	price DOUBLE(16,2) NOT NULL,
	suburb varchar(35) NOT NULL,
	density varchar(35)NOT NULL,
	type_of_property varchar(35) NOT NULL,
	rooms int NOT NULL,
    bedroom int NOT NULL,
	toilets int NOT NULL,
	ensuite int NOT NULL,
	toilets_type varchar(35) NOT NULL,
	garage int NOT NULL,
	swimming_pool TINYINT(1) NOT NULL,
    fixtures_fittings TINYINT(1) NOT NULL,
	cottage int NOT NULL,
	power TINYINT(1) NOT NULL,
	power_backup TINYINT(1) NOT NULL,
	water TINYINT(1) NOT NULL,
	water_backup TINYINT(1) NOT NULL,
	gated_community TINYINT(1) NOT NULL,
	garden_area TINYINT(1) NOT NULL,
	address varchar(60) NOT NULL,
	description varchar(130)NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP	
);

-- Create the users table
CREATE TABLE coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(60) NOT NULL,
	authority VARCHAR(60) NOT NULL,
    coordinates POINT NOT NULL,
    SPATIAL INDEX(coordinates),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);






