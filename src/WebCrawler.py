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

    # Used to securely store your API key
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