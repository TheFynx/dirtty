import argparse
import logging
from dirtty.config import load_config, save_config

logger = logging.getLogger(__name__)

def parse_args():
    logger.info("Parsing command line arguments")
    parser = argparse.ArgumentParser(description="dirtty - LlamaIndex Chatbot")
    parser.add_argument("--directory", type=str, default=None,
                        help="Directory containing documents to index")
    parser.add_argument("--model-name", type=str, default="llama3:latest",
                        help="Name of the Ollama model to use")
    parser.add_argument("--theme", type=str, default="default",
                        help="Name of the theme to use")
    parser.add_argument("-v", "--verbose", action="count",
                        default=0, help="Increase verbosity level")
    args = parser.parse_args()
    logger.debug(f"Parsed arguments: {args}")

    config = load_config()
    logger.debug(f"Loaded config: {config}")

    config['model_name'] = args.model_name or config.get('model_name', 'llama3:latest')
    config['theme'] = args.theme or config.get('theme', 'default')

    if args.verbose == 1:
        config['log_level'] = 'INFO'
    elif args.verbose >= 2:
        config['log_level'] = 'DEBUG'
    else:
        config['log_level'] = config.get('log_level', 'WARNING')

    logger.info(f"Final config: {config}")
    save_config(config)

    config['args'] = args

    return config