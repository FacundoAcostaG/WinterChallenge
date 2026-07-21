# ============================================
# CHEATSHEET BEHAVE - steps
# ============================================
# @given / @when / @then / @step  -> decoran la función que matchea el texto del .feature
# "texto {variable}"              -> parse type; llega como argumento a la función (string)
# "texto {n:d}"                   -> parse type numérico (int)
# context                         -> objeto compartido entre steps/hooks (ver environment.py)
# assert condicion, "mensaje"     -> forma estándar de validar en behave (sin pytest)
# context.page                    -> instancia de Playwright Page (creada en environment.py)
# Los steps NO deberían tener selectores hardcodeados -> delegar en Page Objects
# ============================================

from behave import given, when, then
from pages.search_page import SearchPage

@given('que el usuario está en la página principal')
def step_impl(context): # type: ignore
      context.search_page = SearchPage(context.page)
      context.search_page.visit()


@when('busca la película "{titulo}"')
def step_impl(context, titulo): # type: ignore
    context.search_page.buscar(titulo)

@when('ingresa a la página de la película')
def step_impl(context): # type: ignore
    context.movie_page = context.search_page.abrir_primer_resultado()

@then('el director debe ser "{director}"')
def step_impl(context, director): # type: ignore
    context.director = context.movie_page.obtener_director()
    assert context.director == director, f"Wanted = {director}, but got = {context.director}"


@then('la calificación debe ser superior a {calificacion:f}')
def step_impl(context, calificacion): # type: ignore
    context.puntaje = context.movie_page.obtener_puntaje()
    assert context.puntaje > calificacion, f"Wanted > {calificacion}, but got = {context.puntaje}"


@then('se guarda una captura de pantalla con las validaciones')
def step_impl(context): # type: ignore
    context.page.screenshot(path="screenshots/ice_age.png")
