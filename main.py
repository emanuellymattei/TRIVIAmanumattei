import html
import requests

def traduzir(text):
    url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=pt-BR&q={html.unescape(text)}"
    traducao = requests.get(url)

    if traducao.status_code == 200:
        traducao = traducao.json()
        return traducao [0][0]
    else:
        print('Error fetching translator: status code: {traducao.status_code}')
        return html.unescape(text)
    
#print(traduzir('The world is falling apart'))

def buscarPerguntas():
    url = f'https://opentdb.com/api.php?amount=6&category=10&difficulty=easy'
    perguntas = requests.get(url)

    if perguntas.status_code == 200:
        perguntas = perguntas.json()
        return perguntas['results']
    else:
        print(f'Error fetching Trivia: status code: {perguntas.status_code}')
        return []
    
lista_de_perguntas = buscarPerguntas()

for pergunta in lista_de_perguntas:
    print(f'Original: {pergunta['question']}')
    print(f'Tradução: {traduzir(pergunta['question'])}')
    print('-------------------------------')

import html
import random
import requests
from tradutor import traduzir


def buscar_perguntas(qtd=5, categoria=None, dificuldade=None):
    """
    Busca perguntas da API do OpenTriviaDB.
    - qtd: quantidade de perguntas
    - categoria: categoria numérica (opcional)
    - dificuldade: easy, medium, hard ou None
    """
    parametros = {'amount': qtd}
    if categoria is not None:
        parametros['category'] = categoria
    if dificuldade is not None:
        parametros['difficulty'] = dificuldade

    url = 'https://opentdb.com/api.php'
    resposta = requests.get(url, params=parametros)
    resposta.raise_for_status()

    dados = resposta.json()
    return dados.get('results', [])
