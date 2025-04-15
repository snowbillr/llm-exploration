# Database Migrations

This project uses a model-migration separation approach for database migrations.

## Migration Philosophy

1. **Models reflect current state**: The models in `db/models.py` always reflect the current state of the database schema after all migrations have been applied.

2. **Migrations define the path**: Migrations define how to get from one schema version to the next.

3. **Explicit initial schema**: The initial migration creates tables with explicitly defined columns, not based on the current model definitions.

4. **Incremental changes**: Subsequent migrations use the migrator to make incremental changes to the schema.

## Creating a New Migration

To create a new migration:

```bash
uv run -m scripts.manage_migrations create migration_name
```

Then edit the generated migration file to define your schema changes.

## Running Migrations

To apply all pending migrations:

```bash
uv run -m scripts.manage_migrations migrate
```

To revert the last applied migration:

```bash
uv run -m scripts.manage_migrations migrate --backward
```

## Migration Best Practices

1. Always create a migration for schema changes, never modify the models without a corresponding migration.
2. Keep migrations small and focused on a single change.
3. Always implement both forward and backward migrations.
4. Test migrations thoroughly before applying them to production.

## Example: Adding a New Column

When you need to add a new column to an existing table, create a migration like this:

```python
# Example: db/migrations/YYYYMMDD_HHMMSS_add_player_level.py
from playhouse.migrate import *
from db.migrations_config import migrator
from peewee import IntegerField

def migrate_forward():
    migrate(
        migrator.add_column('player', 'level', IntegerField(default=1)),
    )

def migrate_backward():
    migrate(
        migrator.drop_column('player', 'level'),
    )
```

## Handling Database Recreation

With this approach, if the database is ever deleted and recreated:

1. The initial migration will create tables with only the original columns.
2. Subsequent migrations will add any additional columns.
3. No conflicts will occur because the initial migration doesn't use the current model definitions.
