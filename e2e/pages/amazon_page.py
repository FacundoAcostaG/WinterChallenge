import re
from urllib.parse import urljoin

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect


class AmazonPage:
    BASE_URL = "https://www.amazon.com"

    SEARCH_INPUT = "#twotabsearchtextbox"
    SEARCH_BUTTON = "#nav-search-submit-button"
    CONTINUE_SHOPPING_BUTTON = "button:has-text('Continue shopping')"
    PRODUCT_TITLE = "#productTitle"
    CART_LINK = "#nav-cart"
    CART_ITEMS = ".sc-list-item-content"
    CART_SUBTOTAL = "#sc-subtotal-amount-activecart, #sc-subtotal-amount-buybox"

    RESULTS = "[data-component-type='s-search-result']"

    ADD_TO_CART_SELECTORS = [
        "#add-to-cart-button",
        "#freshAddToCartButton",
        "input[name='submit.add-to-cart']",
    ]

    ADD_TO_CART_CONFIRMATION_SELECTORS = [
        "#sw-gtc",
        "#attach-added-to-cart-message",
        "#NATC_SMART_WAGON_CONF_MSG_SUCCESS",
        "#sw-atc-details-single-container",
    ]

    OPTIONAL_DECLINE_SELECTORS = [
        "#attachSiNoCoverage",
        "#attachSiNoCoverage-announce",
    ]

    def __init__(self, page: Page):
        self.page = page
        self.selected_product = None

    def open(self):
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
        self._dismiss_continue_shopping_if_present()

    def search_product(self, product_name: str):
        self._dismiss_continue_shopping_if_present()
        self.page.locator(self.SEARCH_INPUT).fill(product_name)
        self.page.locator(self.SEARCH_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")

    def select_first_purchasable_product(self):
        candidates = self._get_candidate_products()
        assert candidates, "No se encontraron productos en los resultados de busqueda."

        for candidate in candidates:
            self.page.goto(self._build_url(candidate["href"]), wait_until="domcontentloaded")

            if self._has_add_to_cart():
                title = self.page.locator(self.PRODUCT_TITLE).inner_text().strip()
                self.selected_product = {"title": title}
                return

        raise AssertionError("No se encontro un producto disponible con Add to Cart.")

    def get_selected_product(self):
        assert self.selected_product is not None, "No hay producto seleccionado."
        return self.selected_product

    def add_selected_product_to_cart(self):
        add_to_cart_button = self._find_visible_add_to_cart_button()
        assert add_to_cart_button is not None, "No se encontro el boton Add to Cart."

        add_to_cart_button.click()
        self._handle_optional_decline_step()
        self._wait_for_add_to_cart_confirmation()

    def open_cart(self):
        self.page.locator(self.CART_LINK).click()
        self.page.wait_for_load_state("domcontentloaded")

    def verify_products_are_in_cart(self, selected_products: list[dict]):
        cart_titles = [item["title"] for item in self._get_cart_items()]

        for product in selected_products:
            assert product["title"] in cart_titles, (
                f'El producto "{product["title"]}" no fue encontrado en el carrito.'
            )

    def verify_subtotal_matches_selected_products(self, selected_products: list[dict]):
        cart_items = self._get_cart_items()
        selected_titles = {product["title"] for product in selected_products}
        selected_items = [item for item in cart_items if item["title"] in selected_titles]

        assert len(selected_items) == len(selected_products), (
            "La cantidad de productos seleccionados no coincide con lo esperado."
        )

        expected_subtotal = round(sum(item["price"] for item in selected_items), 2)
        actual_subtotal = self._get_subtotal()

        assert actual_subtotal == expected_subtotal, (
            f"Subtotal esperado: {expected_subtotal}. Subtotal obtenido: {actual_subtotal}."
        )

    def _dismiss_continue_shopping_if_present(self):
        button = self.page.locator(self.CONTINUE_SHOPPING_BUTTON)
        if button.count() == 1 and button.is_visible():
            button.click()
            self.page.wait_for_load_state("domcontentloaded")

    def _get_candidate_products(self, limit: int = 8):
        return self.page.evaluate(
            """(limit) => {
                const cards = Array.from(document.querySelectorAll("[data-component-type='s-search-result']"));

                return cards
                    .map((card) => {
                        const titleLink = card.querySelector("h2 a");
                        if (!titleLink) return null;

                        return {
                            title: (titleLink.textContent || "").trim(),
                            href: titleLink.getAttribute("href")
                        };
                    })
                    .filter(Boolean)
                    .slice(0, limit);
            }""",
            limit,
        )

    def _has_add_to_cart(self):
        return self._find_visible_add_to_cart_button() is not None

    def _find_visible_add_to_cart_button(self):
        for selector in self.ADD_TO_CART_SELECTORS:
            locator = self.page.locator(selector)
            if locator.count() == 1 and locator.is_visible():
                return locator

        return None

    def _handle_optional_decline_step(self):
        for selector in self.OPTIONAL_DECLINE_SELECTORS:
            locator = self.page.locator(selector)
            if locator.count() == 1 and locator.is_visible():
                locator.click()
                return

    def _wait_for_add_to_cart_confirmation(self):
        for selector in self.ADD_TO_CART_CONFIRMATION_SELECTORS:
            try:
                expect(self.page.locator(selector)).to_be_visible(timeout=4000)
                return
            except PlaywrightTimeoutError:
                continue

        raise AssertionError("No aparecio confirmacion luego de agregar el producto al carrito.")

    def _get_cart_items(self):
        items = self.page.evaluate(
            """() => {
                const containers = Array.from(document.querySelectorAll(".sc-list-item-content"));

                return containers.map((container) => {
                    const title =
                        container.querySelector(".sc-product-title")?.textContent?.trim() ||
                        container.querySelector(".a-truncate-cut")?.textContent?.trim() ||
                        container.querySelector("img")?.getAttribute("alt")?.trim() ||
                        "";

                    const price =
                        container.querySelector(".sc-product-price")?.textContent?.trim() ||
                        container.querySelector(".a-color-price")?.textContent?.trim() ||
                        container.querySelector(".a-offscreen")?.textContent?.trim() ||
                        "";

                    return { title, price };
                }).filter((item) => item.title && item.price);
            }"""
        )

        return [
            {"title": item["title"], "price": self._parse_price(item["price"])}
            for item in items
        ]

    def _get_subtotal(self):
        subtotal_text = self.page.locator(self.CART_SUBTOTAL).first.inner_text()
        return self._parse_price(subtotal_text)

    def _build_url(self, path: str):
        return urljoin(self.BASE_URL, path)

    @staticmethod
    def _parse_price(raw_price: str):
        match = re.search(r"(\d[\d,]*\.\d{2})", raw_price.replace("\n", " "))
        assert match, f"No se pudo interpretar el precio: {raw_price}"
        return float(match.group(1).replace(",", ""))

