from db.database import db
from scripts.manage_migrations import run_migrations
from agents.game_master.agent import GameMasterAgent

def main():
    run_migrations()

    # Initialize the GameMasterAgent
    game_master = GameMasterAgent()
    
    # Initialize message history
    messages = []
    
    # Display welcome message
    print("Welcome to the Fantasy Text Adventure!")
    print("Type 'quit' or 'exit' at any time to end the game.\n")
    
    # Game loop
    playing = True
    while playing:
        # Get response from GameMasterAgent if we have messages
        if messages:
            response = game_master.chat(messages)
            gm_response = response["message"]["content"]
            print(f"\nGame Master: {gm_response}")
            
            # Add GM response to history
            messages.append({"role": "assistant", "content": gm_response})
        else:
            # Initial prompt from the game master
            print("Game Master: Welcome, brave adventurer! What is your name?")
        
        # Get player input
        player_input = input("\nYou: ")
        
        # Check if player wants to quit
        if player_input.lower() in ["quit", "exit"]:
            print("\nThank you for playing! Goodbye.")
            playing = False
            continue
        
        # Add player message to history
        messages.append({"role": "user", "content": player_input})


if __name__ == "__main__":
    try:
        main()
    finally:
        # Close the database connection when the program exits
        db.close()
