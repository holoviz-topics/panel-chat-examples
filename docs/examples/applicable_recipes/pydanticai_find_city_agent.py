"""An example Agent UI to find a city.

Originally derived from https://ai.pydantic.dev/examples/pydantic-model/.
"""

import os
import urllib.parse
from typing import cast

import panel as pn
import param
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName

HEADER_CSS = """
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: linear-gradient(135deg, #0078d7, #00a1ff);
    color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
"""

SYSTEM_PROMPT = """"Find the city that best matches the question asked by the user and
explain why you chose that city."""


QUESTIONS = {
    "AI Capital of Europe": "Where is the AI capital of Europe?",
    "Gravel Cycling in Denmark": "Where do I find the best gravel cycling in Denmark",
    "Best food in Germany": "Where do I find the best food in Germany?",
}


class LocationModel(BaseModel):
    city: str
    country: str
    explanation: str

    @property
    def view(self, map_type="h", zoom: int = 8) -> str:
        query = f"{self.city}, {self.country}"
        encoded_query = urllib.parse.quote(query, safe="")
        src = f"https://maps.google.com/maps?q={encoded_query}&z={zoom}&t={map_type}&output=embed"
        return f"""
        <h1>{self.city}, {self.country}</h1>
        <p>{self.explanation}</p>
        <iframe width="100%" height="400px" src="{src}"
        frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
        """


model = cast(KnownModelName, os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o"))
agent = Agent(
    model,
    result_type=LocationModel,
    system_prompt=SYSTEM_PROMPT,
)


async def callback(contents):
    result = await agent.run(contents)
    return pn.pane.HTML(result.data.view, sizing_mode="stretch_width")


chat = pn.chat.ChatInterface(callback=callback, sizing_mode="stretch_both")


def send_chat_message(message):
    return lambda e: chat.send(message)


buttons = [
    pn.widgets.Button(
        name=key,
        on_click=send_chat_message(value),
    )
    for key, value in QUESTIONS.items()
]

header = pn.pane.HTML(
    "<h1 class='header'>City Finder<h1>",
    stylesheets=[HEADER_CSS],
    sizing_mode="stretch_width",
    margin=0,
)
footer = pn.pane.Markdown("Made with Panel, pydantic-ai and ❤️", align="center")

pn.Column(
    header,
    pn.Row(*buttons, align="center", margin=(10, 5, 25, 5)),
    chat,
    footer,
    sizing_mode="stretch_both",
).servable()
