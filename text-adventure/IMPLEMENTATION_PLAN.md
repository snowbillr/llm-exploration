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
1. Create directory structure for new agents
2. Implement base classes and system prompts for each agent
3. Enhance GameMasterAgent to coordinate with specialized agents

### Phase 2: Database Enhancements
1. Add NarrativeSummary model for storing story summaries
2. Add CharacterMemory model for detailed NPC tracking
3. Update database migration scripts

### Phase 3: Agent Communication System
1. Implement message routing between agents
2. Create context enhancement system for GameMasterAgent
3. Develop periodic summarization logic for NarrativeAgent

### Phase 4: Integration and Testing
1. Update main game loop to incorporate all agents
2. Implement context window management
3. Test with complex scenarios to verify memory improvements

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
            
            # Get response from game master
            response = game_master.chat(context_enhanced_messages)
            gm_response = response["message"]["content"]
            print(f"\nGame Master: {gm_response}")
            
            # Process response with specialized agents
            inventory_agent.process_message(gm_response)
            character_agent.process_message(gm_response)
            
            # Add GM response to history
            messages.append({"role": "assistant", "content": gm_response})
            
            # Periodically create narrative summaries
            message_count += 1
            if message_count % 10 == 0:  # Every 10 messages
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
        
        # Add player message to history
        messages.append({"role": "user", "content": player_input})
        
        # Process player input with specialized agents
        inventory_agent.process_message(player_input)
        character_agent.process_message(player_input)
```

### 4. Agent Implementation Details

#### BaseAgent (Existing)
- No changes needed to the base agent class

#### InventoryAgent
- Methods:
  - `process_message(message)`: Analyze message for inventory changes
  - `get_inventory_summary()`: Generate summary of current inventory
  - `add_item(item_name, quantity)`: Add item to inventory
  - `remove_item(item_name, quantity)`: Remove item from inventory
  - `use_item(item_name)`: Mark item as used

#### NarrativeAgent
- Methods:
  - `create_summary(messages)`: Generate summary from recent messages
  - `get_recent_summaries(count)`: Retrieve recent narrative summaries
  - `combine_summaries(summaries)`: Combine multiple summaries

#### CharacterAgent
- Methods:
  - `process_message(message)`: Analyze message for character information
  - `get_relevant_characters(messages)`: Identify characters relevant to current context
  - `update_character_memory(character_name, details)`: Update character information
  - `get_character_details(character_name)`: Retrieve details about a specific character

## Testing Strategy
1. Test each agent individually with sample inputs
2. Test agent communication with mock messages
3. Test full integration with increasingly complex scenarios
4. Verify memory retention across long conversations
5. Test persistence across game sessions

## Success Criteria
- Game Master can accurately recall characters from earlier in the story
- Inventory remains consistent throughout gameplay
- Story continuity is maintained even after many interactions
- Character personalities and details remain consistent

## Future Enhancements
- Storing all messages for a story in the database
- Creating a 'tags' system so relevant narrative summaries can be queried
