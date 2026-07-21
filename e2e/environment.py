import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


E2E_DIR = Path(__file__).resolve().parent
if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))

ARTIFACTS_DIR = E2E_DIR / "artifacts"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
TRACES_DIR = ARTIFACTS_DIR / "traces"


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()


def before_all(context):
    for directory in (VIDEOS_DIR, SCREENSHOTS_DIR, TRACES_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    headless = _as_bool(os.getenv("PW_HEADLESS"), default=False)
    slow_mo = int(os.getenv("PW_SLOW_MO", "500"))

    context.playwright_manager = sync_playwright().start()
    context.browser = context.playwright_manager.chromium.launch(
        headless=headless,
        slow_mo=slow_mo,
    )


def before_scenario(context, scenario):
    context.scenario_slug = _slugify(scenario.name)
    context.browser_context = context.browser.new_context(
        record_video_dir=str(VIDEOS_DIR),
        record_video_size={"width": 1440, "height": 900},
    )
    context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(15000)
    context.selected_products = []


def after_scenario(context, scenario):
    failed = str(scenario.status).lower() == "failed"

    if failed:
        context.page.screenshot(
            path=str(SCREENSHOTS_DIR / f"{context.scenario_slug}.png"),
            full_page=True,
        )
        context.browser_context.tracing.stop(
            path=str(TRACES_DIR / f"{context.scenario_slug}.zip")
        )
    else:
        context.browser_context.tracing.stop()

    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright_manager.stop()
