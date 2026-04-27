-- CS623 Project
-- 03_add_constraints.sql
-- Adds primary keys, foreign keys, and basic checks.
-- This is kept separate on purpose so constraints are easy to review.
-- Foreign keys use reactive actions:
--   ON DELETE CASCADE removes related Stock rows automatically.
--   ON UPDATE CASCADE updates related Stock ids automatically.

ALTER TABLE product
    ADD CONSTRAINT pk_product
    PRIMARY KEY (prodid);

ALTER TABLE depot
    ADD CONSTRAINT pk_depot
    PRIMARY KEY (depid);

ALTER TABLE stock
    ADD CONSTRAINT pk_stock
    PRIMARY KEY (prodid, depid);

ALTER TABLE stock
    ADD CONSTRAINT fk_stock_product
    FOREIGN KEY (prodid)
    REFERENCES product (prodid)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE stock
    ADD CONSTRAINT fk_stock_depot
    FOREIGN KEY (depid)
    REFERENCES depot (depid)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE product
    ADD CONSTRAINT chk_product_price_nonnegative
    CHECK (price >= 0);

ALTER TABLE depot
    ADD CONSTRAINT chk_depot_volume_nonnegative
    CHECK (volume >= 0);
