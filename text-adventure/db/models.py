from peewee import CharField, TextField, ForeignKeyField, BooleanField, IntegerField
from playhouse.shortcuts import ManyToManyField, DeferredThroughModel
from db.database import BaseModel

player_item_deferred = DeferredThroughModel()

class Location(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class Item(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class Player(BaseModel):
    name = CharField(max_length=100)
    health = IntegerField(default=100)
    # Define the many-to-many relationship
    items = ManyToManyField(
        model=Item,
        backref='players',
        through_model=player_item_deferred
    )

class PlayerItem(BaseModel):
    player = ForeignKeyField(Player, backref='player_items')
    item = ForeignKeyField(Item, backref='player_items')
    quantity = IntegerField(default=1)
    
    class Meta:
        # Ensure a player can't have duplicate entries for the same item
        indexes = (
            (('player', 'item'), True),  # True makes it a unique index
        )

class NPC(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class NarrativeSummary(BaseModel):
    summary = TextField()  # Concise summary of recent events
    key_developments = TextField()  # Serialized list of key developments
    active_goals = TextField()  # Serialized list of active quests/goals
    timestamp = IntegerField()  # To track the order of narrative events
    player = ForeignKeyField(Player, backref='narrative_summaries', null=True)  # Optional reference to a player

player_item_deferred.set_model(PlayerItem)
