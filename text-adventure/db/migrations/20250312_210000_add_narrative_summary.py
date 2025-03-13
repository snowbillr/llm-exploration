from playhouse.migrate import *
from db.database import db

def migrate_forward():
    # Create the narrative_summary table
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS narrative_summary (
        id INTEGER PRIMARY KEY,
        summary TEXT NOT NULL,
        key_developments TEXT NOT NULL,
        active_goals TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        player_id INTEGER,
        FOREIGN KEY (player_id) REFERENCES player (id)
    )
    ''')

def migrate_backward():
    # Drop the narrative_summary table
    db.execute_sql('DROP TABLE IF EXISTS narrative_summary')
