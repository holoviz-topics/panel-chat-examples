from langchain.docstore.base import Document

streamlit_to_panel_documents = [
    Document(
            page_content="""HoloViz provides a set of Python packages that make viz easier,
    more accurate, and more powerful""", metadata={"Header 1": "HoloViz"}
    ),
    Document(
        page_content="""
Panel is an open-source Python library that lets you easily build powerful tools,
dashboards and complex applications entirely in Python. It has a batteries-included
philosophy, putting the PyData ecosystem, powerful data tables and much more at your
fingertips.""", metadata={"Header 1": "Panel"}
    )
]