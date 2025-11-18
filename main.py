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

def montar_pergunta(item):
    """
    Organiza a pergunta, alternativas e resposta correta.
    """
    pergunta = html.unescape(item['question'])
    correta = html.unescape(item['correct_answer'])
    incorretas = [html.unescape(x) for x in item['incorrect_answers']]

    opcoes = incorretas + [correta]
    random.shuffle(opcoes)

    return {
        'pergunta': pergunta,
        'opcoes': opcoes,
        'correta': correta
    }

import random

def exibir_pergunta(pergunta):
    """
    Exibe uma pergunta no terminal, embaralha as alternativas
    e retorna a lista embaralhada junto com a resposta correta.

    Parâmetros:
        pergunta (dict): dicionário contendo 'question', 'correct_answer', 'incorrect_answers'

    Retorna:
        alternativas_embaralhadas (list): lista com todas as alternativas embaralhadas
        resposta_correta (str): texto da resposta correta
    """

    texto_pergunta = pergunta['question']
    resposta_correta = pergunta['correct_answer']
    respostas_erradas = pergunta['incorrect_answers']

    # Junta todas as alternativas
    alternativas = respostas_erradas + [resposta_correta]

    # Embaralha
    random.shuffle(alternativas)

    # Exibe a pergunta formatada
    print("\n----------------------------------")
    print(f"Pergunta: {texto_pergunta}")
    print("----------------------------------")

    # Exibe alternativas enumeradas
    for indice, alternativa in enumerate(alternativas, start=1):
        print(f"{indice}. {alternativa}")

    return alternativas, resposta_correta

def verificar_resposta(alternativas, resposta_correta):
    """
    Recebe a lista de alternativas exibidas e verifica se o usuário
    escolheu a resposta correta.

    Parâmetros:
        alternativas (list): lista de alternativas embaralhadas
        resposta_correta (str): texto da alternativa correta

    Retorna:
        True se acertou, False se errou
    """

    while True:
        escolha = input("\nDigite o número da alternativa: ")

        # Confere se digitou um número válido
        if escolha.isdigit():
            escolha = int(escolha)

            if 1 <= escolha <= len(alternativas):
                break
            else:
                print("Número inválido! Digite um número que esteja na lista.")
        else:
            print("Entrada inválida! Digite apenas números.")

    # Descobre qual alternativa foi escolhida
    alternativa_escolhida = alternativas[escolha - 1]

    # Confere se está correta
    if alternativa_escolhida == resposta_correta:
        print("✅ Resposta correta! Muito bem!")
        return True
    else:
        print(f"❌ Resposta errada! A correta era: {resposta_correta}")
        return False

def jogar_trivia():
    print("\n===== 🎮 JOGO DE TRIVIA – BEM-VINDO! =====\n")

    # Escolha da dificuldade
    print("Escolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Médio")
    print("3 - Difícil")

    while True:
        nivel = input("Digite o número da dificuldade: ")

        if nivel == "1":
            dificuldade = "easy"
            break
        elif nivel == "2":
            dificuldade = "medium"
            break
        elif nivel == "3":
            dificuldade = "hard"
            break
        else:
            print("Opção inválida! Escolha 1, 2 ou 3.")

    print(f"\n🔎 Buscando perguntas de dificuldade: {dificuldade}...\n")

    perguntas = fetch_trivia(dificuldade)

    if not perguntas:
        print("Erro ao carregar perguntas. Tente novamente mais tarde.")
        return

    pontuacao = 0
    total = len(perguntas)

    # Loop das perguntas
    for idx, item in enumerate(perguntas, start=1):

        dados = montar_pergunta(item)

        print(f"\n🔹 Pergunta {idx}/{total}:")
        print(dados['pergunta'])

        print("\nOpções:")
        for i, opcao in enumerate(dados['opcoes'], start=1):
            print(f"{i} - {opcao}")

        # Verificar resposta do usuário
        acertou = verificar_resposta(dados['opcoes'], dados['correta'])

        if acertou:
            pontuacao += 1

    # Resultado final
    print("\n===== 🏁 RESULTADO FINAL =====")
    print(f"Você acertou {pontuacao} de {total} perguntas!")
    print("Muito bem!" if pontuacao > total/2 else "Continue praticando!")

