"""Test all app .py files py running them with python"""
import subprocess


def test_app(app_path):
    subprocess.call(['python', app_path])
