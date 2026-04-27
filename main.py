import os

from colorama import init

from src.db import get_connection
from src.display import get_all_table_rows, show_all_tables, show_change_summary
from src.reset import reset_database
from src.status import (
    connection_status_label,
    data_status_label,
    get_overall_data_status,
    is_connection_alive,
    print_database_status,
)
from src.transactions import (
    add_depot_d100_and_stock,
    add_product_p100_and_stock,
    delete_depot_d1,
    delete_product_p1,
    update_depot_d1_to_dd1,
    update_product_p1_to_pp1,
)


def clear_screen():
    """
    Clear the terminal screen for a cleaner console demo.
    """
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """
    Wait for the user before returning to the menu.
    """
    input("\nPress Enter to return to the menu...")


def print_header():
    print("\n" + "=" * 60)
    print("        Gerard's CS623 Database Project")
    print("=" * 60)


def print_runtime_status(connection):
    """
    Print current connection and data status for the main menu.
    """
    if is_connection_alive(connection):
        connection_status = "CONNECTED"
    else:
        connection_status = "DISCONNECTED"

    data_status = get_overall_data_status(connection)

    print(f"Database connection: {connection_status_label(connection_status)}")
    print(f"Data status:         {data_status_label(data_status)}")


def print_menu():
    print("\nMain Menu")
    print("-" * 60)
    print("1. Show all tables")
    print("2. Verify database status")
    print("3. Reset database to original state")

    print("\nRequired Transactions")
    print("-" * 60)
    print("4. Delete product p1")
    print("5. Delete depot d1")
    print("6. Change product p1 to pp1")
    print("7. Change depot d1 to dd1")
    print("8. Add product p100 and stock row")
    print("9. Add depot d100 and stock row")

    print("\n0. Exit")
    print("-" * 60)


def confirm_reset():
    """
    Ask the user to confirm before resetting the database.
    """
    clear_screen()
    print_header()

    print("\nReset Database")
    print("-" * 60)
    print("This will restore the database to the original project data.")
    print("Any changes from previous transaction tests will be removed.")
    print()
    print("Type RESET to continue.")
    print("Press Enter to cancel and return to the main menu.")
    print("-" * 60)

    user_input = input("Your choice: ").strip()

    return user_input == "RESET"


def show_before_after(connection, transaction_title, transaction_function):
    """
    Display tables before and after a transaction.
    Also show a row-level change summary.
    """
    clear_screen()
    print_header()

    print(f"\n{transaction_title}")
    print("-" * 60)

    before_rows = get_all_table_rows(connection)

    print("\nBEFORE")
    print("-" * 60)
    show_all_tables(connection)

    print("\nRunning transaction...")
    transaction_success = transaction_function(connection)

    after_rows = get_all_table_rows(connection)

    if transaction_success:
        print("\nAFTER COMMIT")
    else:
        print("\nAFTER ROLLBACK / CURRENT STATE")

    print("-" * 60)
    show_all_tables(connection)

    show_change_summary(before_rows, after_rows)

    pause()


def main():
    init(autoreset=True)

    try:
        with get_connection() as connection:
            while True:
                clear_screen()
                print_header()
                print_runtime_status(connection)

                print_menu()
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    clear_screen()
                    print_header()
                    show_all_tables(connection)
                    pause()

                elif choice == "2":
                    clear_screen()
                    print_header()
                    print_database_status(connection)
                    pause()

                elif choice == "3":
                    if confirm_reset():
                        clear_screen()
                        print_header()
                        reset_database(connection)
                        print_database_status(connection)
                        pause()
                    else:
                        clear_screen()
                        print_header()
                        print("\nReset cancelled. No changes were made.")
                        pause()

                elif choice == "4":
                    show_before_after(
                        connection,
                        "Transaction 1: Delete product p1",
                        delete_product_p1,
                    )

                elif choice == "5":
                    show_before_after(
                        connection,
                        "Transaction 2: Delete depot d1",
                        delete_depot_d1,
                    )

                elif choice == "6":
                    show_before_after(
                        connection,
                        "Transaction 3: Change product p1 to pp1",
                        update_product_p1_to_pp1,
                    )

                elif choice == "7":
                    show_before_after(
                        connection,
                        "Transaction 4: Change depot d1 to dd1",
                        update_depot_d1_to_dd1,
                    )

                elif choice == "8":
                    show_before_after(
                        connection,
                        "Transaction 5: Add product p100 and stock row",
                        add_product_p100_and_stock,
                    )

                elif choice == "9":
                    show_before_after(
                        connection,
                        "Transaction 6: Add depot d100 and stock row",
                        add_depot_d100_and_stock,
                    )

                elif choice == "0":
                    clear_screen()
                    print("Exiting Gerard's CS623 Database Project. Session complete.")
                    break

                else:
                    print("\nInvalid option. Please try again.")
                    pause()

    except Exception as error:
        print("Something went wrong.")
        print(error)


if __name__ == "__main__":
    main()