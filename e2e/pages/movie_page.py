# ============================================
# CHEATSHEET - MoviePage (Page Object)
# ============================================
# Responsabilidad: ficha de una película puntual.
# - Definir locators para director y calificación.
# - Exponer métodos que devuelvan los VALORES (string/float), sin assert acá.
# - La comparación (director == "Chris Wedge", rating > 7.0) se hace en el step.
# ============================================

from pages.base_page import BasePage


class MoviePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.director = page.locator("//p[text()='Director']/../p/a")
        self.puntaje = page.locator("//div[contains(@class, 'user_score_chart')]")

    def obtener_director(self) -> str:
        return self.director.text_content().strip()

    def obtener_puntaje(self) -> float:
        return float(self.puntaje.get_attribute("data-percent"))
