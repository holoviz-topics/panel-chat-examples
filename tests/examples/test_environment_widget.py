"""Tests the EnvironmentWidgetBase"""
import os

import param
import pytest

from panel_chat_examples import EnvironmentWidgetBase
from panel_chat_examples._environment_widget import VariableNotFound

os.environ["SOME_VALUE"] = "SOME_VALUE"


class EnvironmentWidget(EnvironmentWidgetBase):
    """An example Environment Widget for testing"""

    SOME_VALUE = param.String(doc="A key for the OpenAI api")
    ANOTHER_VALUE = param.String(doc="A key for the Weaviate api")


def test_construct_from_os_environ():
    """Test that it takes environment variable in constructor"""
    environ = EnvironmentWidget()
    assert environ.SOME_VALUE == "SOME_VALUE"
    assert not environ.ANOTHER_VALUE
    assert environ.variables_set == ["SOME_VALUE"]
    assert environ.variables_not_set == ["ANOTHER_VALUE"]


def test_construct_from_custom_values():
    """Test that custom values takes precedence over environment variables"""
    environ = EnvironmentWidget(SOME_VALUE="NEW_VALUE", ANOTHER_VALUE="ANOTHER_VALUE")
    assert environ.SOME_VALUE == "NEW_VALUE"
    assert environ.ANOTHER_VALUE == "ANOTHER_VALUE"
    assert environ.variables_set == [
        "ANOTHER_VALUE",
        "SOME_VALUE",
    ]  # Sorted alphabetically!
    assert environ.variables_not_set == []


def test_get():
    """Test the we can .get like os.environ"""
    environ = EnvironmentWidget()
    assert environ.get("SOME_VALUE", "A") == environ.SOME_VALUE
    assert environ.get("ANOTHER_VALUE", "B") == "B"


def test_indexing():
    """Test the we can [] like os.environ"""
    environ = EnvironmentWidget()
    assert environ["SOME_VALUE"] == environ.SOME_VALUE
    with pytest.raises(VariableNotFound):
        environ["ANOTHER_VALUE"]  # pylint: disable=pointless-statement
