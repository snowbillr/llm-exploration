import os
from peewee import Model, SqliteDatabase

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DB_PATH = os.path.join(DB_DIR, 'text_adventure.db')

os.makedirs(DB_DIR, exist_ok=True)

db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    """A base model that will use our SQLite database"""
    class Meta:
        database = db
        legacy_table_names = False
