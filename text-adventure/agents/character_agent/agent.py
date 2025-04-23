from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT
from db.models import Character
from pydantic import BaseModel, TypeAdapter
from typing_extensions import TypedDict
from agents.llm_logger import log_llm_call

class LLMCharacter(TypedDict):
    name: str
    description: str

class CharacterResponse(BaseModel):
    characters: list[LLMCharacter]

class CharacterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='character_agent', system_prompt=SYSTEM_PROMPT)
    
    def get_character_context(self, game_id):
        query = Character.select().where(Character.game == game_id).limit(20)
        return [character.description for character in query]      
    
    def update_character_context(self, game_master_message, player_message, game_id):
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
            format=CharacterResponse.model_json_schema()
        )
        character_response = TypeAdapter(CharacterResponse).validate_json(llm_response.message.content)

        log_llm_call("CharacterAgent", llm_input, llm_response.message.content)

        for character in character_response.characters:
            # Try to find an existing character in this game with the same name
            existing = Character.select().where(
                (Character.game == game_id) & (Character.name == character['name'])
            ).first()
            if existing:
                # Update the description if character already exists
                existing.description = character['description']
                existing.save()
            else:
                # Create new character if not found
                Character.create(
                    name=character['name'],
                    description=character['description'],
                    game=game_id
                )
