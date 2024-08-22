import logging
import sys
from pathlib import Path
from dirtty.cli import parse_args
from dirtty.helpers import setup_logging, clear_screen
from dirtty.app import DirttyApp
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer
import multiprocessing
from dirtty.directory_selector import DirectorySelector

# Disable tqdm globally
from functools import partialmethod
from tqdm import tqdm
tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

logger = logging.getLogger(__name__)


def setup_index(documents, llm):
    logger.info("Setting up index")
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5")
    Settings.llm = llm
    index = VectorStoreIndex.from_documents(documents, show_progress=False)
    logger.info("Index setup complete")
    return index


def load_documents(directory: Path):
    logger.info(f"Loading documents from {directory}")
    documents = SimpleDirectoryReader(
        input_dir=str(directory), recursive=True).load_data()
    logger.info(f"Loaded {len(documents)} documents")
    return documents


def setup_llm(model_name: str):
    logger.info(f"Setting up Ollama LLM with model: {model_name}")
    from ollama import Client
    client = Client()
    try:
        client.show(model_name)
    except Exception as error:
        logger.error(f"Model '{model_name}' not found. Error: {str(error)}")
        raise ValueError(f"Model '{model_name}' not found. Please pull it using 'ollama pull {
                         model_name}' before running the application.")
    return Ollama(model=model_name, request_timeout=360.0)


def create_query_engine(index):
    logger.info("Creating query engine")
    memory = ChatMemoryBuffer.from_defaults(token_limit=300000)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt="You are a chat bot able to have normal interactions and to provide coding support, as well as talk about the contents of a directory. Keep your responses concise and to the point.",
        max_iterations=10,
    )
    logger.info("Query engine created")
    return chat_engine


def main():
    # This is required on macOS to avoid issues with multiprocessing
    multiprocessing.set_start_method('spawn', force=True)

    opts = parse_args()
    setup_logging(opts['log_level'])
    logger.debug(f"Parsed options: {opts}")
    logger.info("Starting dirtty application")

    directory = Path(
        opts['args'].directory) if opts['args'].directory else None
    clear_screen()

    if directory is None:
        # Show directory selection screen
        selector_app = DirectorySelector()
        selected_directory = selector_app.run()
        if selected_directory is None:
            logger.error("No directory selected. Exiting.")
            sys.exit(1)
        directory = Path(selected_directory)

    try:
        documents = load_documents(directory)
        llm = setup_llm(opts['model_name'])
        index = setup_index(documents, llm)
        query_engine = create_query_engine(index)

        logger.info("Starting TUI")
        app = DirttyApp(directory, query_engine, opts['theme'])
        app.run()
    except ValueError as error:
        logger.error(str(error))
        print(f"Error: {str(error)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
