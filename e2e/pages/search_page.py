# ============================================
# CHEATSHEET - SearchPage (Page Object)
# ============================================
# Responsabilidad: home + buscador del sitio (IMDb o TMDB).
# - Definir acá los locators del input de búsqueda y de los resultados.
# - `buscar(titulo)` escribe y dispara la búsqueda (Enter o botón).
# - `abrir_primer_resultado()` clickea el resultado y devuelve un MoviePage.
# ============================================

import os
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.movie_page import MoviePage

BASE_URL = os.getenv("BASE_URL", "https://www.themoviedb.org/")


class SearchPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator('//*[@placeholder="Search for a movie, tv show, person......"]')
        self.result_title = page.locator("(//h2/span[text()='Ice Age'])").first

    def visit(self):
        self.goto(BASE_URL)

    def buscar(self, titulo: str):
        # wait to load 

        self.search_input.wait_for()
        self.search_input.fill(titulo)
        
        self.search_input.press("Enter")
        
    def abrir_primer_resultado(self) -> MoviePage:
        self.result_title.click()
        return MoviePage(self.page)