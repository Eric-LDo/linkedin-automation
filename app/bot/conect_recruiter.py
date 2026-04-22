from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

def search_recruiters(page: Page, search:str, count:int):
    print('iniciando a busca')

    search_input = page.locator('input[data-testid="typeahead-input"][placeholder="Pesquisar"]')
    search_input.fill(search)
    search_input.press('Enter')
    page.wait_for_timeout(3000)
    page.locator("[data-testid=\"interop-iframe\"]").content_frame.get_by_role("button", name="Pessoas").click()
    page.wait_for_timeout(3000)


    #estrutura de repetição para ser o mesmo numero de convites de count
    this_count = 0
    while this_count < count:
        #pegar todos os botões de convidar da página
        try:
            buttons = page.locator('button[aria-label^="Convidar"][aria-label$="para se conectar"]')
            print(f'Procurando por recrutadores para convidar na página atual. Botões encontrados: {buttons.count()}')
            while buttons.count() == 0:
                print('proxima página')
                page.locator('button[aria-label="Avançar"]:visible').click()
                buttons = page.locator('button[aria-label^="Convidar"][aria-label$="para se conectar"]')
            buttons.first.click()
            page.locator('button[aria-label="Enviar sem nota"]').click()
                
            #clicar em cada botão de convidar, e em convidar sem nota
            
            print(f'Encontrados {buttons.count()} recrutadores para convidar na página atual')
            for i in range(buttons.count()):
                print(f'Tentando convidar recrutador {i+1} da página atual')
                try:
                    buttons.nth(i).click()
                    page.wait_for_timeout(2000)
                    page.wait_for_selector('button[aria-label="Enviar sem nota"]')
                    page.locator('button[aria-label="Enviar sem nota"]').click()
                    this_count += 1
                    if this_count == count:
                        print(f'Número de convites enviados: {this_count}. Alcançado o limite definido.')
                        return True
                    print(f'Convidado {this_count} de {count}')
                    

                except PlaywrightTimeoutError:
                    print(f'Não foi possível convidar o recrutador {i+1}. Continuando para o próximo.')
            #clicar no botão de próxima página
            page.locator('button[aria-label="Avançar"]:visible').first.click()
            page.wait_for_timeout(3000)
            #só termina quando chegar no número de convites ou não tiver mais páginas
        except PlaywrightTimeoutError:
            print('Não foi possível encontrar o botão de convidar ou avançar. Verifique se a estrutura da página mudou ou se há algum bloqueio.')
            break
    return True
    

