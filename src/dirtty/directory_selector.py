from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Footer, Button, Static
from textual.containers import Vertical, Horizontal

class DirectorySelector(App):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Select a directory:", id="title"),
            DirectoryTree("/", id="directory_tree"),
            Horizontal(
                Button("Select", variant="primary", id="select"),
                Button("Cancel", variant="error", id="cancel"),
                id="buttons"
            ),
            id="main"
        )
        yield Footer()

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self.selected_directory = event.path
        self.query_one("#title").update(f"Selected: {self.selected_directory}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select":
            if hasattr(self, 'selected_directory'):
                self.exit(self.selected_directory)
            else:
                self.query_one("#title").update("Please select a directory first")
        elif event.button.id == "cancel":
            self.exit(None)

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()