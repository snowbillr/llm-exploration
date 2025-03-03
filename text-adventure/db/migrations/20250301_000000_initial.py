from playhouse.migrate import *

from db.database import db
from db.models import NPC, PlayerItem, Item, Location, Player

def migrate_forward():
    db.create_tables([Location, Player, Item, PlayerItem, NPC])

def migrate_backward():
    db.drop_tables([Location, Player, Item, PlayerItem, NPC])
