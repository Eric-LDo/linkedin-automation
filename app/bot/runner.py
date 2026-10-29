import os
from contextlib import suppress
from typing import Union

from playwright.sync_api import Browser, sync_playwright
from seleniumbase import sb_cdp

from app.schemas.request import AutomationRequest
from app.schemas.response import AutomationResponse
from app.bot.navigation import navigate_and_connect
from app.utils.proxy import get_random_proxy


def _get_or_create_page(browser: Browser):
    if browser.contexts:
        context = browser.contexts[0]
    else:
        context = browser.new_context()

    if context.pages:
        return context.pages[0]
    return context.new_page()


def run_Bot(payload: Union[AutomationRequest]) -> dict:
    proxy = (
        get_random_proxy()
        if os.getenv("USE_PROXY", "false").lower() == "true"
        else None
    )
    sb = None

    try:
        sb = sb_cdp.Chrome(
            locale="pt-BR",
            headless=False,
            disable_gpu=True,
            incognito=True,
            stealth=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            ),
            proxy=proxy,
        )

        endpoint_url = sb.get_endpoint_url()

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            try:
                page = _get_or_create_page(browser)
                result: AutomationResponse = navigate_and_connect(page, payload)
                # Converte para dict serializável pelo FastAPI
                return result.model_dump()
            finally:
                with suppress(Exception):
                    browser.close()

    except Exception as e:
        return AutomationResponse(
            status="error",
            message=str(e),
        ).model_dump()
    finally:
        if sb is not None:
            with suppress(Exception):
                sb.driver.quit()
