import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_default_theme():
    return {
        "name": "default",
        "dark": False,
        "colors": {
            "primary": "#004578",
            "secondary": "#393939",
            "background": "#FFFFFF",
            "surface": "#EEEEEE",
            "panel": "#F0F0F0",
            "boost": "rgba(0, 0, 0, 0.1)",
            "success": "#2EA043",
            "warning": "#D29922",
            "error": "#DA3633",
            "accent": "#0366D6",
            "text": "#000000"
        }
    }

def load_themes():
    themes_dir = Path(__file__).parent.parent / "themes"
    logger.debug(f"Loading themes from {themes_dir}")
    themes = {}
    theme_files = list(themes_dir.glob('*.yaml'))
    logger.debug(f"Found theme files: {theme_files}")
    for theme_file in theme_files:
        try:
            with open(theme_file, "r") as f:
                theme_data = yaml.safe_load(f)
                themes[theme_data["name"]] = theme_data
                logger.debug(f"Loaded theme: {theme_data['name']}")
        except Exception as e:
            logger.error(f"Error loading theme from {theme_file}: {str(e)}")

    if "default" not in themes:
        logger.warning("Default theme not found. Creating a basic default theme.")
        themes["default"] = create_default_theme()

    logger.debug(f"All loaded themes: {list(themes.keys())}")
    return themes

THEMES = load_themes()

def get_theme(theme_name):
    logger.debug(f"Getting theme: {theme_name}")
    theme = THEMES.get(theme_name)
    if theme is None:
        logger.warning(f"Theme '{theme_name}' not found. Using default theme.")
        theme = THEMES["default"]
    return theme