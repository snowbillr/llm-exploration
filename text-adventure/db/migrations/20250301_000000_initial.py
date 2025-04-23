from playhouse.migrate import *
from db.database import db

def migrate_forward():
    # Create tables with explicit SQL rather than using model classes
    db.execute_sql('''
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL
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
        health INTEGER DEFAULT 100
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
        description TEXT NOT NULL
    )
    ''')

def migrate_backward():
    # Drop tables in reverse dependency order
    db.execute_sql('DROP TABLE IF EXISTS player_item')
    db.execute_sql('DROP TABLE IF EXISTS character')
    db.execute_sql('DROP TABLE IF EXISTS player')
    db.execute_sql('DROP TABLE IF EXISTS item')
    db.execute_sql('DROP TABLE IF EXISTS location')
