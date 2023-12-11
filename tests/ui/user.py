import os
import re
from pathlib import Path

from playwright.sync_api import Page

# Please note Playwright .click() does not work with Panel buttons
# Luckily .dispatch_event("click") does

TIMEOUT = 350

EXAMPLE_PDF = str((Path.cwd() / "docs/examples/langchain/example.pdf").absolute())
EXAMPLE_CSV = str((Path.cwd() / "tests/ui/example.csv").absolute())
PENGUINS_CSV = str((Path.cwd() / "tests/ui/penguins.csv").absolute())


class ChatInterface:
    def __init__(self, page: Page):
        self.page = page

    def send(self, value):
        text_input = self.page.get_by_placeholder("Send a message")
        self.page.wait_for_timeout(TIMEOUT)
        text_input.fill(value)
        self.page.wait_for_timeout(TIMEOUT)
        text_input.press("Enter")

    def button_click(self, name):
        self.page.get_by_role("button", name=name).dispatch_event("click")
        self.page.wait_for_timeout(TIMEOUT)

    def send_click(self):
        self.button_click(" Send")


def basic_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def basic_streaming_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def basic_streaming_chat_async(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def component_chat_input(page: Page):
    text_input = page.get_by_placeholder("Say something")

    text_input.fill("Hello World")
    page.wait_for_timeout(TIMEOUT)
    text_input.press("Enter")
    page.get_by_text("User has sent the following prompt: Hello World").wait_for()

    text_input.fill("Could you please repeat that?")
    page.wait_for_timeout(TIMEOUT)
    text_input.press("Enter")
    page.get_by_text(
        "User has sent the following prompt: Could you please repeat that?"
    ).wait_for()


def component_environment_widget(page: Page):
    langchain = page.get_by_role("textbox").nth(0)
    langchain.fill("some-secret")
    langchain.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)
    weviate = page.get_by_role("textbox").nth(1)
    weviate.fill("another-secret")
    weviate.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)


def component_status(page: Page):
    page.get_by_role("button", name="Run").dispatch_event("click")
    page.get_by_text("Validating data...").wait_for()
    page.wait_for_timeout(TIMEOUT)


