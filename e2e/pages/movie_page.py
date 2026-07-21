class MoviePage:
    def __init__(self, page):
        self.page = page
        self.director = page.locator("//p[text()='Director']/../p/a")
        self.puntaje = page.locator("//div[contains(@class, 'user_score_chart')]")

    def obtener_director(self) -> str:
        return self.director.text_content().strip()

    def obtener_puntaje(self) -> float:
        return float(self.puntaje.get_attribute("data-percent"))
