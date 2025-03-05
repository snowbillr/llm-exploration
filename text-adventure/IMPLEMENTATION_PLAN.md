# Implementation Plan: Multi-Agent Architecture for Text Adventure

## Overview
This document outlines the implementation plan for enhancing the text adventure game with a multi-agent architecture to improve memory management and context retention.

## Current Limitations
- Single GameMasterAgent struggles to remember story details and characters
- No persistent storage of game state beyond basic database models
- Context window limitations of the language model

## Proposed Solution
Split functionality into specialized agents:
1. Game Master Agent (enhanced)
2. Inventory Agent
3. Narrative Agent
4. Character Agent

## Implementation Steps

### Phase 1: Agent Structure Setup
- [x] Create directory structure for new agents
- [x] Implement base classes and system prompts for each agent
- [x] Enhance GameMasterAgent's system prompt and class structure to prepare for specialized agent coordination

### Phase 2: Database Enhancements
- [ ] Add NarrativeSummary model for storing story summaries
- [ ] Add CharacterMemory model for detailed NPC tracking
- [ ] Add Message model for storing all player-GM interactions
- [ ] Update database migration scripts

### Phase 3: Agent Communication System
- [ ] Implement tool-based communication using ollama-python's `tools` parameter
- [ ] Define specific tools for each specialized agent (inventory management, character tracking, etc.)
- [ ] Create message routing system to send GameMaster responses to specialized agents
- [ ] Implement tool execution logic for each agent to update the database
- [ ] Create context enhancement system for GameMasterAgent
- [ ] Develop periodic summarization logic for NarrativeAgent
- [ ] Implement error handling for tool calls and API failures

### Phase 4: Integration and Testing
- [ ] Update main game loop to incorporate all agents
- [ ] Implement context window management
- [ ] Test with complex scenarios to verify memory improvements

## Detailed Implementation

### 1. Agent Structure and System Prompts

#### GameMasterAgent (Enhanced)
- **Purpose**: Primary storyteller and player interface
- **System Prompt Updates**:
  - Add instructions for delegating to specialized agents
  - Include guidance on using summaries and context
- **Implementation Details**:
  - Modify to accept enhanced context from other agents
  - Update chat method to incorporate specialized knowledge

#### InventoryAgent
- **Purpose**: Track and manage player inventory
- **System Prompt**:
  - Instructions for identifying item interactions
  - Guidelines for maintaining inventory state
  - Format for inventory summaries
- **Implementation Details**:
  - Methods for adding, removing, and updating items
  - Database interaction with PlayerItem model
  - Inventory summary generation

#### NarrativeAgent
- **Purpose**: Summarize and track story progression
- **System Prompt**:
  - Instructions for identifying key plot points
  - Guidelines for creating concise summaries
  - Format for narrative continuity
- **Implementation Details**:
  - Periodic summary generation
  - Storage of summaries in database
  - Retrieval of relevant summaries for context

#### CharacterAgent
- **Purpose**: Track and remember NPCs
- **System Prompt**:
  - Instructions for identifying character interactions
  - Guidelines for tracking character traits and relationships
  - Format for character summaries
- **Implementation Details**:
  - NPC identification and tracking
  - Storage of character details in database
  - Character context generation

### 2. Database Enhancements

```python
# New models to add

class NarrativeSummary(BaseModel):
    """Stores narrative summaries created by the Narrative Agent"""
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    
class CharacterMemory(BaseModel):
    """Stores detailed information about NPCs encountered"""
    npc = ForeignKeyField(NPC, backref='memories')
    details = TextField()  # JSON or structured text about the character
    last_updated = DateTimeField(default=datetime.datetime.now)
    
class Message(BaseModel):
    """Stores all messages exchanged between player and game master"""
    player = ForeignKeyField(Player, backref='messages')
    role = CharField(max_length=20)  # 'user' or 'assistant'
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
```

### 3. Main Game Loop Updates

