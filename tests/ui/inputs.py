import time
from pathlib import Path

from playwright.sync_api import Page

# Please note Playwright .click() does not work with Panel buttons
# Luckily .dispatch_event("click") does

TIMEOUT = 350

EXAMPLE_PDF = str((Path.cwd() / "tests/ui/example.pdf").absolute())
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
        time.sleep(1)
        self.button_click(" Send")


def default_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel in a sentence")
    page.wait_for_timeout(TIMEOUT * 10)


def custom_input_widgets(page: Page):
    chat = ChatInterface(page)
    chat.send("How many\nlines\nhere?")
    page.get_by_text("This snippet has 3 lines.").inner_text()
    page.wait_for_timeout(TIMEOUT * 3)


def control_callback_response(page: Page):
    chat = ChatInterface(page)
    chat.button_click(name="Tails!")
    chat.send_click()
    page.wait_for_timeout(TIMEOUT * 5)
    chat.button_click(name="Heads!")
    chat.send_click()
    page.wait_for_timeout(TIMEOUT * 5)


def chained_response(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Yup").inner_text()
    page.wait_for_timeout(TIMEOUT * 3)


def delayed_placeholder(page: Page):
    chat = ChatInterface(page)
    chat.send("4")
    page.get_by_text("Slept 4 seconds!").inner_text()
    page.wait_for_timeout(TIMEOUT * 3)


def llama_cpp_python(page: Page):
    chat = ChatInterface(page)
    chat.send("What is HoloViz Panel in a sentence?")
    page.wait_for_timeout(TIMEOUT * 10)


def langchain_chat_with_pandas(page: Page):
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


def langchain_chat_with_pdf(page: Page):
    chat = ChatInterface(page)
    page.locator('input[type="file"]').set_input_files(EXAMPLE_PDF)
    page.wait_for_timeout(1000)
    chat.send_click()
    page.get_by_text("Let's chat about the PDF!").wait_for()
    page.wait_for_timeout(1000)
    page.get_by_placeholder("Ask questions here!").fill("What assets does the PSF own?")
    page.get_by_placeholder("Ask questions here!").press("Enter")
    page.wait_for_timeout(10000)


def openai_two_bots(page: Page):
    chat = ChatInterface(page)
    chat.send("HoloViz Panel")
    page.wait_for_timeout(15000)


def openai_chat_with_hvplot(page: Page):
    chat = ChatInterface(page)
    chat.send("Plot the population, overlay by country")
    page.wait_for_timeout(4000)
    chat.send("Create a scatter of population vs life expectancy, overlay by country'")
    page.wait_for_timeout(4000)


def openai_images_dall_e(page: Page):
    chat = ChatInterface(page)
    chat.send("Create a complex HoloViz dashboard")
    page.wait_for_timeout(12000)


def pydanticai_find_city_agent(page: Page):
    chat = ChatInterface(page)
    chat.send("Where is the AI capital of Europe?")
    page.wait_for_timeout(12000)


# get all the local functions here
# and put them in a dict
# so we can call them by name like {"openai_two_bots.py": openai_two_bots}
ACTION = {f"{func.__name__}.py": func for func in locals().values() if callable(func)}
ACTION["default_chat"] = default_chat
ZOOM = {}
