import json
import time
from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT
from db.models import NarrativeSummary, Player

class NarrativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='narrative_agent', system_prompt=SYSTEM_PROMPT)
    
    def create_summary(self, messages, player_id=None):
        """
        Generate a summary from recent messages and save it to the database.
        
        Args:
            messages (list): List of recent message dictionaries
            player_id (int, optional): ID of the player this summary relates to
            
        Returns:
            str: A narrative summary of recent events
        """
        # This would typically analyze messages and create a summary
        # For demonstration, we'll create a simple summary
        summary = "Adventure continues with new challenges and opportunities."
        key_developments = json.dumps(["Player found a new item", "Discovered a hidden passage"])
        active_goals = json.dumps(["Find the lost artifact", "Return to the village"])
        
        # Save to database
        narrative_summary = NarrativeSummary.create(
            summary=summary,
            key_developments=key_developments,
            active_goals=active_goals,
            timestamp=int(time.time()),
            player=Player.get_by_id(player_id) if player_id else None
        )
        
        return summary
    
    def get_recent_summaries(self, count=3, player_id=None):
        """
        Retrieve recent narrative summaries from the database.
        
        Args:
            count (int, optional): Number of summaries to retrieve. Defaults to 3.
            player_id (int, optional): ID of the player to get summaries for
            
        Returns:
            list: List of recent summary objects
        """
        query = NarrativeSummary.select().order_by(NarrativeSummary.timestamp.desc()).limit(count)
        
        if player_id:
            query = query.where(NarrativeSummary.player == player_id)
            
        summaries = list(query)
        
        # Format the summaries for display
        formatted_summaries = []
        for summary in summaries:
            formatted_summary = f"""
NARRATIVE SUMMARY:
{summary.summary}

KEY DEVELOPMENTS:
{', '.join(json.loads(summary.key_developments))}

ACTIVE GOALS:
{', '.join(json.loads(summary.active_goals))}
"""
            formatted_summaries.append(formatted_summary)
            
        return formatted_summaries
    
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
