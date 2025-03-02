from playhouse.migrate import *
from db.migrations_config import db, migrator

def migrate_forward():
    # Add a health field to the player table
    migrate(
        migrator.add_column('player', 'health', IntegerField(default=100)),
    )

def migrate_backward():
    # Remove the health field from the player table
    migrate(
        migrator.drop_column('player', 'health'),
    )
