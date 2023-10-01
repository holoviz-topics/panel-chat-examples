"""Test all app .py files py running them with python"""


def test_app(app_path):
    """Test an app. Can you run it with 'python path_to_file.py'?"""
    with open(app_path, "r", encoding="utf8") as file:
        code = file.read()
    exec(code)  # pylint: disable=exec-used
