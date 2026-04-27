-- CS623 Project
-- 01_create_tables.sql
-- Run this after connecting to the cs623_project database.
-- This file creates the three project tables without keys or constraints.
-- Constraints are added separately in 03_add_constraints.sql.

DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS depot;
DROP TABLE IF EXISTS product;

CREATE TABLE product (
    prodid VARCHAR(10),
    pname  VARCHAR(50),
    price  NUMERIC(10, 2)
);

CREATE TABLE depot (
    depid  VARCHAR(10),
    addr   VARCHAR(50),
    volume INTEGER
);

CREATE TABLE stock (
    prodid   VARCHAR(10),
    depid    VARCHAR(10),
    quantity INTEGER
);
