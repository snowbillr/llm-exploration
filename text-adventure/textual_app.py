from textual.app import App, ComposeResult
from textual.widgets import Footer, RichLog, Input, Label
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
import time
import asyncio

from game_loop import GameLoop
from agents.llm_logger import log_llm_call
from llm_event_bus import LLMEventBus
from llm_event_types import LLMEvent

class TextAdventureApp(App):
    CSS_PATH = None
    BINDINGS = [
        Binding("ctrl+x", "toggle_debug", "Toggle Debug Panel", show=True, priority=True)
    ]

    def __init__(self):
        super().__init__()
        self.game_loop = GameLoop()
        self.player = None
        self.initialized = False
        self.debug_mode = False

    def compose(self) -> ComposeResult:
        main_panel = Vertical(
            RichLog(id="messages", highlight=True, markup=True, wrap=True),
            Input(placeholder="What do you do?", id="input"),
            id="main_panel"
        )
        debug_panel = Vertical(
            Label("Debug Log", id="debug_label"),
            RichLog(id="debug_log", highlight=True, markup=True, wrap=True),
            id="debug_panel"
        )

        yield Vertical(
            Horizontal(main_panel, debug_panel, id="panels_container"),
            Footer(),
            id="root_container"
        )

    def on_mount(self) -> None:
        debug_panel = self.query_one("#debug_panel", Vertical)
        debug_panel.display = self.debug_mode

        messages = self.query_one("#messages", RichLog)
        messages.write("[b]Game Master:[/b] Welcome to the Fantasy Text Adventure!", scroll_end=True)
        messages.write("[b]Game Master:[/b] What is your name?", scroll_end=True)

        input_box = self.query_one("#input", Input)
        input_box.focus()

        # Start background task to update debug panel with LLM events
        self.set_interval(1, self.check_llm_events, pause=False)

    def check_llm_events(self):
        debug_log = self.query_one("#debug_log", RichLog)
        while LLMEventBus.has_events():
            event = LLMEventBus.get_event()
            debug_log.write(
                f"[b][yellow]{event.agent}[/yellow][/b] [i]@ {event.timestamp:.2f}[/i]\n[cyan]Input:[/cyan] {event.input_data}\n[magenta]Output:[/magenta] {event.output_data}",
                scroll_end=True
            )

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

    def action_toggle_debug(self):
        self.debug_mode = not self.debug_mode

        debug_panel = self.query_one("#debug_panel", Vertical)
        debug_panel.display = self.debug_mode

if __name__ == "__main__":
    TextAdventureApp().run()
