#!/usr/bin/python3

# Buscar en google un termino, obtener la pagina mas importante y devolver una lista de parrafos de maximo 500 palabras.
# Autor: Ashuin Sharma
# Universidad de Costa Rica

from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request

def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

if __name__ == '__main__':
    results = search("What is Google?", num_results=1, lang="en")
    for result in results:
        html_string = get_html(result)
        clean_text = ' '.join(BeautifulSoup(html_string, "html.parser").stripped_strings)
        print(clean_text)
        break
