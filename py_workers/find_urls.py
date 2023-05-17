import pandas as pd
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp

def get_response_from_url(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == requests.codes.ok:
            return response
        else:
            return None
    except requests.exceptions.RequestException:
        return None

url = 'https://dumps.wikimedia.org/jawiki/20230501/'
response = get_response_from_url(url) 
soup = BeautifulSoup(response.content, "html.parser")
download_links = soup.find_all("a")
for link in download_links:
    if link['href'].startswith("/jawiki/20230501/jawiki-20230501-pages-articles-multistream"):
        if not link['href'].startswith("/jawiki/20230501/jawiki-20230501-pages-articles-multistream-index"): 
            print("https://dumps.wikimedia.org/"+link['href'])
