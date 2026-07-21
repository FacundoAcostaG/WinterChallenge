from behave import when


@when('ingresa a la página de la película')
def step_impl(context): # type: ignore
    context.movie_page = context.results_page.abrir_primer_resultado()
