output from game master agent is shown to user, but also sent to other agents
- inventory agent: responsible before managing items in your inventory
- narrative agent: responsible for summarizing key points in the story, so that the story can be resumed later
- character agent: responsible for tracking characters in the story

game master agent should use a combination of the N most recent messages and the M most recent narrative summaries

TUI for the user interacting with the game

- active goals shouldn't live in the narrative summary model, they are changing too frequently. they should span multiple narrative summaries
- update the game master system prompt to try and keep the player on track and not introduce brand new elements from the world to fit the player's story.

- instrumentation - logging
