from peewee import CharField, TextField, ForeignKeyField, BooleanField, IntegerField
from db.database import BaseModel, db

class Location(BaseModel):
    name = CharField(max_length=100)
    description = TextField()
    north = ForeignKeyField('self', backref='south_of', null=True)
    east = ForeignKeyField('self', backref='west_of', null=True)
    south = ForeignKeyField('self', backref='north_of', null=True)
    west = ForeignKeyField('self', backref='east_of', null=True)

class Player(BaseModel):
    name = CharField(max_length=100)
    current_location = ForeignKeyField(Location, backref='players')
    health = IntegerField(default=100)

class Item(BaseModel):
    name = CharField(max_length=100)
    description = TextField()

class Inventory(BaseModel):
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
    location = ForeignKeyField(Location, backref='npcs')

def initialize_database():
    """Create database tables"""
    # Create tables
    db.connect()
    db.create_tables([Location, Player, Item, Inventory, NPC])

def seed_database():
    """Initialize the database with sample data"""
    # Check if we already have data
    if Location.select().count() > 0:
        return
    
    # Create sample locations
    forest = Location.create(
        name="Forest",
        description="A dense forest with tall trees. Sunlight filters through the leaves."
    )
    
    cave = Location.create(
        name="Cave",
        description="A dark, damp cave. You can hear water dripping somewhere."
    )
    
    meadow = Location.create(
        name="Meadow",
        description="A beautiful meadow filled with wildflowers."
    )
    
    # Set up connections between locations
    forest.east = meadow
    forest.save()
    
    meadow.west = forest
    meadow.north = cave
    meadow.save()
    
    cave.south = meadow
    cave.save()
    
    # Create a player
    player = Player.create(
        name="Adventurer",
        current_location=forest
    )
    
    # Create some items
    sword = Item.create(
        name="Sword",
        description="A sharp steel sword."
    )
    
    lantern = Item.create(
        name="Lantern",
        description="A lantern that provides light in dark places."
    )
    
    treasure = Item.create(
        name="Treasure Chest",
        description="A locked chest that seems to contain something valuable."
    )
    
    # Add an item to player's inventory as an example
    Inventory.create(
        player=player,
        item=sword,
        quantity=1
    )
    
    # Create an NPC
    NPC.create(
        name="Old Wizard",
        description="An elderly wizard with a long white beard.",
        location=meadow
    )
    
    NPC.create(
        name="Cave Troll",
        description="A large, menacing troll guarding the treasure.",
        location=cave
    )
