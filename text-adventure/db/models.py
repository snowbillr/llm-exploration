from peewee import CharField, TextField, ForeignKeyField, BooleanField, IntegerField, DateTimeField
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

class Character(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class NarrativeSummary(BaseModel):
    note = TextField()  # A single narrative note
    timestamp = IntegerField()  # To track the order of narrative events
    player = ForeignKeyField(Player, backref='narrative_summaries', null=True)  # Optional reference to a player

class Message(BaseModel):
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ASSISTANT, 'Assistant')
    ]
    
    content = TextField()  # The content of the message
    role = CharField(max_length=10, choices=ROLE_CHOICES)  # Role of the message sender (user or assistant)
    timestamp = DateTimeField()  # When the message was sent
    player = ForeignKeyField(Player, backref='messages', null=True)  # Optional reference to a player

player_item_deferred.set_model(PlayerItem)
