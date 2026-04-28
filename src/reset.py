import time
from pathlib import Path

from src.ui import error, info, success, title, warning


def run_sql_file(connection, file_path):
    """
    Run one SQL file against the current database connection.
    """
    sql_text = file_path.read_text()

    with connection.cursor() as cursor:
        cursor.execute(sql_text)


def show_loading_bar(message="Resetting database"):
    """
    Simple loading bar for the console reset flow.
    """
    total_steps = 20
    total_seconds = 1.75
    delay = total_seconds / total_steps

    print()
    print(info(message))

    for step in range(total_steps + 1):
        filled = "█" * step
        empty = "░" * (total_steps - step)
        percent = int((step / total_steps) * 100)

        print(f"\r{info('[' + filled)}{empty}{info(']')} {percent}%", end="", flush=True)
        time.sleep(delay)

    print("\n")


def reset_database(connection):
    """
    Reset the database back to the original project state.

    This runs the table creation, data insertion, and constraint scripts.
    It does not run 00_create_database.sql because the database already exists.
    """
    project_root = Path(__file__).resolve().parents[1]
    sql_folder = project_root / "sql"

    scripts = [
        "01_create_tables.sql",
        "02_insert_data.sql",
        "03_add_constraints.sql",
    ]

    try:
        print(title("Reset Process"))
        print("-" * 60)

        for script_name in scripts:
            script_path = sql_folder / script_name
            print(f"{info('Running')} {script_name}...")
            run_sql_file(connection, script_path)

        show_loading_bar()
        connection.commit()
        print(success("Database reset completed successfully."))

    except Exception:
        connection.rollback()
        print(error("\nDatabase reset failed. Changes were rolled back."))
        raise