def feature_chained_response(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text('Yeah! They said "Hello World".').inner_text()


def feature_delayed_placeholder(page: Page):
    chat = ChatInterface(page)
    chat.send("4")
    page.get_by_text("Slept 4 seconds!").inner_text()


def feature_replace_response(page: Page):
    chat = ChatInterface(page)

    chat.button_click(name="Tails!")
    chat.send_click()
    page.wait_for_timeout(4 * TIMEOUT)
    chat.button_click(name="Heads!")
    chat.send_click()
    page.wait_for_timeout(4 * TIMEOUT)


def feature_slim_interface(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def langchain_llama_and_mistral(page: Page):
    # Needs some finetuning
    # Could not get this working as it always starts by downloading models
    chat = ChatInterface(page)
    chat.send("Please explain what kind of model you are in one sentence")
    page.wait_for_timeout(15000)


def langchain_chat_pandas_df(page: Page):
    chat = ChatInterface(page)
    page.get_by_role("textbox").set_input_files(PENGUINS_CSV)
    page.wait_for_timeout(333)
    chat.button_click(" Send")
    page.get_by_text("For example 'how many species are there?'").wait_for()
    chat.send("What are the species?")
    page.get_by_text("The species in the dataframe are").wait_for()
    page.wait_for_timeout(100)
    chat.send("What is the average bill length per species?")
    page.get_by_text("The average bill length per species is as follows").wait_for()
    page.wait_for_timeout(2500)


def langchain_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Tell me what HoloViz Panel is in one sentence")
    page.wait_for_timeout(4 * TIMEOUT)
    chat.send("Tell me more")
    page.wait_for_timeout(6 * TIMEOUT)


def langchain_math_assistant(page: Page):
    chat = ChatInterface(page)
    chat.send("What is the square root of 9?")
    page.get_by_text("Answer:").wait_for()
    page.wait_for_timeout(3000)


def langchain_pdf_assistant(page: Page):
    chat = ChatInterface(page)
    page.get_by_role("textbox").set_input_files(EXAMPLE_PDF)
    page.wait_for_timeout(1000)
    chat.send_click()
    page.get_by_text("Let's chat about the PDF!").wait_for()
    page.wait_for_timeout(500)
    # chat.send("What assets does the PSF own?")
    page.get_by_placeholder("Ask questions here!").fill("What assets does the PSF own?")
    page.get_by_placeholder("Ask questions here!").press("Enter")
    page.wait_for_timeout(10000)


def mistral_and_llama(page: Page):
    chat = ChatInterface(page)
    chat.send("What do you think about HoloViz in a single sentence?")
    page.wait_for_timeout(15000)


def mistral_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel in one sentence")
    page.wait_for_timeout(4000)


def mistral_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Tell me what HoloViz Panel is in one sentence")
    page.wait_for_timeout(3000)
    chat.send("Tell me more")
    page.wait_for_timeout(3000)


def openai_async_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel in one sentence")
    page.wait_for_timeout(4000)


def openai_authentication(page: Page):
    chat = ChatInterface(page)
    page.get_by_placeholder("sk-...").fill(os.environ["OPENAI_API_KEY"])
    page.get_by_placeholder("sk-...").press("Enter")
    page.get_by_text(
        "Your OpenAI key has been set. Feel free to minimize the sidebar."
    ).wait_for()
    page.wait_for_timeout(1000)
    chat.send("Explain who you are in one sentence")
    page.wait_for_timeout(3000)


def openai_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel")
    page.locator("div").filter(has_text=re.compile(r"^ChatGPT$")).first.dispatch_event(
        "click"
    )
    page.wait_for_timeout(2000)


def openai_chat_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Remember this number 8")
    page.locator("div").filter(has_text=re.compile(r"^ChatGPT$")).first.dispatch_event(
        "click"
    )
    page.wait_for_timeout(2000)
    chat.send("What number did I just ask you to remember?")

    # ---------------------


def openai_hvplot(page: Page):
    chat = ChatInterface(page)
    page.get_by_role("textbox").set_input_files(EXAMPLE_CSV)
    page.wait_for_timeout(1000)
    chat.button_click(" Send")
    page.get_by_role("combobox").select_option("clothing")
    page.wait_for_timeout(1000)


def openai_image_generation(page: Page):
    chat = ChatInterface(page)
    chat.send("Two people on a beach in the style of Carl Barks")
    page.get_by_text("DALL-E").wait_for()
    page.locator("img").nth(1).wait_for()
    page.wait_for_timeout(1000)


def openai_two_bots(page: Page):
    chat = ChatInterface(page)
    chat.send("HoloViz Panel")
    page.wait_for_timeout(10000)


ACTION = {
    "basic_chat.py": basic_chat,
    "basic_streaming_chat_async.py": basic_streaming_chat_async,
    "basic_streaming_chat.py": basic_streaming_chat,
    "component_chat_input.py": component_chat_input,
    "component_environment_widget.py": component_environment_widget,
    "component_status.py": component_status,
    "feature_chained_response.py": feature_chained_response,
    "feature_delayed_placeholder.py": feature_delayed_placeholder,
    "feature_replace_response.py": feature_replace_response,
    "feature_slim_interface.py": feature_slim_interface,
    "langchain_llama_and_mistral.py": langchain_llama_and_mistral,
    "langchain_math_assistant.py": langchain_math_assistant,
    "langchain_chat_pandas_df.py": langchain_chat_pandas_df,
    "langchain_pdf_assistant.py": langchain_pdf_assistant,
    "langchain_with_memory.py": langchain_with_memory,
    "mistral_and_llama.py": mistral_and_llama,
    "mistral_chat.py": mistral_chat,
    "mistral_with_memory.py": mistral_with_memory,
    "openai_async_chat.py": openai_async_chat,
    "openai_authentication.py": openai_authentication,
    "openai_chat.py": openai_chat,
    "openai_chat_with_memory.py": openai_chat_with_memory,
    "openai_hvplot.py": openai_hvplot,
    "openai_image_generation.py": openai_image_generation,
    "openai_two_bots.py": openai_two_bots,
}
ZOOM = {
    "basic_chat.py": 1.8,
    "basic_streaming_chat_async.py": 1.8,
    "basic_streaming_chat.py": 1.8,
    "component_chat_input.py": 2,
    "component_environment_widget.py": 1.25,
    "component_status.py": 2,
    "feature_chained_response.py": 1.8,
    "feature_delayed_placeholder.py": 1.8,
    "feature_replace_response.py": 1.8,
    "feature_slim_interface.py": 1.25,
    "langchain_chat_pandas_df.py": 1,
    "langchain_llama_and_mistral.py": 1.25,
    "langchain_math_assistant.py": 1.5,
    "langchain_pdf_assistant.py": 1,
    "langchain_with_memory.py": 1.25,
    "mistral_chat.py": 1.8,
    "mistral_with_memory.py": 1,
    "openai_async_chat.py": 1.75,
    "openai_authentication.py": 1,
    "openai_chat.py": 1.5,
    "openai_hvplot.py": 1,
    "openai_image_generation.py": 1.5,
    "openai_two_bots.py": 1,
}
