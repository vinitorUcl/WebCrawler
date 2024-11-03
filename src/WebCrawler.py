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


from google.colab import userdata
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

    for titulo, link in all_news:
        print(titulo)
        print(link)

        url =link

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        noticias = soup.select('div.clearfix.body-part')
        noticiaTratada=""
        for noticia in noticias:
          noticiaTratada=noticiaTratada+(noticia.get_text(strip=True))


        context=noticiaTratada
        response = model.generate_content(f"Faça um resumo de: {context}")
        print(response.text)
        print('-' * 80)


if __name__ == "__main__":
    main()