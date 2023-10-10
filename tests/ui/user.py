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


def echo(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def echo_stream(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def environment_widget(page: Page):
    langchain = page.get_by_role("textbox").nth(0)
    langchain.fill("some-secret")
    langchain.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)
    weviate = page.get_by_role("textbox").nth(1)
    weviate.fill("another-secret")
    weviate.press("Enter")
    page.wait_for_timeout(4 * TIMEOUT)


def chained_response(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text('Yeah! They said "Hello World".').inner_text()


def delayed_placeholder(page: Page):
    chat = ChatInterface(page)
    chat.send("4")
    page.get_by_text("Slept 4 seconds!").inner_text()


def replace_response(page: Page):
    chat = ChatInterface(page)

    chat.button_click(name="Tails!")
    chat.button_click(name=" Send")
    page.wait_for_timeout(4 * TIMEOUT)
    chat.button_click(name="Heads!")
    chat.button_click(name=" Send")
    page.wait_for_timeout(4 * TIMEOUT)


def slim_interface(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()


def chat_memory(page: Page):
    chat = ChatInterface(page)
    chat.send("Tell me what HoloViz Panel is in one sentence")
    page.wait_for_timeout(4 * TIMEOUT)
    chat.send("Tell me more")
    page.wait_for_timeout(6 * TIMEOUT)


def chrome_pdf_qa(page: Page):
    chat = ChatInterface(page)


ACTION = {
    "echo.py": echo,
    "echo_stream.py": echo_stream,
    "environment_widget.py": environment_widget,
    "chained_response.py": chained_response,
    "delayed_placeholder.py": delayed_placeholder,
    "replace_response.py": replace_response,
    "slim_interface.py": slim_interface,
    "chat_memory.py": chat_memory,
}
ZOOM = {
    "echo.py": 2,
    "echo_stream.py": 2,
    "environment_widget.py": 1.25,
    "chained_response.py": 2,
    "delayed_placeholder.py": 2,
    "replace_response.py": 2,
    "slim_interface.py": 1.25,
    "chat_memory.py": 1.25,
}
