import os

from colorama import init

from src.db import get_connection
from src.display import show_all_tables
from src.reset import reset_database
from src.status import print_database_status
from src.transactions import delete_product_p1


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


def print_menu():
    print("\nMain Menu")
    print("-" * 60)
    print("1. Show all tables")
    print("2. Verify database status")
    print("3. Reset database to original state")

    print("\nRequired Transactions")
    print("-" * 60)
    print("4. Delete product p1")

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
    """
    clear_screen()
    print_header()

    print(f"\n{transaction_title}")
    print("-" * 60)

    print("\nBEFORE")
    print("-" * 60)
    show_all_tables(connection)

    print("\nRunning transaction...")
    transaction_function(connection)

    print("\nAFTER")
    print("-" * 60)
    show_all_tables(connection)

    pause()


def main():
    init(autoreset=True)

    try:
        with get_connection() as connection:
            while True:
                clear_screen()
                print_header()
                print("Database connection: CONNECTED")

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