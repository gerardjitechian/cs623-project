def print_rows(title, columns, rows):
    """
    Print rows in a simple table format for the console demo.
    """
    print("\n" + title)
    print("-" * 60)
    print(" | ".join(columns))
    print("-" * 60)

    if not rows:
        print("(no rows)")
        return

    for row in rows:
        print(" | ".join(str(value) for value in row))


def show_table(connection, table_name, columns, order_by):
    """
    Query and display one database table.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {", ".join(columns)}
            FROM {table_name}
            ORDER BY {order_by};
            """
        )
        rows = cursor.fetchall()

    print_rows(table_name, columns, rows)


def show_all_tables(connection):
    """
    Display Product, Depot, and Stock.
    """
    show_table(
        connection,
        "Product",
        ["prodid", "pname", "price"],
        "prodid",
    )

    show_table(
        connection,
        "Depot",
        ["depid", "addr", "volume"],
        "depid",
    )

    show_table(
        connection,
        "Stock",
        ["prodid", "depid", "quantity"],
        "prodid, depid",
    )