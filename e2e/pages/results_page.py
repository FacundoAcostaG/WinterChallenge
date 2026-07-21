from playwright.sync_api import Page
from pages.movie_page import MoviePage


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.result_title = page.locator("(//h2/span[text()='Ice Age'])").first

    def abrir_primer_resultado(self) -> MoviePage:
        self.result_title.click()
        return MoviePage(self.page)
