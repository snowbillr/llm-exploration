import os
from playhouse.migrate import SqliteMigrator

from db.database import db

# Database configuration
migrator = SqliteMigrator(db)

# Migrations directory
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations')
