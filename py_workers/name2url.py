import pandas as pd
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import re
import argparse

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
        return '' 
    
    #  Send a GET request to potiental URL
    bases = ['https://ja.wikipedia.org/wiki/ファイル:',
             'https://commons.wikimedia.org/wiki/File:']
    for base in bases:
        response = get_response_from_url(base+name)
        if response == None:
            continue
    if response == None:
        return ''
    
    # Get image_link from the valid url
    soup = BeautifulSoup(response.content, "html.parser")
    full_image_div = soup.find("div", class_="fullImageLink")
    image_link = full_image_div.find("a")
    try:
        image_url = image_link["href"]
        return image_url
    except:
        return ''

def mp_name2url(images):
    name = images['url']
    name = name.replace(" ", "_")
    url = name2url(name)
    images['url'] = url
    return images

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help="path to articles xml",
        default="enwiki-20230401-pages-articles-multistream.xml",
    )
    args = parser.parse_args()
    return args

def main():
    args = get_parser()
    input_file = args.input
    df = pd.read_parquet(input_file)
    for index, images in df['images'].items():
        if images is None:
            continue
        new_images = []
        pool = mp.Pool()
        new_images = pool.map(mp_name2url,images)
        #list2dict
        # Close the pool to free resources
        pool.close()
        pool.join() 
        # change the df   
        df.loc[index, 'images'] = [new_images]
    df.to_parquet(input_file)
       
       
if __name__ == '__main__':
    main()