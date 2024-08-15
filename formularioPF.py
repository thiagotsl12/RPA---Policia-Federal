from playwright.sync_api import sync_playwright
import time
import pyautogui

def preencheForms(cidade_nasc, pais_nasc,nome, sobrenome, sexo, nascido_em, nacionalidade, pai, mae, 
                  estado_civil, dt_nascimento, numero_passaporte, pais_passaporte, dt_concessao, cidade, pais, numero_visto, pais_expedidor):
    with sync_playwright() as p:
        # Inicializa o navegador (pode ser 'chromium', 'firefox' ou 'webkit')
        browser = p.chromium.launch(headless=False)
        
        # Cria uma nova página com tamanho de janela especificado
        page = browser.new_page(viewport={"width": 1720, "height": 750})  # Defina a largura e altura da janela aqui
        
        # Define o tempo de espera máximo em segundos
        timeout = 10000
        
        try:
            # Abre a página desejada
            page.goto("https://servicos.dpf.gov.br/sismigra-internet/faces/publico/tipoSolicitacao/solicitarRegistroEmissaoCie.seam")
            
            page.wait_for_selector('input[id="txtNomeCompleto"]', timeout=timeout)
            page.select_option('select[id="tipoRegistro"]', label="Registro de Visto Consular")    
            page.fill('input[id="txtNomeCompleto"]', nome)
            page.fill('input[id="txtSobrenome"]', sobrenome)
            if sexo == 'Masculino':page.check('input[id="idRadioSexo:0"]') 
            else:page.check('input[id="idRadioSexo:1"]')
            page.select_option('select[id="idCondicaoEspecial"]', label="NENHUMA") 
            page.fill('input[id="calDtNascInputDate"]', dt_nascimento)
            page.select_option('select[id="cmbTipoEstadoCivil"]', label=estado_civil.upper()) 
            page.fill('input[id="txtCidadeNascimento"]', cidade_nasc)
            page.select_option('select[id="cmbPaisNascimento"]', label=pais_nasc)
            page.select_option('select[id="paisNacionalidade"]', label=pais_nasc)
            page.fill('input[id="txtEmail"]', "appointmentsdeloitte@deloitte.com")
            page.click('textarea[id="idDescricaoOcupacao"]')
            page.keyboard.type("990")
            page.wait_for_timeout(3000)
            page.keyboard.press('Enter')
            page.fill('input[id="txtNomeDaMae"]', mae)
            page.check('input[id="txtSexoDaMae:1"]')
            page.fill('input[id="txtNomePai"]', pai)
            page.check('input[id="txtSexoDoPai:0"]')
            
            page.click('input[id="idAvancarMail"]')
            
            pyautogui.moveTo(792, 392)
            pyautogui.click()
            page.wait_for_selector('input[id="txtNumeroVisto"]', timeout=timeout)
            page.click('input[id="txtNumeroVisto"]')
            time.sleep(2)
            pyautogui.write(numero_visto)
            page.fill('input[id="dataConcessaoInputDate"]', dt_concessao)
            page.fill('input[id="txtCidadeVisto"]', cidade)
            page.select_option('select[id="idPaisVisto"]', label=pais)
            page.select_option('select[id="idTipoDocumentoIdentificacao"]', label="Passaporte")
            page.fill('input[id="txtNrDocumento"]', numero_passaporte)
            page.select_option('select[id="paisExpedidor"]', label=pais_expedidor)
            page.select_option('select[id="idSiglaUF"]', label="AC")
            page.select_option('select[id="comboLocalEntrada"]', label="ASSIS BRASIL")
            page.select_option('select[id="meioTransporte"]', label="Terrestre")
            page.fill('input[id="dataEntradaInputDate"]', "25/08/2024")

            page.click('input[id="idAvancarConcessaoVisto"]')

            page.wait_for_selector('input[id="cep1"]', timeout=timeout)
            page.click('input[id="cep1"]')
            time.sleep(2)
            pyautogui.write("04711130")
            pyautogui.press("tab")
            time.sleep(4)
            page.fill('input[id="txtLogradouro"]', "Av. Dr. Chucri Zaidan")
            page.fill('input[id="txtComplemento"]', "Andar 12")
            page.fill('input[id="txtDistritoBairro"]', "Vila Sao Francisco")
            page.select_option('select[id="txtUf"]', label="SP")
            page.select_option('select[id="comboCidadeEndResidencial"]', label="São Paulo")
            page.fill('input[id="telefone"]', "11112233441")
            page.fill('input[id="txtNomeComercial"]', "Deloitte")
            page.click('input[id="cep3"]')
            time.sleep(2)
            pyautogui.write("04711130")
            pyautogui.press("tab")
            time.sleep(4)
            page.fill('input[id="txtLogradouro2"]', "Av. Dr. Chucri Zaidan")
            page.fill('input[id="areaTxtComplementoComercial"]', "Andar 12")
            page.fill('input[id="txtBairro"]', "Vila Sao Francisco")
            page.select_option('select[id="naoPossuiEC"]', label="SP")
            page.select_option('select[id="comboCidadeEndResidencial2"]', label="São Paulo")
            page.fill('input[id="telefone-comercial"]', "11112233441")

            page.click('input[id="idAvancar"]')


            #page.wait_for_selector('input[id="declaracao"]', timeout=timeout) 
            #page.click('input[id="declaracao"]')
            #page.click('input[id="idSalvar"]')


        finally:
            # Fecha o navegador no final do script
            browser.close()

if __name__ == "__main__":
    preencheForms()
