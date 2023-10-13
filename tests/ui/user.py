from playwright.sync_api import Page

# Please note Playwright .click() does not work with Panel buttons
# Luckily .dispatch_event("click") does

TIMEOUT = 350


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


def basic_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def basic_streaming_chat(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def component_environment_widget(page: Page):
    langchain = page.get_by_role("textbox").nth(0)
    langchain.fill("some-secret")
    langchain.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)
    weviate = page.get_by_role("textbox").nth(1)
    weviate.fill("another-secret")
    weviate.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)


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
    chat.button_click(name=" Send")
    page.wait_for_timeout(4 * TIMEOUT)
    chat.button_click(name="Heads!")
    chat.button_click(name=" Send")
    page.wait_for_timeout(4 * TIMEOUT)


def feature_slim_interface(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def langchain_with_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Tell me what HoloViz Panel is in one sentence")
    page.wait_for_timeout(4 * TIMEOUT)
    chat.send("Tell me more")
    page.wait_for_timeout(6 * TIMEOUT)


def langchain_pdf_assistant(page: Page):
    ChatInterface(page)


ACTION = {
    "basic_chat.py": basic_chat,
    "basic_streaming_chat.py": basic_streaming_chat,
    "component_environment_widget.py": component_environment_widget,
    "feature_chained_response.py": feature_chained_response,
    "feature_delayed_placeholder.py": feature_delayed_placeholder,
    "feature_replace_response.py": feature_replace_response,
    "feature_slim_interface.py": feature_slim_interface,
    "langchain_with_memory.py": langchain_with_memory,
}
ZOOM = {
    "basic_chat.py": 2,
    "basic_streaming_chat.py": 2,
    "component_environment_widget.py": 1.25,
    "feature_chained_response.py": 2,
    "feature_delayed_placeholder.py": 2,
    "feature_replace_response.py": 2,
    "feature_slim_interface.py": 1.25,
    "langchain_with_memory.py": 1.25,
}
