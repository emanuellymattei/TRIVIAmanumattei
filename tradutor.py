import html
import requests

def traduzir(text):
    """
    Traduz um texto para PT-BR utilizando a API pública do Google.
    """
    url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=pt-BR&q={html.unescape(text)}"
    traducao = requests.get(url)

    if traducao.status_code == 200:
        try:
            traducao = traducao.json()
            return traducao[0][0]
        except:
            return html.unescape(text)
    else:
        print(f"Erro ao traduzir. Código HTTP: {traducao.status_code}")
        return html.unescape(text)
