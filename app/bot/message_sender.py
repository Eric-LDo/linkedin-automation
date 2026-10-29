"""
Responsável por:
1. Navegar até a aba "Minha Rede" (conexões aceitas recentemente).
2. Identificar conexões novas que ainda não receberam a mensagem inicial.
3. Enviar a mensagem personalizada via chat do LinkedIn.
4. Marcar cada pessoa como "já recebeu mensagem" no store persistente.

Regra principal: uma pessoa NÃO pode receber a mensagem se já recebeu
em qualquer execução anterior (controlado pelo message_store).
"""

from datetime import datetime
from typing import List

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from app.schemas.response import MessageSent
from app.utils.message_store import already_received_message, mark_message_sent

# ── URL da página de conexões ─────────────────────────────────────────────────
MY_NETWORK_URL = "https://www.linkedin.com/mynetwork/invite-connect/connections/"


def _build_message(first_name: str, skills: str) -> str:
    """Monta a mensagem personalizada com o primeiro nome e as habilidades."""
    return (
        f"{first_name} obrigado pela conexão!! "
        "Estou avaliando algumas oportunidades de mercado e adoraria marcar "
        "uma conversa rápida com você para falar um pouco mais sobre a minha "
        f"experiência com {skills} e entender um pouco os desafios atuais da empresa.\n\n"
        "O que acha? Como está sua disponibilidade essa semana?"
    )


def send_messages_to_new_connections(
    page: Page,
    skills: str,
) -> List[MessageSent]:
    """
    Percorre a lista de conexões recentes no LinkedIn e envia a mensagem
    somente para quem ainda não a recebeu. Retorna a lista de MessageSent.
    """
    messages_sent: List[MessageSent] = []

    print("Navegando para a página de conexões...")
    page.goto(MY_NETWORK_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    # Coleta todos os cards de conexão visíveis na página
    # Seletor genérico: cada conexão tem um link de perfil e um botão de mensagem
    connection_cards = page.locator("li.mn-connection-card")
    total_cards = connection_cards.count()
    print(f"Conexões encontradas na página: {total_cards}")

    for i in range(total_cards):
        try:
            card = connection_cards.nth(i)

            # ── Nome e URL do perfil ───────────────────────────────────────
            profile_link = card.locator("a.mn-connection-card__link").first
            full_name = (
                card.locator("span.mn-connection-card__name").first.inner_text().strip()
            )
            profile_url_raw = profile_link.get_attribute("href") or ""
            profile_url = profile_url_raw.split("?")[0].rstrip("/")

            first_name = full_name.split()[0] if full_name else "Olá"

            print(f"Verificando: {full_name} ({profile_url})")

            # ── Verificação de duplicidade ────────────────────────────────
            if already_received_message(profile_url or None, full_name):
                print(f"  ↳ Já recebeu mensagem. Pulando.")
                continue

            # ── Clica no botão "Mensagem" do card ─────────────────────────
            msg_button = card.locator('button:has-text("Mensagem")')
            if msg_button.count() == 0:
                print(f"  ↳ Botão de mensagem não encontrado. Pulando.")
                continue

            msg_button.first.click()
            page.wait_for_timeout(2000)

            # ── Digita e envia a mensagem ──────────────────────────────────
            message_text = _build_message(first_name, skills)

            # Caixa de texto do chat
            chat_box = page.locator(
                'div.msg-form__contenteditable[contenteditable="true"]'
            ).last
            chat_box.click()
            chat_box.fill(message_text)
            page.wait_for_timeout(1000)

            # Botão de enviar
            send_btn = page.locator('button.msg-form__send-button[type="submit"]').last
            send_btn.click()
            page.wait_for_timeout(2000)

            # ── Marca no store e registra na lista ────────────────────────
            mark_message_sent(profile_url or None, full_name)

            sent = MessageSent(
                name=full_name,
                profile_url=profile_url or None,
                sent_at=datetime.now().isoformat(timespec="seconds"),
                message_preview=message_text[:120] + "...",
            )
            messages_sent.append(sent)
            print(f"  ↳ Mensagem enviada para {full_name}.")

            # Fecha o chat aberto (tecla Escape ou botão fechar)
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(800)
            except Exception:
                pass

        except PlaywrightTimeoutError:
            print(f"  ↳ Timeout ao processar conexão {i + 1}. Continuando.")
        except Exception as exc:
            print(f"  ↳ Erro ao processar conexão {i + 1}: {exc}. Continuando.")

    print(f"Total de mensagens enviadas nesta execução: {len(messages_sent)}")
    return messages_sent
