"Ta elao, a mirar una peli"
Automatizar un flujo completo de búsqueda y validación en IMDb o TMDB, simulando el
comportamiento de alguien que, encerrado por el frío, busca una buena película invernal.
Objetivos
    ○ Buscar la película "Ice Age" (La Era de Hielo).
    ○ Ingresar a la página de la película.
    ○ Validar que:
    ■ Aparece el director "Chris Wedge"
    ■ La película tiene una calificación superior a 7.0

Bonus: Guardar una captura de pantalla con las validaciones anteriores.
Para ambos casos, se debe de utilizar sintaxis Gherkin y Page Object Model.
Tecnologías sugeridas:
    ○ Behave + Playwright

# Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    cp .env.example .env   # ajustar BASE_URL si se usa TMDB en vez de IMDb

# Correr los tests

    behave

# Debug

    HEADLESS=false behave          # ver el navegador correr
    HEADLESS=false SLOW_MO=500 behave   # + cámara lenta (ms entre acciones)
    PWDEBUG=1 behave                # Playwright Inspector (headed + pausa + step-by-step)

    # o dentro de un step/page object, para pausar en un punto puntual:
    self.page.pause()

# Estructura

    features/
      buscar_peli.feature          -> escenario Gherkin (Given/When/Then)
      environment.py                -> hooks de behave (setup/teardown de Playwright)
      steps/
        home_steps.py                -> steps de la página principal (visitar, buscar)
        results_steps.py             -> steps de los resultados (seleccionar película)
        movie_steps.py               -> steps de la ficha de película (director, calificación, captura)
      pages/
        home_page.py                 -> home + buscador
        results_page.py               -> resultados de la búsqueda, selección de película
        movie_page.py                -> ficha de película (director, calificación)

Lo que falta implementar (marcado con TODO / NotImplementedError):
    ○ Locators reales de IMDb o TMDB
    ○ Lógica de búsqueda y navegación en HomePage/ResultsPage
    ○ Lectura de director/calificación en MoviePage
    ○ Conexión de esa lógica en los steps

    