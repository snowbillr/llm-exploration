from playhouse.migrate import *
from db.database import db

def migrate_forward():
    # Create the message table
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY,
        content TEXT NOT NULL,
        role VARCHAR(10) NOT NULL,
        timestamp DATETIME NOT NULL,
        player_id INTEGER,
        FOREIGN KEY (player_id) REFERENCES player (id)
    )
    ''')

def migrate_backward():
    # Drop the message table
    db.execute_sql('DROP TABLE IF EXISTS message')
