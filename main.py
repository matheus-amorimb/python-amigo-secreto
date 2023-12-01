import json
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from AmigoOculto import AmigoOculto


def main(amigo_oculto_dict: dict, texto: str):
    """
    Envia mensagens no WhatsApp para os participantes do Amigo Oculto.

    Args:
        amigo_oculto_dict (dict): Dicionário contendo os participantes e seus amigos sorteados.
        texto (str): Mensagem a ser enviada, com placeholders para participante e sorteado.

    Returns:
        None
    """
    # Inicializa o navegador Chrome
    navegador = webdriver.Chrome()
    navegador.get('https://web.whatsapp.com/')

    # Aguarda até que o elemento 'side' seja encontrado, indicando que o WhatsApp Web foi carregado
    while not navegador.find_elements(By.ID, 'side'):
        time.sleep(1)

    time.sleep(2)

    # Itera sobre os participantes e seus amigos sorteados
    for key, value in amigo_oculto_dict.items():
        participante = key
        amigo_sorteado = value['amigoX']
        numero = value['telefone']

        # Substitui os placeholders na mensagem
        msg = texto
        msg = msg.replace('participante', participante).replace(
            'sorteado', amigo_sorteado
        )
        msg = quote(msg)

        # Constrói o link para enviar a mensagem no WhatsApp
        link = f'https://web.whatsapp.com/send?phone={numero}&text={msg}'

        # Abre o link no navegador
        navegador.get(link)

        # Aguarda até que o botão de envio da mensagem seja encontrado
        while not navegador.find_elements(
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span',
        ):
            pass

        time.sleep(2)

        try:
            # Envia a mensagem pressionando a tecla ENTER
            navegador.find_element(
                By.XPATH,
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span',
            ).send_keys(Keys.ENTER)
            time.sleep(5) #Ajustar conforme a velocidade da sua internet

        except Exception as e:
            print(f'Um erro aconteceu: \n {e}')
    
    print('Sorteio realizado com sucesso')


if __name__ == '__main__':
    # Carrega os participantes do arquivo JSON
    with open('participantes.JSON') as participantes_file:
        participantes_dict = json.load(participantes_file)

    # Cria uma instância da classe AmigoOculto e realiza o sorteio
    amigo_oculto_familia = AmigoOculto()
    amigo_oculto_familia.inserir_participante(participantes_dict)
    amigo_oculto_familia.sortear()

    # Salva o resultado do sorteio em um arquivo JSON
    result = amigo_oculto_familia.sorteio
    with open('resultado.JSON', 'w', encoding='utf-8') as resultado:
        json.dump(result, resultado, indent=2, ensure_ascii=False)

    # Lê o texto da mensagem a ser enviado
    with open('mensagens.txt') as mensagem:
        texto = mensagem.read()

    # Chama a função principal para enviar as mensagens no WhatsApp
    main(amigo_oculto_dict=amigo_oculto_familia.sorteio, texto=texto)

