import os
from playwright.sync_api import Page
from pages.results_page import ResultsPage

BASE_URL = os.getenv("BASE_URL", "https://www.themoviedb.org/")


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator('//*[@placeholder="Search for a movie, tv show, person......"]')

    def visit(self):
        self.page.goto(BASE_URL)

    def buscar(self, titulo: str) -> ResultsPage:
        self.search_input.wait_for()
        self.search_input.fill(titulo)
        self.search_input.press("Enter")
        return ResultsPage(self.page)
