from playhouse.migrate import *
from migrations_config import db, migrator
from peewee import CharField, TextField, ForeignKeyField, BooleanField, IntegerField

def migrate_forward():
    # Create all tables
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        north_id INTEGER,
        east_id INTEGER,
        south_id INTEGER,
        west_id INTEGER,
        FOREIGN KEY (north_id) REFERENCES location (id),
        FOREIGN KEY (east_id) REFERENCES location (id),
        FOREIGN KEY (south_id) REFERENCES location (id),
        FOREIGN KEY (west_id) REFERENCES location (id)
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        current_location_id INTEGER NOT NULL,
        FOREIGN KEY (current_location_id) REFERENCES location (id)
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
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (player_id) REFERENCES player (id),
        FOREIGN KEY (item_id) REFERENCES item (id),
        UNIQUE (player_id, item_id)
    )
    ''')
    
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS npc (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        location_id INTEGER NOT NULL,
        FOREIGN KEY (location_id) REFERENCES location (id)
    )
    ''')

def migrate_backward():
    # Drop all tables in reverse order
    db.execute_sql('DROP TABLE IF EXISTS npc')
    db.execute_sql('DROP TABLE IF EXISTS inventory')
    db.execute_sql('DROP TABLE IF EXISTS item')
    db.execute_sql('DROP TABLE IF EXISTS player')
    db.execute_sql('DROP TABLE IF EXISTS location')
