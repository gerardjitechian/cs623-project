def delete_product_p1(connection):
    """
    Transaction 1:
    Delete product p1 from Product.

    Related Stock rows should be deleted automatically by
    the foreign key ON DELETE CASCADE constraint.
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

        connection.commit()
        print("\nTransaction committed successfully.")
        print("Product p1 was deleted.")
        print("Related Stock rows were handled by PostgreSQL cascade rules.")

    except Exception:
        connection.rollback()
        print("\nTransaction failed. Changes were rolled back.")
        raise