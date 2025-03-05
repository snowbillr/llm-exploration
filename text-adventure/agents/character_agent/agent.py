from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT

class CharacterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='character_agent', system_prompt=SYSTEM_PROMPT)
    
    def get_relevant_characters(self, messages):
        """
        Identify characters relevant to the current context.
        
        Args:
            messages (list): List of recent message dictionaries
            
        Returns:
            str: Information about relevant characters
        """
        # This would typically analyze messages and identify relevant characters
        # For now, return a placeholder message
        return "RELEVANT CHARACTERS PLACEHOLDER - Will be implemented with message analysis"
    
    def update_character_memory(self, character_name, details):
        """
        Update character information in the database.
        
        Args:
            character_name (str): The name of the character
            details (str): New information about the character
        """
        # This would typically update the character information in the database
        print(f"[CharacterAgent] Updating character: {character_name} with details: {details}")
    
    def get_character_details(self, character_name):
        """
        Retrieve details about a specific character.
        
        Args:
            character_name (str): The name of the character to retrieve
            
        Returns:
            str: Detailed information about the character
        """
        # This would typically query the database for character details
        # For now, return a placeholder message
        return f"CHARACTER DETAILS PLACEHOLDER for {character_name} - Will be implemented with database integration"
    
    def process_message_with_tools(self, message):
        """
        Process a message using LLM tools to detect character information.
        
        Args:
            message (str): The message to analyze
            tools (list, optional): List of tool definitions for the LLM
            
        Returns:
            dict: The response from the LLM, potentially including tool calls
        """

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_relevant_characters",
                    "description": "Identify characters relevant to the current context",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_character_details",
                    "description": "Retrieve details about a specific character",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "character_name": {
                                "type": "string",
                                "description": "The name of the character to retrieve"
                            }
                        },
                        "required": ["character_name"]
                    }
                }
            }
        ]
        
        messages = [{"role": "user", "content": message}]
        return self.chat(messages=messages, tools=tools)
