from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input

class TextAdventureApp(App):
    def compose(self) -> ComposeResult:
        yield RichLog(id="messages", highlight=True)
        yield Input(placeholder="What do you do?", id="input")

if __name__ == "__main__":
    TextAdventureApp().run()
