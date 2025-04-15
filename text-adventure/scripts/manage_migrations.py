#!/usr/bin/env python
import os
import importlib.util
import datetime
import argparse

from db.database import db
from db.migrations_config import MIGRATIONS_DIR

def create_migration(name):
    """Create a new migration file"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{name}.py"
    filepath = os.path.join(MIGRATIONS_DIR, filename)
    
    # Create migration template
    with open(filepath, 'w') as f:
        f.write("""from playhouse.migrate import *
from db.migrations_config import migrator
from db.database import db

def migrate_forward():
    # Write your forward migration here
    # Example:
    # migrate(
    #     migrator.add_column('table_name', 'column_name', CharField(default='')),
    # )
    pass

def migrate_backward():
    # Write your backward migration here (optional)
    # Example:
    # migrate(
    #     migrator.drop_column('table_name', 'column_name'),
    # )
    pass
""")
    
    print(f"Created migration: {filepath}")

def run_migrations(direction='forward'):
    """Run all migrations in the specified direction"""
    # Get all migration files
    migration_files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.py')])
    
    if not migration_files:
        print("No migrations found.")
        return
    
    # Connect to the database
    db.connect()
    
    # Create migrations table if it doesn't exist
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        applied_at TIMESTAMP NOT NULL
    )
    ''')
    
    # Get applied migrations
    applied_migrations = [row[0] for row in db.execute_sql('SELECT name FROM migrations').fetchall()]
    
    if direction == 'forward':
        # Apply migrations that haven't been applied yet
        for migration_file in migration_files:
            if migration_file not in applied_migrations:
                print(f"Applying migration: {migration_file}")
                
                # Import the migration module
                spec = importlib.util.spec_from_file_location(
                    migration_file.replace('.py', ''),
                    os.path.join(MIGRATIONS_DIR, migration_file)
                )
                migration_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration_module)
                
                # Run the migration
                migration_module.migrate_forward()
                
                # Record the migration
                db.execute_sql(
                    'INSERT INTO migrations (name, applied_at) VALUES (?, ?)',
                    (migration_file, datetime.datetime.now())
                )
                
                print(f"Successfully applied migration: {migration_file}")
    
    elif direction == 'backward':
        # Revert the last applied migration
        if applied_migrations:
            last_migration = applied_migrations[-1]
            print(f"Reverting migration: {last_migration}")
            
            # Import the migration module
            spec = importlib.util.spec_from_file_location(
                last_migration.replace('.py', ''),
                os.path.join(MIGRATIONS_DIR, last_migration)
            )
            migration_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration_module)
            
            # Run the backward migration
            migration_module.migrate_backward()
            
            # Remove the migration record
            db.execute_sql('DELETE FROM migrations WHERE name = ?', (last_migration,))
            
            print(f"Successfully reverted migration: {last_migration}")
        else:
            print("No migrations to revert.")
    
    # Close the database connection
    db.close()

def main():
    parser = argparse.ArgumentParser(description='Manage database migrations')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create migration command
    create_parser = subparsers.add_parser('create', help='Create a new migration')
    create_parser.add_argument('name', help='Name of the migration')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run migrations')
    migrate_parser.add_argument('--backward', action='store_true', help='Revert the last migration')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_migration(args.name)
    elif args.command == 'migrate':
        direction = 'backward' if args.backward else 'forward'
        run_migrations(direction)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
