from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT

class InventoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='inventory_agent', system_prompt=SYSTEM_PROMPT)
    
    def get_inventory_summary(self):
        """
        Generate a summary of the current inventory.
        
        Returns:
            str: A formatted summary of the player's current inventory
        """
        # This would typically query the database for current inventory items
        # For now, return a placeholder message
        return "INVENTORY SUMMARY PLACEHOLDER - Will be implemented with database integration"
    
    def add_item(self, item_name, quantity=1):
        """
        Add an item to the player's inventory.
        
        Args:
            item_name (str): The name of the item to add
            quantity (int, optional): The quantity to add. Defaults to 1.
        """
        # This would typically update the database
        print(f"[InventoryAgent] Adding {quantity} {item_name} to inventory")
    
    def remove_item(self, item_name, quantity=1):
        """
        Remove an item from the player's inventory.
        
        Args:
            item_name (str): The name of the item to remove
            quantity (int, optional): The quantity to remove. Defaults to 1.
        """
        # This would typically update the database
        print(f"[InventoryAgent] Removing {quantity} {item_name} from inventory")
    
    def use_item(self, item_name):
        """
        Mark an item as used in the player's inventory.
        
        Args:
            item_name (str): The name of the item to use
        """
        # This would typically update the database
        print(f"[InventoryAgent] Using {item_name} from inventory")

    def process_message_with_tools(self, message):
        """
        Process a message using LLM tools to detect inventory changes.
        
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
                    "name": "get_inventory_summary",
                    "description": "Generate a summary of the current inventory",
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
                    "name": "add_item",
                    "description": "Add an item to the player's inventory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_name": {
                                "type": "string",
                                "description": "The name of the item to add"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "The quantity to add"
                            }
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
                            "item_name": {
                                "type": "string",
                                "description": "The name of the item to remove"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "The quantity to remove"
                            }
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
                            "item_name": {
                                "type": "string",
                                "description": "The name of the item to use"
                            }
                        },
                        "required": ["item_name"]
                    }
                }
            }
        ]
        
        messages = [{"role": "user", "content": message}]
        return self.chat(messages=messages, tools=tools)
