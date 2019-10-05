import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

#inicio de variables
principal_url = 'http://books.toscrape.com'
contador_hoja = 1
contador_libro = 1
biblioteca = {}

#inicio metodos

def clean_url(url):
    #recibir parametros para poder procesarlo con soup
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

def get_sheets(url):
    #obtener todas las paginas para poder acceder a cada una de ellas mas tarde
    pages_urls = [url]
    soup = clean_url(pages_urls[0])
    while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
        new_url = soup.findAll("a", href=re.compile("page"))[-1].get("href")
        if new_url == 'catalogue/page-2.html':
            pages_urls.append(principal_url+'/'+new_url)
            soup = clean_url(principal_url+'/'+new_url)
        else:
            pages_urls.append(principal_url+'/catalogue/'+new_url)
            soup = clean_url(principal_url+'/catalogue/'+new_url)
    return pages_urls

def book_info(link_libro,):
    #recopilar toda la informacion solicitada de los libros
    libro = []
    prueba_elemento = clean_url(principal_url+"/"+link_libro)

    title = str(prueba_elemento.find("div", class_ = "col-sm-6 product_main").h1.text) #Title
    precio = str(prueba_elemento.find("p", class_ = "price_color").text) #Precio
    stock = str(re.sub("\D", "", prueba_elemento.find("p", class_ = "instock availability").text)) #Stock
    categoria = get_category(prueba_elemento) #categorias
    src = str(prueba_elemento.find("div", class_ = "item active").img.get('src')) #url_iamgen
    casi_src = src.split('./')
    nueva_src = principal_url+"/"+casi_src[2]
    table = prueba_elemento.find("table", attrs={"class":"table table-striped"})
    table = prueba_elemento.find('table', {'class': 'table-striped'})
    categoria = ' '.join(categoria.split())
    tds = table.findAll('td')

    libro.append(title)
    libro.append(precio[2:])
    libro.append(stock)
    libro.append(categoria)
    libro.append(nueva_src)
    libro.append(tds[0].text)
    libro.append(tds[1].text)
    libro.append(tds[2].text[2:])
    libro.append(tds[3].text[2:])
    libro.append(tds[4].text[2:])
    libro.append(tds[5].text[10:12])
    libro.append(tds[6].text)

    return libro

def get_category(url):
    #obtener el nombre de la categoria de un libro
    lista = url.find("ul", attrs={"class":"breadcrumb"})
    ul = lista.findAll('li')
    return ul[2].text
