# Winter Challenge

Base inicial para resolver el challenge con foco en pruebas de API usando Playwright + TypeScript.

## Stack elegido

- API testing: Playwright Test
- Lenguaje: TypeScript
- Estructura simple: clientes por API + utilidades compartidas + una sola spec principal

## Alcance actual

El módulo de API incluye:

- validaciones de contrato
- casos de respuesta esperada y no esperada
- una prueba de integración entre TheMealDB y Open-Meteo
- un bloque con dataset dinámico de 5 entradas

## Instalación

```bash
npm install
```

## Ejecución

```bash
npm run test:api
```

## Performance con k6

La parte de performance está concentrada en un solo archivo:

`performance/winter-challenge.k6.js`

Para ejecutarla:

```bash
npm run test:performance
```

Requiere tener `k6` instalado en la máquina.

## E2E con Behave + Playwright

La parte E2E quedó armada en:

`e2e/`

Con separación en:

- `features`
- `steps`
- `pages` (Page Object Model)

Instalación:

```bash
pip install -r e2e/requirements.txt
python -m playwright install chromium
```

Ejecución:

```bash
behave e2e/features/amazon_winter_cart.feature
```

## Organización actual

Los tests de API están concentrados en un único archivo spec para que el flujo quede más fácil de leer.
