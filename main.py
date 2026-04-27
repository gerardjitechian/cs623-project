from src.db import get_connection
from src.display import show_all_tables


def print_header():
    print("\n" + "=" * 60)
    print("        Gerard's CS623 Database Project")
    print("=" * 60)


def print_menu():
    print("\nMain Menu")
    print("-" * 60)
    print("1. Show all tables")
    print("0. Exit")
    print("-" * 60)


def main():
    try:
        with get_connection() as connection:
            while True:
                print_header()
                print("Database connection: CONNECTED")

                print_menu()
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    show_all_tables(connection)
                    input("\nPress Enter to return to the menu...")

                elif choice == "0":
                    print("\nGoodbye.")
                    break

                else:
                    print("\nInvalid option. Please try again.")

    except Exception as error:
        print("Something went wrong.")
        print(error)


if __name__ == "__main__":
    main()