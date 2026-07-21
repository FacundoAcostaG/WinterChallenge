# ============================================
# CHEATSHEET PLAYWRIGHT (sync API) - básico
# ============================================
# page.goto(url)                          -> navegar a una URL
# page.locator(selector)                  -> obtener un localizador (no falla si no existe aún)
# locator.click() / .fill(texto) / .press("Enter")
# locator.text_content() / .inner_text()  -> leer texto
# locator.is_visible()                    -> chequeo de visibilidad
# page.wait_for_selector(selector)        -> esperar a que aparezca
# page.screenshot(path="...")             -> capturar pantalla
# Selectores recomendados: get_by_role, get_by_text, get_by_placeholder
#   (más estables que CSS/XPath frágiles)
# ============================================
#
# CHEATSHEET POM (Page Object Model)
# ============================================
# - Cada página/pantalla real = una clase con sus locators + acciones.
# - Los métodos devuelven acciones o el próximo Page Object (ej: al navegar).
# - Las aserciones NO van acá: van en los steps (buscar_peli_steps.py).
# - BasePage concentra lo común a todas las páginas (goto, screenshot, etc.)
# ============================================

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        

    def goto(self, url: str):
        self.page.goto(url)



    def take_screenshot(self, path: str):
        self.page.screenshot(path=path)

    