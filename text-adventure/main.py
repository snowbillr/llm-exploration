import logging

from db.database import db
from scripts.manage_migrations import run_migrations
from db.models import Message, Player
from datetime import datetime

from agents import GameMasterAgent, InventoryAgent, NarrativeAgent, CharacterAgent
from game_loop import GameLoop

logging.basicConfig(level=logging.INFO, filename="development.log", filemode="w")


def get_game_master_context():
    pass

if __name__ == "__main__":
    run_migrations()
    try:
        GameLoop().run()
    finally:
        db.close()
