def delete_product_p1(connection):
    """
    Transaction 1:
    Delete product p1 from Product.

    Because Stock.prodid references Product.prodid with ON DELETE CASCADE,
    PostgreSQL should automatically delete related Stock rows.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Product
                WHERE prodid = %s;
                """,
                ("p1",),
            )

            if cursor.rowcount != 1:
                raise ValueError("Product p1 was not found. Reset the database before running this transaction.")

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Deleted Product row: p1")
        print("Related Stock rows were handled by PostgreSQL ON DELETE CASCADE.")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False


def delete_depot_d1(connection):
    """
    Transaction 2:
    Delete depot d1 from Depot.

    Because Stock.depid references Depot.depid with ON DELETE CASCADE,
    PostgreSQL should automatically delete related Stock rows.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Depot
                WHERE depid = %s;
                """,
                ("d1",),
            )

            if cursor.rowcount != 1:
                raise ValueError("Depot d1 was not found. Reset the database before running this transaction.")

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Deleted Depot row: d1")
        print("Related Stock rows were handled by PostgreSQL ON DELETE CASCADE.")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False


def update_product_p1_to_pp1(connection):
    """
    Transaction 3:
    Change product id p1 to pp1.

    Because Stock.prodid references Product.prodid with ON UPDATE CASCADE,
    PostgreSQL should automatically update related Stock rows.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Product
                SET prodid = %s
                WHERE prodid = %s;
                """,
                ("pp1", "p1"),
            )

            if cursor.rowcount != 1:
                raise ValueError("Product p1 was not found. Reset the database before running this transaction.")

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Updated Product prodid: p1 -> pp1")
        print("Related Stock rows were handled by PostgreSQL ON UPDATE CASCADE.")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False


def update_depot_d1_to_dd1(connection):
    """
    Transaction 4:
    Change depot id d1 to dd1.

    Because Stock.depid references Depot.depid with ON UPDATE CASCADE,
    PostgreSQL should automatically update related Stock rows.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Depot
                SET depid = %s
                WHERE depid = %s;
                """,
                ("dd1", "d1"),
            )

            if cursor.rowcount != 1:
                raise ValueError("Depot d1 was not found. Reset the database before running this transaction.")

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Updated Depot depid: d1 -> dd1")
        print("Related Stock rows were handled by PostgreSQL ON UPDATE CASCADE.")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False


def add_product_p100_and_stock(connection):
    """
    Transaction 5:
    Add Product row (p100, cd, 5)
    and Stock row (p100, d2, 50).

    Both inserts must succeed together. If either insert fails,
    the whole transaction is rolled back.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Product (prodid, pname, price)
                VALUES (%s, %s, %s);
                """,
                ("p100", "cd", 5),
            )

            cursor.execute(
                """
                INSERT INTO Stock (prodid, depid, quantity)
                VALUES (%s, %s, %s);
                """,
                ("p100", "d2", 50),
            )

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Inserted Product row: (p100, cd, 5)")
        print("Inserted Stock row: (p100, d2, 50)")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False


def add_depot_d100_and_stock(connection):
    """
    Transaction 6:
    Add Depot row (d100, Chicago, 100)
    and Stock row (p1, d100, 100).

    Both inserts must succeed together. If either insert fails,
    the whole transaction is rolled back.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Depot (depid, addr, volume)
                VALUES (%s, %s, %s);
                """,
                ("d100", "Chicago", 100),
            )

            cursor.execute(
                """
                INSERT INTO Stock (prodid, depid, quantity)
                VALUES (%s, %s, %s);
                """,
                ("p1", "d100", 100),
            )

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Inserted Depot row: (d100, Chicago, 100)")
        print("Inserted Stock row: (p1, d100, 100)")
        return True

    except Exception as error:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        print(f"Reason: {error}")
        return False