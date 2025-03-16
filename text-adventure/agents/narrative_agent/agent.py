import logging
import json
import time
from pydantic import BaseModel

from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT
from db.models import NarrativeSummary, Player

logger = logging.getLogger(__name__)

class NarrativeSummaryResponse(BaseModel):
    key_developments: list[str]

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
KEY DEVELOPMENTS:
{', '.join(json.loads(summary.key_developments))}
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

        llm_response = self.chat(
            messages=[
                {"role": "assistant", "content": game_master_message},
                {"role": "user", "content": player_message}
            ],
            format=NarrativeSummaryResponse.model_json_schema())
        narrative_summary_response = NarrativeSummaryResponse.model_validate_json(llm_response.message.content)

        narrative_summary = NarrativeSummary.create(
            key_developments=json.dumps(narrative_summary_response.key_developments),
            timestamp=int(time.time()),
            player=Player.get_by_id(player_id) if player_id else None
        )

        logger.info(f"""
Narrative agent:
  Key developments: {narrative_summary.key_developments}                    
""")
