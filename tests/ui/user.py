from playwright.sync_api import Page


class ChatInterface():
    def __init__(self, page: Page):
        self.page =page

    def send(self, value):
        text_input = self.page.get_by_placeholder("Send a message")
        text_input.fill(value)
        text_input.press("Enter")

def echo(page: Page):
    chat = ChatInterface(page)
    chat.send("Hello World")

ACTION = {
    "echo.py": echo
}
ZOOM = {
    "echo.py": 2
}