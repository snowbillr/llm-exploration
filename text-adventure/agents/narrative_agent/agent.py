from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT

class NarrativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='narrative_agent', system_prompt=SYSTEM_PROMPT)
    
    def create_summary(self, messages):
        """
        Generate a summary from recent messages.
        
        Args:
            messages (list): List of recent message dictionaries
            
        Returns:
            str: A narrative summary of recent events
        """
        # This would typically analyze messages and create a summary
        # For now, return a placeholder message
        return "NARRATIVE SUMMARY PLACEHOLDER - Will be implemented with message analysis"
    
    def get_recent_summaries(self, count=3):
        """
        Retrieve recent narrative summaries.
        
        Args:
            count (int, optional): Number of summaries to retrieve. Defaults to 3.
            
        Returns:
            str: Combined recent summaries
        """
        # This would typically query the database for recent summaries
        # For now, return a placeholder message
        return "RECENT SUMMARIES PLACEHOLDER - Will be implemented with database integration"
    
    def combine_summaries(self, summaries):
        """
        Combine multiple summaries into a cohesive narrative.
        
        Args:
            summaries (list): List of summary strings
            
        Returns:
            str: A combined narrative summary
        """
        # This would typically combine and condense multiple summaries
        # For now, return a placeholder message
        return "COMBINED SUMMARY PLACEHOLDER - Will be implemented with summary processing"
    
    def tag_summary(self, summary, tags):
        """
        Add searchable tags to narrative summaries.
        
        Args:
            summary (str): The narrative summary
            tags (list): List of tag strings
        """
        # This would typically save the summary with tags to the database
        tag_str = ", ".join(tags)
        print(f"[NarrativeAgent] Tagging summary with: {tag_str}")
    
    def process_message_with_tools(self, message):
        """
        Process a message using LLM tools to identify key narrative elements.
        
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
                    "name": "create_summary",
                    "description": "Generate a summary from recent messages",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The narrative summary content"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recent_summaries",
                    "description": "Retrieve recent narrative summaries",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "count": {
                                "type": "integer",
                                "description": "Number of summaries to retrieve"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tag_summary",
                    "description": "Add searchable tags to narrative summaries",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "The narrative summary"
                            },
                            "tags": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "Tags to categorize the summary"
                            }
                        },
                        "required": ["summary", "tags"]
                    }
                }
            }
        ]
        
        messages = [{"role": "user", "content": message}]
        return self.chat(messages=messages, tools=tools)
