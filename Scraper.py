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
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)
