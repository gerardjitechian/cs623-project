# CS623 Database Management Systems Project

A local Python + PostgreSQL console application for demonstrating database transactions, referential integrity, cascading updates/deletes, and rollback behavior.

This project uses the `Product`, `Depot`, and `Stock` relations from CS623 and implements the required transactions through a menu-driven Python console app.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Database Design](#database-design)
- [Data Dictionary](#data-dictionary)
- [Original Data](#original-data)
- [SQL Scripts](#sql-scripts)
- [Python Application Structure](#python-application-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Console Menu Features](#console-menu-features)
- [Required Transactions](#required-transactions)
- [Rollback / Failure Demo](#rollback--failure-demo)
- [Reset Behavior](#reset-behavior)
- [Testing Checklist](#testing-checklist)
- [Notes for Presentation](#notes-for-presentation)
- [Author](#author)

---

## Project Overview

This application demonstrates how a Python program can interact with a PostgreSQL database to execute database transactions safely.

The main focus of the project is not a front end or web interface. Instead, this project uses a console-based application to demonstrate:

- PostgreSQL table design
- Primary key and foreign key constraints
- Reactive constraints using `ON DELETE CASCADE` and `ON UPDATE CASCADE`
- Transaction commit and rollback behavior
- Before/after transaction results
- Database reset and status checking

The application runs locally on a laptop and connects to a local PostgreSQL database.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Application / console interface |
| PostgreSQL | Relational database system |
| psycopg2 | Python PostgreSQL database driver |
| python-dotenv | Loads database credentials from `.env` |
| Colorama | Console color formatting |
| Tabulate | Clean table formatting in the console |
| GitHub | Source control and project submission |

---

## Repository Structure

```text
cs623-project/
├── sql/
│   ├── 00_create_database.sql
│   ├── 01_create_tables.sql
│   ├── 02_insert_data.sql
│   ├── 03_add_constraints.sql
│   └── 04_verify_setup.sql
│
├── src/
│   ├── __init__.py
│   ├── db.py
│   ├── demo.py
│   ├── display.py
│   ├── reset.py
│   ├── status.py
│   ├── transactions.py
│   └── ui.py
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

> Note: `.env` is used locally and should not be committed to GitHub.

---

## Database Design

The project uses three relations:

```text
Product(prodid, pname, price)
Depot(depid, addr, volume)
Stock(prodid, depid, quantity)
```

### Keys

| Table | Primary Key |
|---|---|
| Product | `prodid` |
| Depot | `depid` |
| Stock | `(prodid, depid)` |

### Foreign Keys

| Table | Column | References |
|---|---|---|
| Stock | `prodid` | Product(`prodid`) |
| Stock | `depid` | Depot(`depid`) |

### Reactive Constraint Behavior

The foreign keys use cascading behavior:

```sql
ON DELETE CASCADE
ON UPDATE CASCADE
```

This means:

- If a product is deleted, related stock rows are automatically deleted.
- If a depot is deleted, related stock rows are automatically deleted.
- If a product ID is changed, related stock rows are automatically updated.
- If a depot ID is changed, related stock rows are automatically updated.

---

## Data Dictionary

### Product

| Column | Description | Example |
|---|---|---|
| `prodid` | Product ID. Primary key. | `p1` |
| `pname` | Product name. | `tape` |
| `price` | Product price. | `2.50` |

### Depot

| Column | Description | Example |
|---|---|---|
| `depid` | Depot ID. Primary key. | `d1` |
| `addr` | Depot location/address. | `New York` |
| `volume` | Depot storage volume. | `9000` |

### Stock

| Column | Description | Example |
|---|---|---|
| `prodid` | Product ID. Foreign key to `Product`. | `p1` |
| `depid` | Depot ID. Foreign key to `Depot`. | `d1` |
| `quantity` | Quantity of product stored at depot. | `1000` |

---

## Original Data

The original project data is inserted by:

```text
sql/02_insert_data.sql
```

The application also uses this original data as the expected clean state when checking database status.

### Product

| prodid | pname | price |
|---|---|---:|
| p1 | tape | 2.50 |
| p2 | tv | 250.00 |
| p3 | vcr | 80.00 |

### Depot

| depid | addr | volume |
|---|---|---:|
| d1 | New York | 9000 |
| d2 | Syracuse | 6000 |
| d4 | New York | 2000 |

### Stock

| prodid | depid | quantity |
|---|---|---:|
| p1 | d1 | 1000 |
| p1 | d2 | -100 |
| p1 | d4 | 1200 |
| p2 | d1 | -400 |
| p2 | d2 | 2000 |
| p2 | d4 | 1500 |
| p3 | d1 | 3000 |
| p3 | d4 | 2000 |

---

## SQL Scripts

The `sql/` folder contains the database setup scripts.

| Script | Purpose |
|---|---|
| `00_create_database.sql` | Creates the project database. Usually run once manually. |
| `01_create_tables.sql` | Creates the `Product`, `Depot`, and `Stock` tables. |
| `02_insert_data.sql` | Inserts the original project data. |
| `03_add_constraints.sql` | Adds primary keys, foreign keys, and cascade behavior. |
| `04_verify_setup.sql` | Runs basic queries to verify setup. |

The constraints are intentionally stored in their own script so the schema creation, data insertion, and constraint logic are clearly separated.

---

## Python Application Structure

### `main.py`

Main entry point for the console application.

Responsibilities:

- Displays the main menu
- Handles user input
- Routes menu choices to the correct functions
- Shows before/after transaction output

### `src/db.py`

Handles PostgreSQL connection setup using values from `.env`.

### `src/display.py`

Displays the `Product`, `Depot`, and `Stock` tables using formatted console tables.

Also handles row-level change summaries:

- Green rows = added rows
- Red rows = removed rows

### `src/status.py`

Checks current database status.

It verifies:

- PostgreSQL connection
- Current user
- Current database
- Whether the project tables exist
- Whether table contents match the original expected data

Possible data states:

| Status | Meaning |
|---|---|
| `ORIGINAL` | Database matches the original project data. |
| `MODIFIED` | Database has changed from the original project data. |

### `src/reset.py`

Resets the database back to the original project state by rerunning the setup scripts:

```text
01_create_tables.sql
02_insert_data.sql
03_add_constraints.sql
```

### `src/transactions.py`

Contains the required transaction functions.

Each transaction uses:

```python
connection.commit()
```

if successful, or:

```python
connection.rollback()
```

if an error occurs.

### `src/demo.py`

Contains guided demo mode.

Guided demo mode resets the database before each transaction so every transaction starts from the same original state.

### `src/ui.py`

Centralizes console styling and color formatting.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd cs623-project
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the PostgreSQL database

If the database does not already exist, run the database creation script manually with an admin PostgreSQL user:

```bash
psql -U postgres -d postgres -f sql/00_create_database.sql
```

### 6. Create a project database user

The application is intended to run using a normal project user, not the PostgreSQL admin account.

Example:

```sql
CREATE ROLE cs623_user
WITH LOGIN
PASSWORD 'your_password_here'
NOSUPERUSER
NOCREATEDB
NOCREATEROLE;
```

If the database already exists, assign ownership or grant access as needed:

```sql
ALTER DATABASE cs623_project OWNER TO cs623_user;
GRANT CONNECT ON DATABASE cs623_project TO cs623_user;
```

Then connect to the project database and grant schema/table permissions:

```sql
\c cs623_project

GRANT USAGE, CREATE ON SCHEMA public TO cs623_user;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO cs623_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLES TO cs623_user;
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DB_NAME=cs623_project
DB_USER=cs623_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

Do not commit `.env` to GitHub.

The `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

---

## Running the Application

From the project root:

```bash
python main.py
```

The app opens a console menu.

---

## Console Menu Features

The main menu includes:

```text
1. Show all tables
2. Verify database status
3. Reset database to original state

Required Transactions
4. Delete product p1
5. Delete depot d1
6. Change product p1 to pp1
7. Change depot d1 to dd1
8. Add product p100 and stock row
9. Add depot d100 and stock row

Demo
10. Run guided demo mode
11. Run rollback/failure demo

0. Exit
```

---

## Required Transactions

The project implements six required transactions.

### Transaction 1: Delete product `p1`

Deletes product `p1` from `Product`.

Expected result:

- `p1` is removed from `Product`
- Related rows in `Stock` are automatically removed by `ON DELETE CASCADE`

---

### Transaction 2: Delete depot `d1`

Deletes depot `d1` from `Depot`.

Expected result:

- `d1` is removed from `Depot`
- Related rows in `Stock` are automatically removed by `ON DELETE CASCADE`

---

### Transaction 3: Change product `p1` to `pp1`

Updates the primary key value in `Product`.

Expected result:

- `Product.prodid` changes from `p1` to `pp1`
- Related `Stock.prodid` values are automatically updated by `ON UPDATE CASCADE`

---

### Transaction 4: Change depot `d1` to `dd1`

Updates the primary key value in `Depot`.

Expected result:

- `Depot.depid` changes from `d1` to `dd1`
- Related `Stock.depid` values are automatically updated by `ON UPDATE CASCADE`

---

### Transaction 5: Add product `p100` and stock row

Adds:

```text
Product: (p100, cd, 5)
Stock:   (p100, d2, 50)
```

Both inserts must succeed together. If either insert fails, the full transaction is rolled back.

---

### Transaction 6: Add depot `d100` and stock row

Adds:

```text
Depot: (d100, Chicago, 100)
Stock: (p1, d100, 100)
```

Both inserts must succeed together. If either insert fails, the full transaction is rolled back.

---

## Rollback / Failure Demo

The rollback demo intentionally creates a failing transaction.

It tries to:

1. Insert a valid product:

```text
Product: (p200, demo_item, 10)
```

2. Insert an invalid stock row:

```text
Stock: (p200, bad_depot, 25)
```

The second insert fails because `bad_depot` does not exist in `Depot`.

Because the transaction fails, Python calls:

```python
connection.rollback()
```

Expected result:

- The invalid stock row is not inserted
- The product `p200` is also undone
- The database remains unchanged

This demonstrates transaction atomicity: either the whole transaction succeeds, or none of it is kept.

---

## Reset Behavior

The required transactions are destructive. For example:

- deleting `p1` removes rows
- renaming `p1` changes keys
- inserting `p100` adds new data

Because of this, the application includes a reset option.

Resetting the database reruns:

```text
01_create_tables.sql
02_insert_data.sql
03_add_constraints.sql
```

This restores the database to the original project state.

Guided demo mode also resets the database before each transaction and performs a final reset at the end.

---

## Testing Checklist

Manual testing was used for this project.

### Basic App Test

- [ ] Run `python main.py`
- [ ] Confirm app opens without errors
- [ ] Confirm database connection shows `CONNECTED`
- [ ] Confirm menu displays correctly
- [ ] Confirm exit works

### Reset and Status Test

- [ ] Choose option `3`
- [ ] Type `RESET`
- [ ] Choose option `2`
- [ ] Confirm data status is `ORIGINAL`

### Individual Transaction Tests

For each transaction:

- [ ] Reset database first
- [ ] Run one transaction
- [ ] Confirm BEFORE table output appears
- [ ] Confirm AFTER table output appears
- [ ] Confirm change summary appears
- [ ] Confirm expected rows were added, removed, or updated

Transactions tested:

- [ ] Delete product `p1`
- [ ] Delete depot `d1`
- [ ] Change product `p1` to `pp1`
- [ ] Change depot `d1` to `dd1`
- [ ] Add product `p100` and stock row
- [ ] Add depot `d100` and stock row

### Guided Demo Test

- [ ] Choose option `10`
- [ ] Confirm all six transactions run
- [ ] Confirm each transaction starts with a reset
- [ ] Confirm final cleanup reset occurs
- [ ] Confirm database ends with status `ORIGINAL`

### Rollback Demo Test

- [ ] Choose option `11`
- [ ] Confirm intentional failure occurs
- [ ] Confirm rollback message appears
- [ ] Confirm no row-level changes are detected
- [ ] Confirm database status remains `ORIGINAL`

---

## Notes for Presentation

A suggested explanation for the project:

> This project uses Python as the application layer and PostgreSQL as the database layer. The Python console app connects to PostgreSQL, runs SQL transactions, and explicitly commits or rolls back changes. PostgreSQL enforces the primary keys, foreign keys, and cascading behavior. This keeps the database logic centered in the DBMS while Python provides a clean interface for demonstrating each transaction.

Important points to mention:

- The project is local, not cloud-based.
- The app is console-based, not a web app.
- The database uses primary keys and foreign keys.
- Cascading behavior is handled by PostgreSQL.
- Python controls commit and rollback behavior.
- Reset mode makes the demo repeatable.
- Guided demo mode walks through all required transactions.
- Rollback demo proves atomicity.

---

## Author

Gerard

CS623 - Database Management Systems
