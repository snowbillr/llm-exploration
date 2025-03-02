import os
import sys
from models import seed_database
from database import db
from manage_migrations import run_migrations

def main():
    """Initialize the database with migrations and seed it with sample data"""
    # Run migrations
    run_migrations()
    
    # Seed the database with sample data
    seed_database()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Close the database connection when the program exits
        db.close()
