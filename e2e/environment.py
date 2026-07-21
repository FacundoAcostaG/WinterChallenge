# ============================================
# CHEATSHEET BEHAVE - environment.py (hooks)
# ============================================
# Orden de ejecución de los hooks de Behave:
#   before_all(context)                -> una vez, antes de toda la corrida
#     before_feature(context, feature)     -> antes de cada .feature
#       before_scenario(context, scenario)     -> antes de cada Scenario
#         before_step(context, step)               -> antes de cada step (opcional)
#         after_step(context, step)                -> después de cada step (opcional)
#       after_scenario(context, scenario)       -> después de cada Scenario
#     after_feature(context, feature)      -> después de cada .feature
#   after_all(context)                 -> una vez, al final de toda la corrida
#
# `context` viaja entre hooks y steps: todo lo que se cuelga acá
# (context.browser, context.page, etc.) queda disponible en los steps.
# ============================================

import os

from pages.search_page import SearchPage

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

# HEADLESS=false behave         -> corre con navegador visible
# PWDEBUG=1 behave              -> abre el Playwright Inspector (fuerza headed igual)
# SLOW_MO=0 behave              -> desactiva la espera entre acciones
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"
SLOW_MO = int(os.getenv("SLOW_MO", "500"))  # ms de espera entre cada acción de Playwright


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=HEADLESS, slow_mo=SLOW_MO
    )


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context(locale="en-US")
    context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.page = context.browser_context.new_page()
    # TODO: instanciar acá los Page Objects que se usen en los steps
    context.search_page = SearchPage(context.page)




def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.browser_context.tracing.stop(path=f"traces/{scenario.name}.zip")
    else:
        context.browser_context.tracing.stop(path=f"traces/{scenario.name}.zip")  # descarta el trace si pasó
        context.browser_context.close()




def after_all(context):
    context.browser.close()
    context.playwright.stop()