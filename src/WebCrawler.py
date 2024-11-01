 import requests
 from bs4 import BeautifulSoup

 # Scrape do site do gov pesquisando sobre noticias sobre vagas
 def scrape_es_government():
        url = 'https://www.es.gov.br/Noticias'
            base_url = 'https://www.es.gov.br'
                response = requests.get(url)
                    response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                            noticias = soup.select('div div div ul li article div div div div div div h4 a')
                                return [(noticia.get_text(), base_url + noticia['href']) for noticia in noticias if 'vagan noticia.get_text().lower() or 'cursos' in noticia.get_text().lower()]

                                # Scrape do site do qualificar
                                def scrape_qualificar_es():
                                        url = 'https://qualificar.es.gov.br/'
                                            base_url = 'https://qualificar.es.gov.br'
                                                response = requests.get(url)
                                                    response.raise_for_status()
                                                        soup = BeautifulSoup(response.text, 'html.parser')
                                                            noticias = soup.select('div div div ul li div div div div h4 a')
                                                                return [(noticia.get_text(), base_url + noticia['href']) for noticia in noticias if 'vagas' in noticia.get_text().lower() or 'cursos' in noticia.get_text().lower()]