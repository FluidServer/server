import os, time, pathlib
import sqlite3

os.system("clear")

print("\n  \033[38;2;0;170;255mF\033[38;2;0;175;255ml\033[38;2;0;180;255mu\033[38;2;0;185;255mi\033[38;2;0;190;255md\033[38;2;0;195;255mS\033[38;2;0;200;255me\033[38;2;0;205;255mr\033[38;2;0;210;255mv\033[38;2;0;215;255me\033[38;2;0;220;255mr\033[0m")

my_file = pathlib.Path(os.getcwd() + "/db")
if my_file.is_dir():
    pass
else:
    print("\n   DB folder doesn't exist!\n")
    exit(1)

my_file = pathlib.Path(os.getcwd() + "/db/db.db")
if my_file.is_file():
    print("\n   DB already exists!\n")
    exit(1)
else:
    pass

print("\n   Welcome to the database setup for FluidServer")
print("\n   This assitant will help you\n   setup the database for FluidServer.")
print("\n")
confirmationForStart = input("   Do you want to create a database (y/N)? ")
print("\n")

if confirmationForStart.lower() == "y":
    print("   Okay! Just a few more questions and everything\n   will be set up!")
    print("\n")
else:
    exit(0)

time.sleep(3)

os.system("clear")

print("\n   Do you want to create the database?\n")
print("\n   What will happen:")
print("\n     - A database will be created with the tables:")
print("       controlled, place, products, stock, users")
print("       in db/db.db, with default data.")

databaseCreationConfirmation = input("\n   Create database (y/N)? ")
print("")

if databaseCreationConfirmation.lower() == "y":
    print("   Okay! The database will now be created under db.db")
    print("\n")
else:
    exit(0)

print("   Creating database in 3.")
time.sleep(1)
print("   Creating database in 2..")
time.sleep(1)
print("   Creating database in 1...")
time.sleep(1)

def createDb(name):
    conn = None
    try:
        conn = sqlite3.connect(name)
        print("   (TEST) SQLite version " + sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print("Something went wrong!")
        print(e)
    finally:
        if conn:
            conn.close()

databaseFile = pathlib.Path(os.getcwd() + "/db/db.db")
print("   Creating database in " + str(databaseFile))

createDb(databaseFile)

def createTables():
    sql_statements = [ 
        """CREATE TABLE IF NOT EXISTS controlled (
                Barcode int, 
                IsControl int
        );""",
        """CREATE TABLE IF NOT EXISTS place (
                Barcode int,
                Place varchar(512)
        );""",
        """CREATE TABLE IF NOT EXISTS products (
                Barcode int,
                Name varchar(512),
                PriceUn int,
                BaseType int
        );""",
        """CREATE TABLE IF NOT EXISTS stock (
                Barcode int,
                InStock int
        );""",
        """CREATE TABLE IF NOT EXISTS users (
                UserID int,
                Name varchar(255)
        );"""]

    # create a database connection
    try:
        with sqlite3.connect(databaseFile) as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            
            conn.commit()
    except sqlite3.Error as e:
        print(e)
        

createTables()

def insertDefaultData():
    sql_statements = [ 
        """INSERT INTO controlled (Barcode, IsControl)
        VALUES ('1', '0');""",
        """INSERT INTO place (Barcode, Place)
        VALUES ('1', 'A1:1');""",
        """INSERT INTO products (Barcode, Name, PriceUn, BaseType)
        VALUES ('1', 'Test Product', '1,00', '0');""",
        """INSERT INTO stock (Barcode, InStock)
        VALUES ('1', '400');""",
        """INSERT INTO users (UserID, Name)
        VALUES ('1', 'clue')"""]

    # create a database connection
    try:
        with sqlite3.connect(databaseFile) as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            
            conn.commit()
    except sqlite3.Error as e:
        print(e)