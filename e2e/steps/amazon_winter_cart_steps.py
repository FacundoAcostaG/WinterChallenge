from behave import given, then, when

from pages.amazon_page import AmazonPage


@given("que el usuario se encuentra en la pagina principal de Amazon")
def step_open_amazon_home(context):
    context.amazon_page = AmazonPage(context.page)
    context.amazon_page.open()


@when('busca el producto "{product_name}"')
def step_search_product(context, product_name):
    context.amazon_page.search_product(product_name)


@when("selecciona un producto disponible de los resultados")
def step_select_available_product(context):
    context.amazon_page.select_first_purchasable_product()


@when("agrega el producto seleccionado al carrito")
def step_add_selected_product_to_cart(context):
    selected_product = context.amazon_page.get_selected_product()
    context.amazon_page.add_selected_product_to_cart()
    context.selected_products.append(selected_product)


@then("el carrito debe contener los dos productos seleccionados")
def step_verify_selected_products(context):
    context.amazon_page.open_cart()
    context.amazon_page.verify_products_are_in_cart(context.selected_products)


@then("el subtotal debe coincidir con la suma de los productos")
def step_verify_subtotal(context):
    context.amazon_page.open_cart()
    context.amazon_page.verify_subtotal_matches_selected_products(context.selected_products)