```python
def main():
    # Initialize all agents
    game_master = GameMasterAgent()
    inventory_agent = InventoryAgent()
    narrative_agent = NarrativeAgent()
    character_agent = CharacterAgent()
    
    # Initialize message history
    messages = []
    
    # Game loop
    playing = True
    message_count = 0
    
    while playing:
        # Get response from GameMasterAgent if we have messages
        if messages:
            # Enhance context with specialized agent knowledge
            recent_summaries = get_recent_narrative_summaries(3)
            character_context = character_agent.get_relevant_characters(messages[-5:])
            inventory_context = inventory_agent.get_inventory_summary()
            
            enhanced_context = f"""
            Recent Story Summary: {recent_summaries}
            
            Character Information: {character_context}
            
            Current Inventory: {inventory_context}
            """
            
            # Add enhanced context as a system message
            context_message = {"role": "system", "content": enhanced_context}
            context_enhanced_messages = messages[-10:] + [context_message]
            
            # Define tools for the GameMaster to use
            gm_tools = [
                # Tools for delegating to specialized agents
                {
                    "type": "function",
                    "function": {
                        "name": "update_inventory",
                        "description": "Update player inventory when items are acquired, used, or lost",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["add", "remove", "use"],
                                    "description": "The action to perform on the inventory"
                                },
                                "item": {
                                    "type": "string",
                                    "description": "The name of the item"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "The quantity of the item (default: 1)"
                                }
                            },
                            "required": ["action", "item"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_character_memory",
                        "description": "Update information about an NPC character",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "character_name": {
                                    "type": "string",
                                    "description": "The name of the NPC"
                                },
                                "details": {
                                    "type": "string",
                                    "description": "New information about the character"
                                }
                            },
                            "required": ["character_name", "details"]
                        }
                    }
                }
            ]
            
            # Get response from game master with tools
            response = game_master.chat(
                context_enhanced_messages,
                tools=gm_tools
            )
            
            # Process any tool calls from the response
            if "tool_calls" in response:
                for tool_call in response["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    arguments = json.loads(tool_call["function"]["arguments"])
                    
                    if tool_name == "update_inventory":
                        inventory_agent.handle_inventory_update(
                            arguments["action"],
                            arguments["item"],
                            arguments.get("quantity", 1)
                        )
                    elif tool_name == "update_character_memory":
                        character_agent.update_character_memory(
                            arguments["character_name"],
                            arguments["details"]
                        )
            
            gm_response = response["message"]["content"]
            print(f"\nGame Master: {gm_response}")
            
            # Route the GM response to specialized agents for processing with their tools
            inventory_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "add_item",
                        "description": "Add an item to the player's inventory",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "item_name": {"type": "string"},
                                "quantity": {"type": "integer"}
                            },
                            "required": ["item_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "remove_item",
                        "description": "Remove an item from the player's inventory",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "item_name": {"type": "string"},
                                "quantity": {"type": "integer"}
                            },
                            "required": ["item_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "use_item",
                        "description": "Mark an item as used in the player's inventory",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "item_name": {"type": "string"}
                            },
                            "required": ["item_name"]
                        }
                    }
                }
            ]
            
            # Process GM response with inventory agent
            inventory_response = inventory_agent.process_message_with_tools(
                gm_response,
                tools=inventory_tools
            )
            
            # Handle any inventory tool calls
            if "tool_calls" in inventory_response:
                for tool_call in inventory_response["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    arguments = json.loads(tool_call["function"]["arguments"])
                    
                    if tool_name == "add_item":
                        inventory_agent.add_item(
                            arguments["item_name"],
                            arguments.get("quantity", 1)
                        )
                    elif tool_name == "remove_item":
                        inventory_agent.remove_item(
                            arguments["item_name"],
                            arguments.get("quantity", 1)
                        )
                    elif tool_name == "use_item":
                        inventory_agent.use_item(arguments["item_name"])
            
            # Similar processing for character agent with its own tools
            character_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "update_character",
                        "description": "Update information about an NPC",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "character_name": {"type": "string"},
                                "details": {"type": "string"}
                            },
                            "required": ["character_name", "details"]
                        }
                    }
                }
            ]
            
            character_response = character_agent.process_message_with_tools(
                gm_response,
                tools=character_tools
            )
            
            # Handle any character tool calls
            if "tool_calls" in character_response:
                for tool_call in character_response["tool_calls"]:
                    if tool_call["function"]["name"] == "update_character":
                        arguments = json.loads(tool_call["function"]["arguments"])
                        character_agent.update_character_memory(
                            arguments["character_name"],
                            arguments["details"]
                        )
            
            # Process GM response with narrative agent
            narrative_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "create_narrative_summary",
                        "description": "Create a summary of recent narrative events",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "The narrative summary content"
                                },
                                "tags": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "Tags to categorize the summary"
                                }
                            },
                            "required": ["content"]
                        }
                    }
                }
            ]
            
            narrative_response = narrative_agent.process_message_with_tools(
                gm_response,
                tools=narrative_tools
            )
            
            # Handle any narrative tool calls
            if "tool_calls" in narrative_response:
                for tool_call in narrative_response["tool_calls"]:
                    if tool_call["function"]["name"] == "create_narrative_summary":
                        arguments = json.loads(tool_call["function"]["arguments"])
                        summary = arguments["content"]
                        tags = arguments.get("tags", [])
                        
                        # Save the summary with tags if provided
                        if tags:
                            narrative_agent.tag_summary(summary, tags)
                        else:
                            save_narrative_summary(summary)
            
            # Add GM response to history and save to database
            messages.append({"role": "assistant", "content": gm_response})
            save_message_to_database(player.id, "assistant", gm_response)
            
            # Periodically create narrative summaries if not already created by tools
            message_count += 1
            if message_count % 10 == 0 and "tool_calls" not in narrative_response:  # Every 10 messages
                narrative_summary = narrative_agent.create_summary(messages[-20:])
                save_narrative_summary(narrative_summary)
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
        
        # Add player message to history and save to database
        messages.append({"role": "user", "content": player_input})
        save_message_to_database(player.id, "user", player_input)
        
        # Process player input with specialized agents using tools
        # Similar tool processing as with GM responses
        inventory_response = inventory_agent.process_message_with_tools(
            player_input,
            tools=inventory_tools
        )
        
        # Handle any inventory tool calls from player input
        if "tool_calls" in inventory_response:
            for tool_call in inventory_response["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                
                if tool_name == "add_item":
                    inventory_agent.add_item(
                        arguments["item_name"],
                        arguments.get("quantity", 1)
                    )
                elif tool_name == "remove_item":
                    inventory_agent.remove_item(
                        arguments["item_name"],
                        arguments.get("quantity", 1)
                    )
                elif tool_name == "use_item":
                    inventory_agent.use_item(arguments["item_name"])
        
        # Process player input with character agent
        character_response = character_agent.process_message_with_tools(
            player_input,
            tools=character_tools
        )
        
        # Handle any character tool calls from player input
        if "tool_calls" in character_response:
            for tool_call in character_response["tool_calls"]:
                if tool_call["function"]["name"] == "update_character":
                    arguments = json.loads(tool_call["function"]["arguments"])
                    character_agent.update_character_memory(
                        arguments["character_name"],
                        arguments["details"]
                    )
        
        # Process player input with narrative agent
        narrative_response = narrative_agent.process_message_with_tools(
            player_input,
            tools=narrative_tools
        )
        
        # Handle any narrative tool calls from player input
        if "tool_calls" in narrative_response:
            for tool_call in narrative_response["tool_calls"]:
                if tool_call["function"]["name"] == "create_narrative_summary":
                    arguments = json.loads(tool_call["function"]["arguments"])
                    summary = arguments["content"]
                    tags = arguments.get("tags", [])
                    
                    # Save the summary with tags if provided
                    if tags:
                        narrative_agent.tag_summary(summary, tags)
                    else:
                        save_narrative_summary(summary)
```

