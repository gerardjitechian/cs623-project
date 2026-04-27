from decimal import Decimal

from colorama import Fore, Style


# Expected original data based on sql/02_insert_data.sql
EXPECTED_DATA = {
    "Product": {
        "columns": ["prodid", "pname", "price"],
        "order_by": "prodid",
        "rows": [
            ("p1", "tape", Decimal("2.50")),
            ("p2", "tv", Decimal("250.00")),
            ("p3", "vcr", Decimal("80.00")),
        ],
    },
    "Depot": {
        "columns": ["depid", "addr", "volume"],
        "order_by": "depid",
        "rows": [
            ("d1", "New York", 9000),
            ("d2", "Syracuse", 6000),
            ("d4", "New York", 2000),
        ],
    },
    "Stock": {
        "columns": ["prodid", "depid", "quantity"],
        "order_by": "prodid, depid",
        "rows": [
            ("p1", "d1", 1000),
            ("p1", "d2", -100),
            ("p1", "d4", 1200),
            ("p2", "d1", -400),
            ("p2", "d2", 2000),
            ("p2", "d4", 1500),
            ("p3", "d1", 3000),
            ("p3", "d4", 2000),
        ],
    },
}


def status_label(label):
    """
    Return a colored status label for console output.
    """
    if label == "[OK]":
        return f"{Fore.GREEN}{label}{Style.RESET_ALL}"

    if label == "[WARNING]":
        return f"{Fore.YELLOW}{label}{Style.RESET_ALL}"

    if label == "[ERROR]":
        return f"{Fore.RED}{label}{Style.RESET_ALL}"

    return label


def data_status_label(status):
    """
    Return a colored overall data status.
    """
    if status == "ORIGINAL":
        return f"{Fore.GREEN}{status}{Style.RESET_ALL}"

    if status == "MODIFIED":
        return f"{Fore.RED}{status}{Style.RESET_ALL}"

    return status


def print_section(title):
    """
    Print a section title with a simple underline.
    """
    print(f"\n{title}")
    print("-" * 72)


def print_status_row(status, item, detail):
    """
    Print one aligned status row.
    """
    plain_status = status
    colored_status = status_label(status)
    spacing = " " * max(0, 10 - len(plain_status))

    print(f"{colored_status}{spacing} {item:<18} {detail}")


def table_exists(connection, table_name):
    """
    Check whether a table exists in the public schema.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = %s
            );
            """,
            (table_name.lower(),),
        )
        return cursor.fetchone()[0]


def get_connection_info(connection):
    """
    Return the current PostgreSQL user and database.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_user, current_database();")
        return cursor.fetchone()


def get_table_rows(connection, table_name, columns, order_by):
    """
    Return selected rows from a table in a consistent order.
    """
    column_list = ", ".join(columns)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {column_list}
            FROM {table_name}
            ORDER BY {order_by};
            """
        )
        return cursor.fetchall()


def check_original_data(connection):
    """
    Check whether each project table exactly matches the original data.
    """
    results = {}

    for table_name, expected in EXPECTED_DATA.items():
        if not table_exists(connection, table_name):
            results[table_name] = {
                "exists": False,
                "expected_count": len(expected["rows"]),
                "actual_count": None,
                "matches_expected": False,
            }
            continue

        actual_rows = get_table_rows(
            connection,
            table_name,
            expected["columns"],
            expected["order_by"],
        )

        expected_rows = expected["rows"]

        results[table_name] = {
            "exists": True,
            "expected_count": len(expected_rows),
            "actual_count": len(actual_rows),
            "matches_expected": actual_rows == expected_rows,
        }

    return results


def print_database_status(connection):
    """
    Print a clean database status report for the console app.
    """
    current_user, current_database = get_connection_info(connection)

    print_section("Database Connection Status")
    print_status_row("[OK]", "PostgreSQL", "Connected")
    print_status_row("[OK]", "Current user", current_user)
    print_status_row("[OK]", "Database", current_database)

    print_section("Project Tables and Data Check")
    print(f"{'Status':<10} {'Table':<18} {'Rows':<14} Result")
    print("-" * 72)

    data_results = check_original_data(connection)

    for table_name, result in data_results.items():
        if not result["exists"]:
            print(
                f"{status_label('[ERROR]'):<19} "
                f"{table_name:<18} {'N/A':<14} Table is missing"
            )
            continue

        row_summary = f"{result['actual_count']} / {result['expected_count']}"

        if result["matches_expected"]:
            print(
                f"{status_label('[OK]'):<19} "
                f"{table_name:<18} {row_summary:<14} Original data verified"
            )
        else:
            print(
                f"{status_label('[WARNING]'):<19} "
                f"{table_name:<18} {row_summary:<14} Data has changed"
            )

    print_section("Overall Data Status")

    if all(result["matches_expected"] for result in data_results.values()):
        print_status_row("[OK]", "Data status", data_status_label("ORIGINAL"))
        print("\nThe database matches the original project data.")
    else:
        print_status_row("[WARNING]", "Data status", data_status_label("MODIFIED"))
        print("\nReset the database before running a clean demo.")