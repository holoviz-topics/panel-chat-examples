"""
The `Status` *indicator* can report progress in steps and with
detailed context."""
from contextlib import contextmanager

import panel as pn
import param
from panel.widgets.indicators import LoadingSpinner

COLORS = {
    "running": "green",
    "complete": "black",
    "error": "red",
    "next": "lightgray",
}
STATUS_PARAMETERS = ["value", "title", "collapsed", "bgcolor", "color", "steps", "step"]


class Status(pn.viewable.Viewer):
    """The `Status` *indicator* can report progress in steps and with
    detailed context."""

    value = param.Selector(
        default="complete",
        objects=["complete", "running", "error"],
        doc="""
        The current state of the Status indicator. One of 'complete',
        'running' or 'error'""",
    )
    title = param.String(doc="The title shown in the card header")

    bgcolor = param.ObjectSelector(
        default=LoadingSpinner.param.bgcolor.default,
        objects=LoadingSpinner.param.bgcolor.objects,
        doc="""The background color of the LoadingSpinner""",
    )
    color = param.ObjectSelector(
        default="success",
        objects=LoadingSpinner.param.color.objects,
        doc="""The color of the LoadingSpinner""",
    )
    collapsed = param.Boolean(
        default=True, doc="""Whether or not the Card is collapsed"""
    )

    steps = param.List(constant=False, doc="""A list of (markdown) string steps""")
    step = param.Parameter(constant=True, doc="""The current step""")

    def __init__(self, title: str, **params):
        params["title"] = title
        params["steps"] = params.get("steps", [])
        layout_params = {
            key: value for key, value in params.items() if key not in STATUS_PARAMETERS
        }
        params = {
            key: value for key, value in params.items() if key not in layout_params
        }
        super().__init__(**params)

        self._indicators = {
            "running": pn.indicators.LoadingSpinner(
                value=True,
                color=self.param.color,
                bgcolor=self.param.bgcolor,
                size=25,
                # margin=(15, 0, 0, 0),
            ),
            "complete": "✔️",
            "error": "❌",
        }

        self._title_pane = pn.pane.Markdown(self.param.title, align="center")
        self._header_row = pn.Row(
            pn.panel(self._indicator, sizing_mode="fixed", width=40, align="center"),
            self._title_pane,
            sizing_mode="stretch_width",
            margin=(0, 5),
        )
        self._details_pane = pn.pane.HTML(
            self._details, margin=(10, 5, 10, 55), sizing_mode="stretch_width"
        )
        self._layout = pn.Card(
            self._details_pane,
            header=self._header_row,
            collapsed=self.param.collapsed,
            **layout_params,
        )

    def __panel__(self):
        return self._layout

    @param.depends("value")
    def _indicator(self):
        return self._indicators[self.value]

    @property
    def _step_color(self):
        return COLORS[self.value]

    def _step_index(self):
        if self.step not in self.steps:
            return 0
        return self.steps.index(self.step)

    @param.depends("step", "value")
    def _details(self):
        steps = self.steps

        if not steps:
            return ""

        index = self._step_index()

        html = ""
        for step in steps[:index]:
            html += f"<div style='color:{COLORS['complete']}'>{step}</div>"
        step = steps[index]
        html += f"<div style='color:{self._step_color}'>{step}</div>"
        for step in steps[index + 1 :]:
            html += f"<div style='color:{COLORS['next']};'>{step}</div>"

        return html

    def progress(self, step: str):
        with param.edit_constant(self):
            self.value = "running"
            if step not in self.steps:
                self.steps = self.steps + [step]
            self.step = step

    def reset(self):
        with param.edit_constant(self):
            self.steps = []
            self.value = self.param.value.default

    def start(self):
        with param.edit_constant(self):
            self.step = None
        self.value = "running"

    def complete(self):
        self.value = "complete"

    @contextmanager
    def report(self):
        self.start()
        try:
            yield self.progress
        except Exception:
            self.value = "error"
        else:
            self.complete()
