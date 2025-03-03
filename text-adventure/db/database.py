import os
from peewee import Model, SqliteDatabase

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'text_adventure.db')
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    """A base model that will use our SQLite database"""
    class Meta:
        database = db
