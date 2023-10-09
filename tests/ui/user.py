from playwright.sync_api import Page

TIMEOUT = 350

class ChatInterface():
    def __init__(self, page: Page):
        self.page =page

    def send(self, value):
        text_input = self.page.get_by_placeholder("Send a message")
        self.page.wait_for_timeout(TIMEOUT)
        text_input.fill(value)
        self.page.wait_for_timeout(TIMEOUT)
        text_input.press("Enter")

def echo(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()

def echo_stream(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text("Echoing User: Hello World").inner_text()

def chained_response(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")
    page.get_by_text('Yeah! They said "Hello World".').inner_text()

def delayed_placeholder(page: Page):
    chat = ChatInterface(page)
    chat.send("4")
    page.get_by_text('Slept 4 seconds!').inner_text()

def environment_widget(page: Page):
    langchain=page.get_by_role("textbox")
    langchain.first.click()
    langchain.fill("some-secret")
    langchain.press("Enter")
    langchain.press("Tab")
    weviate=page.get_by_role("textbox").nth(1)
    weviate.fill("another-secret")
    weviate.press("Enter")

ACTION = {
    "echo.py": echo,
    "echo_stream.py": echo_stream,
    "environment_widget.py": environment_widget,
    "chained_response.py": chained_response,
    "delayed_placeholder.py": delayed_placeholder,
}
ZOOM = {
    "echo.py": 2,
    "echo_stream.py": 2,
    "environment_widget.py": 1.25,
    "chained_response.py": 2,
    "delayed_placeholder.py": 2,
}