from playhouse.migrate import *
from db.database import db

def migrate_forward():
    migrator = SqliteMigrator(db)
    # 1. Rename the old column
    migrate(
        migrator.rename_column('narrative_summary', 'key_developments', 'note')
    )
    # Optionally, if you want to handle data migration, you could do so here.
    # But if you already migrated the code, new rows will be correct.


def migrate_backward():
    migrator = SqliteMigrator(db)
    migrate(
        migrator.rename_column('narrative_summary', 'note', 'key_developments')
    )
