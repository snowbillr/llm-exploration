from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input
import asyncio

from game_loop import GameLoop

class TextAdventureApp(App):
    CSS_PATH = None

    def __init__(self):
        super().__init__()
        self.game_loop = GameLoop()
        self.player = None
        self.initialized = False

    def compose(self) -> ComposeResult:
        yield RichLog(id="messages", highlight=True)
        yield Input(placeholder="What do you do?", id="input")

    async def on_mount(self) -> None:
        # Setup game and prompt for player name
        messages = self.query_one("#messages", RichLog)
        messages.write("[b]Game Master:[/b] Welcome to the Fantasy Text Adventure!", scroll_end=True)
        messages.write("[b]Game Master:[/b] What is your name?", scroll_end=True)
        self.initialized = False
        # Autofocus the input box
        input_box = self.query_one("#input", Input)
        input_box.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        messages = self.query_one("#messages", RichLog)
        user_message = event.value.strip()
        input_box = self.query_one("#input", Input)

        if not user_message:
            return

        input_box.value = ""
        messages.write(f"[b][cyan]You:[/cyan][/b] {user_message}", scroll_end=True)

        if not self.initialized:
            # First input is player name
            self.player = self.game_loop.create_player(user_message)
            messages.write(f"[b]Game Master:[/b] Welcome, {user_message}! Your adventure begins now.", scroll_end=True)
            self.initialized = True
            return

        if user_message.lower() in ["quit", "exit"]:
            messages.write("[b]Game Master:[/b] Thank you for playing! Goodbye.", scroll_end=True)
            await asyncio.sleep(1)
            self.exit()
            return

        input_box.disabled = True
        response = await asyncio.to_thread(self.game_loop.process_turn, user_message, self.player)
        input_box.disabled = False

        messages.write(f"[b][magenta]Game Master:[/magenta][/b] {response}", scroll_end=True)
        input_box.focus()

if __name__ == "__main__":
    TextAdventureApp().run()
