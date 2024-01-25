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


def basic_custom_widgets(page: Page):
    chat = ChatInterface(page)
    chat.send("How many\nlines\nhere?")
    page.get_by_text("This snippet has 1 lines.").inner_text()


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


def langchain_lcel(page: Page):
    chat = ChatInterface(page)
    chat.send("Python")
    page.wait_for_timeout(5000)


def langchain_streaming_lcel_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Remember this number: 8. Be concise.")
    page.wait_for_timeout(10000)
    chat.send("What number did I just ask you to remember?")
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


def mistral_api_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel in one sentence")
    page.wait_for_timeout(4000)


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


def openai_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Remember this number 8")
    page.locator("div").filter(has_text=re.compile(r"^ChatGPT$")).first.dispatch_event(
        "click"
    )
    page.wait_for_timeout(1500)
    chat.send("What number did I just ask you to remember?")
    page.wait_for_timeout(1000)


def openai_chat_with_hvplot(page: Page):
    chat = ChatInterface(page)
    chat.send("Plot the prices using distinct shades of pink")
    page.wait_for_timeout(4000)
    chat.send("Create an ohlc plot. Give it the title 'OHLC Plot'")
    page.wait_for_timeout(4000)


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


# get all the local functions here
# and put them in a dict
# so we can call them by name like {"openai_two_bots.py": openai_two_bots}
ACTION = {f"{func.__name__}.py": func for func in locals().values() if callable(func)}
ZOOM = {}
