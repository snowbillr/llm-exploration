from playhouse.migrate import *
from db.database import db

def migrate_forward():
    # Create tables with explicit SQL rather than using model classes
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        game_id INTEGER,
        FOREIGN KEY (game_id) REFERENCES game (id)
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        health INTEGER DEFAULT 100,
        game_id INTEGER,
        FOREIGN KEY (game_id) REFERENCES game (id)
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS player_item (
        id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (player_id) REFERENCES player (id),
        FOREIGN KEY (item_id) REFERENCES item (id),
        UNIQUE (player_id, item_id)
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS character (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        game_id INTEGER,
        FOREIGN KEY (game_id) REFERENCES game (id)
    )
    ''')

    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS narrative_summary (
        id INTEGER PRIMARY KEY,
        note TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        game_id INTEGER,
        FOREIGN KEY (game_id) REFERENCES game (id)
    )
    ''')

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

    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS game (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL
    )
    ''')


def migrate_backward():
    # Drop tables in reverse dependency order
    db.execute_sql('DROP TABLE IF EXISTS player_item')
    db.execute_sql('DROP TABLE IF EXISTS character')
    db.execute_sql('DROP TABLE IF EXISTS player')
    db.execute_sql('DROP TABLE IF EXISTS item')
    db.execute_sql('DROP TABLE IF EXISTS location')
    db.execute_sql('DROP TABLE IF EXISTS narrative_summary')
    db.execute_sql('DROP TABLE IF EXISTS message')
    db.execute_sql('DROP TABLE IF EXISTS game')
