from peewee import CharField, TextField, ForeignKeyField, BooleanField, IntegerField
from db.database import BaseModel, db

class Location(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class Player(BaseModel):
    name = CharField(max_length=100)
    health = IntegerField(default=100)

class Item(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class PlayerItem(BaseModel):
    player = ForeignKeyField(Player, backref='inventory_items')
    item = ForeignKeyField(Item, backref='inventories')
    quantity = IntegerField(default=1)
    
    class Meta:
        # Ensure a player can't have duplicate entries for the same item
        indexes = (
            (('player', 'item'), True),  # True makes it a unique index
        )

class NPC(BaseModel):
    name = CharField(max_length=100)
    description = TextField()
