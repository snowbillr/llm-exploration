import os
from peewee import SqliteDatabase
from playhouse.migrate import SqliteMigrator

# Database configuration
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'text_adventure.db')
db = SqliteDatabase(DB_PATH)
migrator = SqliteMigrator(db)

# Migrations directory
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations')

# Create migrations directory if it doesn't exist
if not os.path.exists(MIGRATIONS_DIR):
    os.makedirs(MIGRATIONS_DIR)
