"""Locust load test file"""

from pathlib import Path
from random import choice

from conftest import APP_PATHS  # pylint: disable=import-error
from locust import HttpUser, task


class RandomPageUser(HttpUser):
    """This User gets a random page"""

    @task(weight=len(APP_PATHS))
    def get_random_page(self):
        """Gets a random page"""
        app_path = choice(APP_PATHS)
        self.client.get(f"/{Path(app_path).name.replace('.py', '')}")

    @task
    def get_index_page(self):
        """Gets the index page"""
        self.client.get("/")
