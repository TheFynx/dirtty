from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, DirectoryTree, Input, RichLog
from textual.reactive import reactive
from pathlib import Path
from llama_index.core.query_engine import BaseQueryEngine
from dirtty.themes import get_theme
import logging

logger = logging.getLogger(__name__)

class DirttyApp(App):
    CSS = """
    Screen {
        background: $background;
        color: $text;
    }

    #sidebar {
        width: 25%;
        height: 100%;
        background: $surface;
    }

    #chat-area {
        width: 75%;
        height: 100%;
    }

    #chat-messages {
        height: 85%;
        width: 100%;
        overflow-y: auto;
    }

    #chat-input {
        height: 15%;
        width: 100%;
        dock: bottom;
        background: $surface;
        color: $text;
    }
    """

    selected_directory = reactive(Path)

    def __init__(self, directory: Path, query_engine: BaseQueryEngine, theme: str = "default"):
        super().__init__()
        self.selected_directory = directory
        self.query_engine = query_engine
        self.theme_name = theme

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Container(DirectoryTree(str(self.selected_directory)), id="sidebar")
            with Container(id="chat-area"):
                yield RichLog(id="chat-messages", wrap=True)
                yield Input(placeholder="Type your message here...", id="chat-input")
        yield Footer()

    def on_mount(self) -> None:
        self.apply_theme()
        self.title = f"Dirtty - Chatting about {self.selected_directory.name}"
        self.query_one("#chat-input").focus()

    def apply_theme(self):
        theme_data = get_theme(self.theme_name)
        logger.debug(f"Applying theme: {theme_data}")
        colors = theme_data.get("colors", {})
        for color_name, color_value in colors.items():
            setattr(self.styles, color_name, color_value)
        self.dark = theme_data.get("dark", False)
        logger.info(f"Applied theme: {self.theme_name}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_widget = event.input
        message = input_widget.value
        self.query_one("#chat-messages", RichLog).write(f"You: {message}")

        try:
            response = self.query_engine.chat(message)
            self.query_one("#chat-messages", RichLog).write(f"Assistant: {str(response)}")
        except Exception as error:
            self.query_one("#chat-messages", RichLog).write(f"Error: {str(error)}", style="bold red")

        input_widget.value = ""
        self.query_one("#chat-messages").scroll_end(animate=False)