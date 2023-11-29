"""The `Document` pane and the `DocumentsViewer` component makes it easy to explore
LangChain `Document`s in your notebook or data app"""
from __future__ import annotations

from typing import List

import panel as pn
import param
from langchain.docstore.document import Document as _Document


class SingleDocument(pn.viewable.Viewer):
    """The Document pane displays LangChain Documents"""

    object: _Document = param.ClassSelector(
        class_=_Document,
        doc="""
    The LangChain Document to display""",
    )

    def __init__(self, object: _Document | None = None, **params):
        name = params.pop("name", None)
        super().__init__(object=object, name=name)

        self._layout = pn.Column(
            "## Meta Data",
            pn.pane.JSON(object=self._metadata, sizing_mode="stretch_width"),
            "## Page Content",
            pn.pane.Markdown(self._page_content, sizing_mode="stretch_width"),
            **params,
        )

    def __panel__(self):
        return self._layout

    @param.depends("object")
    def _metadata(self) -> dict:
        if self.object:
            return self.object.metadata
        return {}

    @param.depends("object")
    def _page_content(self) -> str:
        if self.object:
            return self.object.page_content
        return ""


class Document(pn.viewable.Viewer):
    """The Document viewer makes it easy to display a single or a list of LangChain
    Documents"""

    object: _Document | List[_Document] | None = param.ClassSelector(
        class_=(_Document, list),
        doc="""
    A single LangChain document or a list of LangChain Documents to display""",
    constant=True # We don't support dynamically changing the object yet
    )

    _index: int = param.Integer(label="Document")

    def __init__(self, **params):
        layout_params = {
            key: value
            for key, value in params.items()
            if key not in ["object", "name"]
        }
        params = {
            key: value for key, value in params.items() if key not in layout_params
        }
        super().__init__(**params)
        print(self.object)
        self._single_document = SingleDocument(name="Document")
        self._update_single_document()

    @property
    def _objects(self)->List[_Document]:
        if not self.object:
            return []
        if isinstance(self.object, _Document):
            return [self.object]
        return self.object

    @param.depends("object")
    def _layout(self):
        self._index = 0
        end = max(len(self._objects)-1, 1)
        self.param._index.bounds=(0, end)
        
        if not self._objects:
            return "No documents provided"
        if len(self._objects)==1:
            return self._single_document
        else:
            slider = pn.widgets.IntSlider.from_param(self.param._index, sizing_mode="stretch_width", max_width=800)
            return pn.Column(slider, self._single_document)


    @param.depends("object", "_index", watch=True)
    def _update_single_document(self):
        if not self.object:
            self._single_document.object=None
        elif isinstance(self.object, _Document):
            self._single_document.object=self.object
        else:
            self._single_document.object=self.object[self._index]

    def __panel__(self):
        return self._layout
