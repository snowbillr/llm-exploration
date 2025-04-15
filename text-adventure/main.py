import logging

from db.database import db
from scripts.manage_migrations import run_migrations
from db.models import Message, Player
from datetime import datetime

from agents import GameMasterAgent, InventoryAgent, NarrativeAgent, CharacterAgent
from textual_app import TextAdventureApp

logging.basicConfig(level=logging.INFO, filename="development.log", filemode="w")


def get_game_master_context():
    pass

if __name__ == "__main__":
    run_migrations()
    try:
        TextAdventureApp().run()
    finally:
        db.close()
