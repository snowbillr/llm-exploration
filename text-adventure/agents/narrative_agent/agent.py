import json
import time
from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT
from db.models import NarrativeSummary, Player

class NarrativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='narrative_agent', system_prompt=SYSTEM_PROMPT)

    def get_narrative_context(self, count=3, player_id=None):
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
    
    def update_narrative_context(self, game_master_message, player_message, player_id=None):
        """
        Generate a summary from recent messages and save it to the database.
        
        Args:
            messages (list): List of recent message dictionaries
            player_id (int, optional): ID of the player this summary relates to
            
        Returns:
            str: A narrative summary of recent events
        """

        llm_response = self.chat([{"role": "assistant", "content": game_master_message}, {"role": "user", "content": player_message}])['message']['content']

        # extract the summary, key developments, and active goals from the response
        summary = ""
        key_developments = []
        active_goals = []
        
        # Parse the narrative summary
        if "NARRATIVE SUMMARY:" in llm_response and "KEY DEVELOPMENTS:" in llm_response:
            summary_start = llm_response.find("NARRATIVE SUMMARY:") + len("NARRATIVE SUMMARY:")
            summary_end = llm_response.find("KEY DEVELOPMENTS:")
            summary = llm_response[summary_start:summary_end].strip()
        
        # Parse the key developments
        if "KEY DEVELOPMENTS:" in llm_response and "ACTIVE GOALS:" in llm_response:
            dev_start = llm_response.find("KEY DEVELOPMENTS:") + len("KEY DEVELOPMENTS:")
            dev_end = llm_response.find("ACTIVE GOALS:")
            dev_text = llm_response[dev_start:dev_end].strip()
            
            # Extract bullet points
            for line in dev_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    key_developments.append(line[2:])
        
        # Parse the active goals
        if "ACTIVE GOALS:" in llm_response:
            goals_start = llm_response.find("ACTIVE GOALS:") + len("ACTIVE GOALS:")
            goals_text = llm_response[goals_start:].strip()
            
            # Extract bullet points
            for line in goals_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    active_goals.append(line[2:])
        
        # Save to database
        narrative_summary = NarrativeSummary.create(
            summary=summary,
            key_developments=json.dumps(key_developments),
            active_goals=json.dumps(active_goals),
            timestamp=int(time.time()),
            player=Player.get_by_id(player_id) if player_id else None
        )
        
        return summary
