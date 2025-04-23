import logging
from pydantic import BaseModel
from datetime import datetime
from agents.llm_logger import log_llm_call
from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT
from db.models import NarrativeSummary, Player

logger = logging.getLogger(__name__)

class NarrativeSummaryResponse(BaseModel):
    key_developments: list[str]

class NarrativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='narrative_agent', system_prompt=SYSTEM_PROMPT)

    def get_narrative_context(self, game_id):
        """
        Retrieve recent narrative summaries from the database.
        
        Args:
            count (int, optional): Number of summaries to retrieve. Defaults to 3.
            game_id (int, optional): ID of the game to get summaries for
            
        Returns:
            list: List of recent summary objects
        """
        query = NarrativeSummary.select().where(NarrativeSummary.game == game_id).order_by(NarrativeSummary.timestamp.desc()).limit(20)
        
        return [summary.note for summary in query]
    
    def update_narrative_context(self, game_master_message, player_message, game_id):
        """
        Generate a summary from recent messages and save it to the database.
        
        Args:
            messages (list): List of recent message dictionaries
            game_id (int, optional): ID of the game this summary relates to
            
        Returns:
            str: A narrative summary of recent events
        """

        llm_input = f"""
<player message>
{player_message}
</player message>
<game master message>
{game_master_message}
</game master message>
                 """
        llm_response = self.chat(
            messages=[
                {
                    "role": "user",
                    "content": llm_input
                }
            ],
            format=NarrativeSummaryResponse.model_json_schema())
        narrative_summary_response = NarrativeSummaryResponse.model_validate_json(llm_response.message.content)

        # Log the LLM call for the narrative agent
        log_llm_call("NarrativeAgent", llm_input, llm_response.message.content)

        # Create one NarrativeSummary per note
        for note in narrative_summary_response.key_developments:
            NarrativeSummary.create(
                note=note,
                timestamp=int(datetime.now().timestamp()),
                game=game_id
            )

        logger.info(f"""
Narrative agent:
  Key developments: {narrative_summary_response.key_developments}                    
""")