### 4. Agent Implementation Details

#### BaseAgent (Existing)
- No changes needed to the base agent class

#### InventoryAgent
- Methods:
  - `process_message_with_tools(message, tools)`: Analyze message using LLM tools to detect inventory changes
  - `handle_inventory_update(action, item, quantity)`: Process inventory updates from GameMaster
  - `get_inventory_summary()`: Generate summary of current inventory
  - `add_item(item_name, quantity)`: Add item to inventory
  - `remove_item(item_name, quantity)`: Remove item from inventory
  - `use_item(item_name)`: Mark item as used

#### NarrativeAgent
- Methods:
  - `process_message_with_tools(message, tools)`: Analyze message using LLM tools to identify key narrative elements
  - `create_summary(messages)`: Generate summary from recent messages
  - `get_recent_summaries(count)`: Retrieve recent narrative summaries
  - `combine_summaries(summaries)`: Combine multiple summaries
  - `tag_summary(summary, tags)`: Add searchable tags to narrative summaries

#### CharacterAgent
- Methods:
  - `process_message_with_tools(message, tools)`: Analyze message using LLM tools to detect character information
  - `get_relevant_characters(messages)`: Identify characters relevant to current context
  - `update_character_memory(character_name, details)`: Update character information
  - `get_character_details(character_name)`: Retrieve details about a specific character

## Testing Strategy
- [ ] Test each agent individually with sample inputs
- [ ] Test agent communication with mock messages
- [ ] Test full integration with increasingly complex scenarios
- [ ] Verify memory retention across long conversations
- [ ] Test persistence across game sessions

## Success Criteria
- Game Master can accurately recall characters from earlier in the story
- Inventory remains consistent throughout gameplay
- Story continuity is maintained even after many interactions
- Character personalities and details remain consistent

## Future Enhancements
- Creating a 'tags' system so relevant narrative summaries can be queried
- Implementing a message search functionality for players to recall past interactions
- Adding sentiment analysis to messages to track emotional tone of the story
