from colorama import Fore, Style
from tabulate import tabulate

from src.ui import error, success, title


TABLE_CONFIG = {
    "Product": {
        "columns": ["prodid", "pname", "price"],
        "order_by": "prodid",
    },
    "Depot": {
        "columns": ["depid", "addr", "volume"],
        "order_by": "depid",
    },
    "Stock": {
        "columns": ["prodid", "depid", "quantity"],
        "order_by": "prodid, depid",
    },
}


def print_rows(table_title, columns, rows):
    """
    Print rows as a clean console table.
    """
    print(f"\n{title(table_title)}")
    print("-" * 60)

    if not rows:
        print("(no rows)")
        return

    print(
        tabulate(
            rows,
            headers=columns,
            tablefmt="pretty",
            numalign="right",
            stralign="left",
        )
    )


def get_table_rows(connection, table_name):
    """
    Return rows for one project table.
    """
    config = TABLE_CONFIG[table_name]
    columns = config["columns"]
    order_by = config["order_by"]

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {", ".join(columns)}
            FROM {table_name}
            ORDER BY {order_by};
            """
        )
        return cursor.fetchall()


def get_all_table_rows(connection):
    """
    Return current rows for Product, Depot, and Stock.
    Used for before/after transaction comparison.
    """
    return {
        table_name: get_table_rows(connection, table_name)
        for table_name in TABLE_CONFIG
    }


def show_table(connection, table_name):
    """
    Query and display one database table.
    """
    config = TABLE_CONFIG[table_name]
    rows = get_table_rows(connection, table_name)

    print_rows(table_name, config["columns"], rows)


def show_all_tables(connection):
    """
    Display Product, Depot, and Stock.
    """
    for table_name in TABLE_CONFIG:
        show_table(connection, table_name)


def print_change_table(change_title, columns, rows, color):
    """
    Print added or removed rows using a color.
    """
    if not rows:
        return

    colored_rows = [
        tuple(f"{color}{value}{Style.RESET_ALL}" for value in row)
        for row in rows
    ]

    print_rows(change_title, columns, colored_rows)


def show_change_summary(before_rows, after_rows):
    """
    Show row-level differences between the before and after table states.

    Green rows were added.
    Red rows were removed.
    """
    print(f"\n{title('CHANGE SUMMARY')}")
    print("-" * 60)

    any_changes = False

    for table_name, config in TABLE_CONFIG.items():
        before_set = set(before_rows[table_name])
        after_set = set(after_rows[table_name])

        removed_rows = sorted(before_set - after_set)
        added_rows = sorted(after_set - before_set)

        if not removed_rows and not added_rows:
            continue

        any_changes = True

        print(f"\n{title(table_name)}")
        print("-" * 60)

        print_change_table(
            error("Removed rows"),
            config["columns"],
            removed_rows,
            Fore.RED,
        )

        print_change_table(
            success("Added rows"),
            config["columns"],
            added_rows,
            Fore.GREEN,
        )

    if not any_changes:
        print(success("No row-level changes detected."))