-- Custom MySQL schema required by register_app.
-- This application does NOT use Django models for these two tables.

CREATE DATABASE IF NOT EXISTS mysql;
USE mysql;

CREATE TABLE IF NOT EXISTS `register` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `First_Name` VARCHAR(40) NOT NULL,
    `Last_Name` VARCHAR(40) NOT NULL,
    `gender` VARCHAR(20) NOT NULL,
    `emailid` VARCHAR(254) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `req_time` DATETIME NULL,
    `token` VARCHAR(255) NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_register_emailid` (`emailid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Employee` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `First_Name` VARCHAR(40) NOT NULL,
    `Last_Name` VARCHAR(40) NOT NULL,
    `DOB` DATE NOT NULL,
    `gender` VARCHAR(20) NOT NULL,
    `department` VARCHAR(50) NOT NULL,
    `position` VARCHAR(50) NOT NULL,
    `emailid` VARCHAR(254) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `useremail` VARCHAR(254) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_employee_useremail` (`useremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
