from db.database import db
from scripts.manage_migrations import run_migrations

def main():
    run_migrations()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Close the database connection when the program exits
        db.close()
