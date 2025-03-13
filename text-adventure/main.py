from db.database import db
from scripts.manage_migrations import run_migrations
from db.models import Message, Player
from datetime import datetime

from agents import GameMasterAgent, InventoryAgent, NarrativeAgent, CharacterAgent

def main():
    run_migrations()

    game_master = GameMasterAgent()
    inventory_agent = InventoryAgent()
    character_agent = CharacterAgent()
    narrative_agent = NarrativeAgent()
    
    print("Welcome to the Fantasy Text Adventure!")
    print("Type 'quit' or 'exit' at any time to end the game.\n")

    print("Game Master: Welcome, brave adventurer! What is your name?")
    
    player_name = input("\nYou: ")
    player = Player.create(name=player_name)
    
    print(f"\nGame Master: Welcome, {player_name}! Your adventure begins now.")

    # starting prompt
    
    playing = True
    while playing:
        player_input = input("\nYou: ")

        if player_input.lower() in ["quit", "exit"]:
            print("\nThank you for playing! Goodbye.")
            playing = False
            continue
        
        Message.create(
            content=player_input,
            role=Message.ROLE_USER,
            timestamp=datetime.now(),
            player=player
        )

        narrative_context = narrative_agent.get_narrative_context(player_id=player.id)
        # character_context = character_agent.get_character_context(player_id=player.id)
        # inventory_context = inventory_agent.get_inventory_context(player_id=player.id)
        character_context = ""
        inventory_context = ""
        last_messages = [
            "{message.role}: {message.content}"
            for message
            in Message.select().where(Message.player == player.id).order_by(Message.timestamp.desc()).limit(3)
        ]

        message = """
NARRATIVE_CONTEXT: {narrative_context}

CHARACTER_CONTEXT: {character_context}

INVENTORY_CONTEXT: {inventory_context}

LAST_MESSAGES: {last_messages}
"""

        game_master_response_text = game_master.chat([
            { "role": "assistant", "content": message },
            { "role": "user", "content": player_input }
        ])['message']['content']

        Message.create(
            content=game_master_response_text,
            role=Message.ROLE_ASSISTANT,
            timestamp=datetime.now(),
            player=player
        )

        narrative_agent.update_narrative_context(game_master_message=game_master_response_text, player_message=player_input, player_id=player.id)
        # character_agent.update_character_context(game_master_message=game_master_response_text, player_message=player_input, player_id=player.id)
        # inventory_agent.update_inventory_context(game_master_message=game_master_response_text, player_message=player_input, player_id=player.id)

        print(f"Game Master: {game_master_response_text}")

def get_game_master_context():
    pass

if __name__ == "__main__":
    try:
        main()
    finally:
        db.close()
