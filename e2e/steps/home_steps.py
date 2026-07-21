from behave import given, when
from pages.home_page import HomePage


@given('que el usuario está en la página principal')
def step_impl(context): # type: ignore
    context.home_page = HomePage(context.page)
    context.home_page.visit()


@when('busca la película "{titulo}"')
def step_impl(context, titulo): # type: ignore
    context.results_page = context.home_page.buscar(titulo)
