import requests
import html
import random
from tradutor import traduzir

# ---------------------------
# BUSCA PERGUNTAS DA API
# ---------------------------
def fetch_trivia(dificuldade):
    url = f'https://opentdb.com/api.php?amount=5&difficulty={dificuldade}&type=multiple'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return dados['results']
    else:
        print(f"Erro ao buscar perguntas. Código HTTP: {response.status_code}")
        return []


# ---------------------------
# MONTA PERGUNTA COM OPÇÕES
# ---------------------------
def montar_pergunta(item):
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


# ---------------------------
# VERIFICA RESPOSTA
# ---------------------------
def verificar_resposta(opcoes, correta):
    while True:
        try:
            escolha = int(input("\nDigite o número da resposta: "))
            if 1 <= escolha <= len(opcoes):
                break
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Digite apenas números.")

    resposta_escolhida = opcoes[escolha - 1]

    if resposta_escolhida == correta:
        print("✔ Resposta correta!")
        return True
    else:
        print(f"❌ Resposta incorreta! A correta era: {correta}")
        return False


# ---------------------------
# FUNÇÃO PRINCIPAL DO JOGO
# ---------------------------
def jogar_trivia():

    print("\n===== 🎮 BEM-VINDO AO JOGO DE TRIVIA! =====\n")

    print("Escolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Médio")
    print("3 - Difícil")

    while True:
        nivel = input("Escolha (1/2/3): ")

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
            print("Opção inválida. Tente novamente.")

    print("\n🔎 Buscando perguntas...")
    perguntas = fetch_trivia(dificuldade)

    if not perguntas:
        print("Erro ao carregar perguntas. Tente novamente mais tarde.")
        return

    pontuacao = 0
    total = len(perguntas)

    for idx, item in enumerate(perguntas, start=1):

        dados = montar_pergunta(item)

        print("\n-----------------------------")
        print(f"Pergunta {idx}/{total}")
        print("🛈", traduzir(dados['pergunta']))
        print("-----------------------------\n")

        for i, opcao in enumerate(dados['opcoes'], start=1):
            print(f"{i} - {traduzir(opcao)}")

        acertou = verificar_resposta(
            [traduzir(op) for op in dados['opcoes']],
            traduzir(dados['correta'])
        )

        if acertou:
            pontuacao += 1

    print("\n===== 🏁 RESULTADO FINAL =====")
    print(f"Você acertou {pontuacao} de {total} perguntas!")

    if pontuacao == total:
        print("🔥 Perfeito! Um gênio!")
    elif pontuacao >= total / 2:
        print("😄 Muito bem!")
    else:
        print("🙂 Continue praticando!")


# ---------------------------
# EXECUTAR O JOGO
# ---------------------------
if __name__ == "__main__":
    jogar_trivia()
