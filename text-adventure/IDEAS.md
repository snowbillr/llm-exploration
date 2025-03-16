TUI for the user interacting with the game

- update the game master system prompt to try and keep the player on track and not introduce brand new elements from the world to fit the player's story.

- don't end the game master prompt with any questions to the user

- does updating the narrative context need more than the game master message and the player message?

- narrative entries thoughts
  - are key developments are too granular?
  - no need for a summary, the key developments are enough
  - update model such that each entry is a note on the current player's story rather than containing multiple notes

- local model sucks at taking notes compared to chatgpt 4o
  - we're in prompt engineering territory now
  - need a way to compare the performance of different prompts to the same messages

- generate a quest line prior to starting the story
  - characters
  - items
  - locations
  - track progress in a new table thats used in the enhanced context
