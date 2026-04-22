from datetime import datetime
from typing import List

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from app.schemas.response import ConnectionRequest


def _extract_name_from_button(aria_label: str) -> str:
    """
    Extrai o nome da pessoa a partir do aria-label do botão.
    Exemplo: 'Convidar João Silva para se conectar' → 'João Silva'
    """
    label = aria_label or ""
    prefix = "Convidar "
    suffix = " para se conectar"
    if label.startswith(prefix) and label.endswith(suffix):
        return label[len(prefix) : -len(suffix)].strip()
    return label.strip()


def _extract_profile_url_from_button(page: Page, button) -> str:
    """
    Tenta obter a URL do perfil a partir do elemento mais próximo com link de perfil.
    Percorre o DOM pai do botão em busca de um <a href> que aponte para /in/...
    """
    try:
        # O botão fica dentro de um li/card — procura o link de perfil no container
        profile_link = button.locator(
            "xpath=ancestor::li//a[contains(@href,'/in/')]"
        ).first
        href = profile_link.get_attribute("href")
        if href:
            return href.split("?")[0].rstrip("/")
    except Exception:
        pass
    return ""


def search_recruiters(
    page: Page,
    search: str,
    count: int,
) -> List[ConnectionRequest]:
    """
    Navega até a pesquisa do LinkedIn, filtra por Pessoas e envia convites
    para até `count` pessoas. Retorna a lista de ConnectionRequest com nome
    e URL de perfil de cada pessoa convidada.
    """
    print("iniciando a busca")
    connection_requests: List[ConnectionRequest] = []

    # ── Pesquisa ──────────────────────────────────────────────────────────────
    search_input = page.locator(
        'input[data-testid="typeahead-input"][placeholder="Pesquisar"]'
    )
    search_input.fill(search)
    search_input.press("Enter")
    page.wait_for_timeout(3000)

    # Filtra por "Pessoas"
    page.locator('[data-testid="interop-iframe"]').content_frame.get_by_role(
        "button", name="Pessoas"
    ).click()
    page.wait_for_timeout(3000)

    # ── Loop de convites ──────────────────────────────────────────────────────
    this_count = 0

    while this_count < count:
        try:
            buttons = page.locator(
                'button[aria-label^="Convidar"][aria-label$="para se conectar"]'
            )

            # Avança páginas até encontrar botões disponíveis
            while buttons.count() == 0:
                print("proxima página")
                page.locator('button[aria-label="Avançar"]:visible').click()
                page.wait_for_timeout(3000)
                buttons = page.locator(
                    'button[aria-label^="Convidar"][aria-label$="para se conectar"]'
                )

            print(
                f"Encontrados {buttons.count()} botões de convite na página atual"
            )

            for i in range(buttons.count()):
                if this_count >= count:
                    break

                print(f"Tentando convidar pessoa {i + 1} da página atual")
                try:
                    btn = buttons.nth(i)
                    aria_label = btn.get_attribute("aria-label") or ""
                    name = _extract_name_from_button(aria_label)
                    profile_url = _extract_profile_url_from_button(page, btn)

                    btn.click()
                    page.wait_for_timeout(2000)
                    page.wait_for_selector('button[aria-label="Enviar sem nota"]')
                    page.locator('button[aria-label="Enviar sem nota"]').click()
                    page.wait_for_timeout(1500)

                    this_count += 1

                    req = ConnectionRequest(
                        name=name,
                        profile_url=profile_url or None,
                        sent_at=datetime.now().isoformat(timespec="seconds"),
                    )
                    connection_requests.append(req)
                    print(
                        f"Convidado {this_count}/{count}: {name} ({profile_url})"
                    )

                except PlaywrightTimeoutError:
                    print(
                        f"Não foi possível convidar a pessoa {i + 1}. "
                        "Continuando para o próximo."
                    )

            if this_count < count:
                # Avança para a próxima página de resultados
                try:
                    page.locator('button[aria-label="Avançar"]:visible').first.click()
                    page.wait_for_timeout(3000)
                except PlaywrightTimeoutError:
                    print("Sem mais páginas de resultados.")
                    break

        except PlaywrightTimeoutError:
            print(
                "Não foi possível encontrar o botão de convidar ou avançar. "
                "Verifique se a estrutura da página mudou ou se há algum bloqueio."
            )
            break

    print(f"Total de convites enviados: {len(connection_requests)}")
    return connection_requests
