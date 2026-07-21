# E2E - Amazon winter cart

Suite E2E con Behave, Gherkin, Playwright y Page Object Model.

## Estructura

```text
e2e/
  features/
    amazon_winter_cart.feature
  steps/
    amazon_winter_cart_steps.py
  pages/
    amazon_page.py
  environment.py
  requirements.txt
```

## Instalacion

```bash
pip install -r e2e/requirements.txt
python -m playwright install chromium
```

## Ejecucion

```bash
python -m behave e2e
```

En Windows, si `py` esta disponible:

```bash
py -m behave e2e
```

## Auditoria de fallos

El navegador abre visible por defecto. Si falla el escenario, se guardan:

- videos en `e2e/artifacts/videos/`
- screenshots en `e2e/artifacts/screenshots/`
- traces en `e2e/artifacts/traces/`

Para correr oculto:

```powershell
$env:PW_HEADLESS="true"
$env:PW_SLOW_MO="0"
python -m behave e2e
```

Para abrir un trace:

```bash
playwright show-trace e2e/artifacts/traces/<scenario>.zip
```
