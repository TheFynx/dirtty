import yaml
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)


def load_themes():
    # Look for themes in the project root, not in src
    themes_dir = Path(__file__).parent.parent.parent / "themes"
    logger.debug(f"Loading themes from {themes_dir}")
    logger.debug(f"Current working directory: {os.getcwd()}")

    if not themes_dir.exists():
        logger.error(f"Themes directory not found: {themes_dir}")
        return {"default": create_default_theme()}

    logger.debug(f"Directory contents: {list(themes_dir.glob('*'))}")

    themes = {}
    theme_files = list(themes_dir.glob('*.yaml'))
    logger.debug(f"Found theme files: {theme_files}")
    for theme_file in theme_files:
        logger.debug(f"Attempting to load theme from {theme_file}")
        try:
            with open(theme_file, "r") as f:
                theme_data = yaml.safe_load(f)
                themes[theme_data["name"]] = theme_data
                logger.debug(f"Successfully loaded theme: {
                             theme_data['name']}")
                logger.debug(f"Theme data: {theme_data}")
        except Exception as e:
            logger.error(f"Error loading theme from {theme_file}: {str(e)}")

    if "default" not in themes:
        logger.warning(
            "Default theme not found. Creating a basic default theme.")
        themes["default"] = create_default_theme()
        logger.debug(f"Created default theme: {themes['default']}")

    logger.debug(f"All loaded themes: {list(themes.keys())}")
    return themes


def create_default_theme():
    logger.debug("Creating default theme")
    default_theme = {
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
    logger.debug(f"Default theme created: {default_theme}")
    return default_theme


THEMES = load_themes()


def get_theme(theme_name):
    logger.debug(f"Getting theme: {theme_name}")
    if not THEMES:
        logger.warning("No themes were loaded. Using default theme.")
        return create_default_theme()

    theme = THEMES.get(theme_name)
    if theme is None:
        logger.warning(f"Theme '{theme_name}' not found. Using default theme.")
        theme = THEMES.get("default") or create_default_theme()
    logger.debug(f"Returned theme data: {theme}")
    return theme


def dump_theme_info():
    logger.debug("Dumping all theme-related information")
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Theme directory: {Path(__file__).parent.parent / 'themes'}")
    logger.debug(f"All loaded themes: {list(THEMES.keys())}")
    for theme_name, theme_data in THEMES.items():
        logger.debug(f"Theme '{theme_name}' data: {theme_data}")
