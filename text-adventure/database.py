from peewee import Model
from migrations_config import db

class BaseModel(Model):
    """A base model that will use our SQLite database"""
    class Meta:
        database = db
