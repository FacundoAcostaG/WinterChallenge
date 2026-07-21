from behave import then


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
