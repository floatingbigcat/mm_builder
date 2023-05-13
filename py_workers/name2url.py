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
    
def name2url(name):
    """Get url from pure file name"""
    if len(name) == 0:
        return name
    
    #  Send a GET request to potiental URL
    bases = ['https://ja.wikipedia.org/wiki/ファイル:',
             'https://commons.wikimedia.org/wiki/File:']
    for base in bases:
        response = get_response_from_url(base+name)
        if response == None:
            continue
    if response == None:
        return name
    
    # Get image_link from the valid url
    soup = BeautifulSoup(response.content, "html.parser")
    full_image_div = soup.find("div", class_="fullImageLink")
    image_link = full_image_div.find("a")
    image_url = image_link["href"]

    return image_url

def mp_name2url(pair):
    label,name = pair
    name = name.replace(" ", "_")
    url = name2url(name)
    return label,url

if __name__ == '__main__':
    # df = pd.read_parquet('../data/names.parquet')
    df = pd.read_parquet('../data/wiki_itl_0.parquet')

    i = 0
    # replace " " with "_"
    for index, pairs in df['pairs'].items():
        
        # i += 1
        # if i>20:
        #     break
        
        if pairs is None:
            continue
        
        # get new pairs with url in mp.pool
        new_pairs = []
        pool = mp.Pool()
        new_pairs = pool.map(mp_name2url,pairs)
        # Close the pool to free resources
        pool.close()
        pool.join() 
     
        # change the df   
        df.loc[index, 'pairs'] = [new_pairs]
       
 