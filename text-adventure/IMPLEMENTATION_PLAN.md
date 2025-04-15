# IMPLEMENTATION PLAN: Textual Interface for Text Adventure Game

## 1. Choose the Library
- Use the [Textual](https://textual.textualize.io/) library for building the terminal-based UI.

## 2. Define the Layout
- **Vertical Layout:**
  - **Top Panel:** Message history using a `TextLog` widget (scrollable, displays conversation between player and game master).
  - **Bottom Panel:** Input box for user commands/messages.

## 3. Implement the Message Panel
- Use a `TextLog` widget for displaying messages.
- Append new messages as they are sent/received.
- Optionally, color-code messages (e.g., player vs. game master).

## 4. Implement the Input Panel
- Use an `Input` widget at the bottom for user input.
- Capture the Enter key to submit the message.
- On submission:
  - Add the user message to the message panel.
  - Send it to the game logic (game master agent).
  - Display the game master's response in the message panel.

## 5. Wire Up the Logic
- Maintain a message history (list or buffer).
- On user input:
  - Update the message panel.
  - Call the game logic to get a response.
  - Update the message panel with the response.

## 6. Integration
- Refactor your main game loop to run inside the Textual app.
- Ensure the game logic can be called asynchronously or in a non-blocking way to keep the UI responsive.

---

### Example Structure

```python
from textual.app import App, ComposeResult
from textual.widgets import TextLog, Input

class AdventureApp(App):
    def compose(self) -> ComposeResult:
        yield TextLog(id="messages", highlight=True)
        yield Input(placeholder="Type your message...", id="input")

    # Add event handlers for input submission, message display, etc.

if __name__ == "__main__":
    AdventureApp().run()
```
