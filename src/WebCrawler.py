import requests
from bs4 import BeautifulSoup

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


genai.configure(api_key='AIzaSyDUnXqUIVReCj1do3tAKqAQ3P-PPRSTcLU')
model = genai.GenerativeModel("gemini-1.5-flash")

# Scrape do site do gov pesquisando sobre noticias sobre vagas
def scrape_es_government():
    url = 'https://www.es.gov.br/Noticias'
    base_url = 'https://www.es.gov.br'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = soup.select('div div div ul li article div div div div div div h4 a')
    return [(noticia.get_text(), base_url + noticia['href']) for noticia in noticias if 'vagas' in noticia.get_text().lower() or 'cursos' in noticia.get_text().lower()]

# Scrape do site do qualificar
def scrape_qualificar_es():
    url = 'https://qualificar.es.gov.br/'
    base_url = 'https://qualificar.es.gov.br'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = soup.select('div div div ul li div div div div h4 a')
    return [(noticia.get_text(), base_url + noticia['href']) for noticia in noticias if 'vagas' in noticia.get_text().lower() or 'cursos' in noticia.get_text().lower()]


def main():
    es_government_news = scrape_es_government()
    qualificar_es_news = scrape_qualificar_es()

    all_news = es_government_news + qualificar_es_news

    with open("noticia_resumo.txt", "w", encoding="utf-8") as file:
        for titulo, link in all_news:
            print(titulo)
            print(link)

            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Seleciona a div com a classe "clearfix body-part"
            noticias = soup.select('div.clearfix.body-part')
            noticiaTratada = ""

            # Concatena o texto da notícia
            for noticia in noticias:
                noticiaTratada += noticia.get_text(strip=True) + "\n\n"

            # Gera o resumo (substitua o código abaixo pelo seu gerador de resumos)
            context = noticiaTratada
            response = model.generate_content(f"Faça um resumo de: {context}")
            resumo = response.text
            print(resumo)
            print('-' * 80)

            # Salva o conteúdo e o resumo no arquivo texto
            file.write("Título: " + titulo + "\n")
            file.write("Link: " + link + "\n")
            file.write("Notícia Completa:\n" + noticiaTratada + "\n")
            file.write("Resumo:\n" + resumo + "\n")
            file.write("-" * 80 + "\n\n")

    print("Arquivo 'noticia_resumo.txt' salvo com sucesso!")

if __name__ == "__main__":
    main()
