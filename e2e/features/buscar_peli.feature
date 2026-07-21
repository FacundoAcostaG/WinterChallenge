# ============================================
# CHEATSHEET GHERKIN - referencia rápida
# ============================================
# Feature          -> agrupa escenarios relacionados
# Background       -> pasos comunes antes de cada Scenario
# Scenario         -> un caso de prueba concreto
# Scenario Outline -> escenario parametrizado + Examples
# Given            -> precondición / estado inicial
# When             -> acción que dispara el comportamiento
# Then             -> resultado esperado / validación
# And / But        -> encadena pasos del mismo tipo
# """ ... """      -> Doc String (texto largo)
# | col | col |    -> Data Table
# @tag             -> filtra ejecución (behave --tags=tag)
# ============================================

Feature: Búsqueda de películas invernales
    Como usuario que busca qué ver en una tarde fría
    Quiero buscar una película y validar su información
    Para asegurarme de elegir una buena película

    Scenario: Buscar "Ice Age" y validar director y calificación
        Given que el usuario está en la página principal
        When busca la película "Ice Age"
        And ingresa a la página de la película
        Then el director debe ser "Chris Wedge"
        And la calificación debe ser superior a 70.0
        And se guarda una captura de pantalla con las validaciones
        