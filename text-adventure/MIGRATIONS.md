# Peewee Migrations Guide

This project uses Peewee's `playhouse.migrate` module to manage database migrations. This document explains how to use the migration system.

## Migration Files

Migration files are stored in the `migrations/` directory and are Python scripts that define how to apply and revert database changes. Each migration file has two main functions:

- `migrate_forward()`: Applies the migration changes to the database
- `migrate_backward()`: Reverts the migration changes (optional but recommended)

## Managing Migrations

The `manage_migrations.py` script provides commands to create and run migrations.

### Creating a New Migration

To create a new migration, run:

```bash
uv run manage_migrations.py create migration_name
```

This will create a new migration file in the `migrations/` directory with a timestamp prefix.

### Running Migrations

To apply all pending migrations, run:

```bash
uv run manage_migrations.py migrate
```

### Reverting the Last Migration

To revert the most recently applied migration, run:

```bash
uv run manage_migrations.py migrate --backward
```

## Example Migration

Here's an example of a migration that adds a new column to a table:

```python
from playhouse.migrate import *
from migrations_config import db, migrator

def migrate_forward():
    # Add a new column to the player table
    migrate(
        migrator.add_column('player', 'experience', IntegerField(default=0)),
    )

def migrate_backward():
    # Remove the column from the player table
    migrate(
        migrator.drop_column('player', 'experience'),
    )
```

## Common Migration Operations

Here are some common migration operations:

### Adding a Column

```python
migrate(
    migrator.add_column('table_name', 'column_name', ColumnType(default='default_value')),
)
```

### Removing a Column

```python
migrate(
    migrator.drop_column('table_name', 'column_name'),
)
```

### Renaming a Column

```python
migrate(
    migrator.rename_column('table_name', 'old_name', 'new_name'),
)
```

### Changing a Column Type

```python
migrate(
    migrator.drop_column('table_name', 'column_name'),
    migrator.add_column('table_name', 'column_name', NewColumnType()),
)
```

### Adding an Index

```python
migrate(
    migrator.add_index('table_name', ('column1', 'column2'), unique=True),
)
```

### Removing an Index

```python
migrate(
    migrator.drop_index('table_name', 'index_name'),
)
```

## Best Practices

1. Always create a `migrate_backward()` function to allow reverting migrations
2. Keep migrations small and focused on a single change
3. Test migrations on a development database before applying to production
4. Never modify existing migration files after they've been applied
5. Use descriptive names for migration files
