from playwright.sync_api import Page
from typing import Union
from app.schemas.request import AutomationRequest
from app.bot.conect_recruiter import search_recruiters
LOGIN_URL = "https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
FEED_URL_PREFIX = "https://www.linkedin.com/feed"

def navigate_and_connect(page: Page, payload: Union[AutomationRequest]):
    login(page, payload)
    search_recruiters(page, payload.search, payload.count)
    page.pause()
    
    


def login(page: Page, payload:Union[AutomationRequest]):
    print('iniciando login')
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.locator("#username").fill(payload.email)
    page.locator("#password").fill(payload.password)
    page.get_by_role("button", name="Entrar", exact=True).click()
    page.pause()
    page.wait_for_timeout(3000)
    print('login realizado com sucesso')
    
    current_url = page.url
    print(f'url atual {page.url}')

    if (current_url.startswith(FEED_URL_PREFIX)):
        return True
    else:
        raise ValueError(f"Login invalido ou bloqueado.")
    



    
