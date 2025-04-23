import logging

from db.database import db
from scripts.manage_migrations import run_migrations

from textual_app import TextAdventureApp

logging.basicConfig(level=logging.INFO, filename="development.log", filemode="w")

if __name__ == "__main__":
    run_migrations()

    try:
        TextAdventureApp().run()
    finally:
        db.close()
