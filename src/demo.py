from src.display import get_all_table_rows, show_all_tables, show_change_summary
from src.reset import reset_database
from src.status import print_database_status
from src.transactions import (
    add_depot_d100_and_stock,
    add_product_p100_and_stock,
    delete_depot_d1,
    delete_product_p1,
    update_depot_d1_to_dd1,
    update_product_p1_to_pp1,
)


DEMO_TRANSACTIONS = [
    {
        "number": 1,
        "title": "Delete product p1",
        "function": delete_product_p1,
    },
    {
        "number": 2,
        "title": "Delete depot d1",
        "function": delete_depot_d1,
    },
    {
        "number": 3,
        "title": "Change product p1 to pp1",
        "function": update_product_p1_to_pp1,
    },
    {
        "number": 4,
        "title": "Change depot d1 to dd1",
        "function": update_depot_d1_to_dd1,
    },
    {
        "number": 5,
        "title": "Add product p100 and stock row",
        "function": add_product_p100_and_stock,
    },
    {
        "number": 6,
        "title": "Add depot d100 and stock row",
        "function": add_depot_d100_and_stock,
    },
]


def run_guided_demo(connection, clear_screen, print_header, pause):
    """
    Run all required transactions in a guided presentation flow.

    The database is reset before each transaction so every transaction starts
    from the original project data. The database is also reset at the end so
    the project finishes in a clean original state.
    """
    clear_screen()
    print_header()

    print("\nGuided Demo Mode")
    print("-" * 60)
    print("This mode runs all six required project transactions.")
    print("Before each transaction, the database is reset to the original state.")
    print("At the end, the database is reset one final time.")
    print("Each step will show BEFORE, AFTER, and a row-level change summary.")
    print()
    print("Press Enter to begin the guided demo.")
    input()

    for demo_item in DEMO_TRANSACTIONS:
        clear_screen()
        print_header()

        print(
            f"\nDemo Step {demo_item['number']} of {len(DEMO_TRANSACTIONS)}: "
            f"{demo_item['title']}"
        )
        print("-" * 60)

        print("\nResetting database before this transaction...")
        reset_database(connection)

        before_rows = get_all_table_rows(connection)

        print("\nBEFORE")
        print("-" * 60)
        show_all_tables(connection)

        print("\nRunning transaction...")
        transaction_success = demo_item["function"](connection)

        after_rows = get_all_table_rows(connection)

        if transaction_success:
            print("\nAFTER COMMIT")
        else:
            print("\nAFTER ROLLBACK / CURRENT STATE")

        print("-" * 60)
        show_all_tables(connection)

        show_change_summary(before_rows, after_rows)

        if demo_item["number"] < len(DEMO_TRANSACTIONS):
            print("\nGuided demo will continue to the next transaction.")
            pause()
        else:
            print("\nAll required transactions have been demonstrated.")
            pause()

    clear_screen()
    print_header()

    print("\nFinal Cleanup")
    print("-" * 60)
    print("Resetting database one final time so the project ends in the original state.")

    reset_database(connection)

    print_database_status(connection)

    print("\nGuided demo complete. The database is back to ORIGINAL.")
    pause()