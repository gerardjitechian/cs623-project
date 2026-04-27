-- CS623 Project
-- 02_insert_data.sql
-- Inserts the starting data from the Product, Depot, and Stock examples.
-- Run this before adding the constraints.

INSERT INTO product (prodid, pname, price) VALUES
    ('p1', 'tape', 2.50),
    ('p2', 'tv', 250.00),
    ('p3', 'vcr', 80.00);

INSERT INTO depot (depid, addr, volume) VALUES
    ('d1', 'New York', 9000),
    ('d2', 'Syracuse', 6000),
    ('d4', 'New York', 2000);

INSERT INTO stock (prodid, depid, quantity) VALUES
    ('p1', 'd1', 1000),
    ('p1', 'd2', -100),
    ('p1', 'd4', 1200),
    ('p3', 'd1', 3000),
    ('p3', 'd4', 2000),
    ('p2', 'd4', 1500),
    ('p2', 'd1', -400),
    ('p2', 'd2', 2000);
