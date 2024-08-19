import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import Ollama
import pytermgui as ptg

# LlamaIndex setup
llm = Ollama(model="llama2")
service_context = ServiceContext.from_defaults(llm=llm)
documents = SimpleDirectoryReader('path/to/your/directory').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()

# TUI setup
with ptg.WindowManager() as manager:
    manager.layout.add_slot("Header")
    manager.layout.add_slot("Body")
    manager.layout.add_slot("Footer")

    header = ptg.Window(
        "[bold]LlamaIndex Chatbot[/bold]",
        box="DOUBLE",
    )

    chat_box = ptg.Window(
        "",
        box="ROUNDED",
        height=20,
    )

    input_field = ptg.InputField()
    send_button = ptg.Button("Send", lambda *_: send_message())
    exit_button = ptg.Button("Exit", lambda *_: manager.stop())

    footer = ptg.Window(
        ptg.Splitter(
            input_field,
            ptg.Container(send_button, exit_button)
        ),
        box="ROUNDED"
    )

    def send_message(*_):
        user_input = input_field.value
        if user_input:
            chat_box.add(f"\nYou: {user_input}")
            response = query_engine.query(user_input)
            chat_box.add(f"\nAssistant: {response}")
            input_field.value = ""

    input_field.bind(ptg.keys.ENTER, send_message)

    manager.add(header, assign="Header")
    manager.add(chat_box, assign="Body")
    manager.add(footer, assign="Footer")

    manager.run()