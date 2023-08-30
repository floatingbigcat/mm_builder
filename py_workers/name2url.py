import pandas as pd
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import argparse
import os
from tqdm import tqdm

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help="path to articles xml",
        default="enwiki-20230401-pages-articles-multistream.xml",
    )
    parser.add_argument(
        "--outdir",
        "-o",
        help="dir path to the transformed file",
        default="/home/lfsm/code/mm_builder/dataset/wiki_en/interleaved",
    )
    args = parser.parse_args()
    return args

def get_response_from_url(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == requests.codes.ok:
            return response
        else:
            return None
    except requests.exceptions.RequestException:
        print(f"Can't reach {url} due to time out")
        return None
    
def name2url(name):
    """Get url from image name"""
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


def main():
    args = get_parser()
    input_file = args.input
    name = os.path.basename(input_file)
    if '.csv' in name:
        df = pd.read_csv(input_file)
        name = name.replace('.csv','.parquet')
    elif '.parquet' in name:
        df = pd.read_parquet(input_file)
    else:
        raise ValueError ('Check input_file format')
    out_file = os.path.join(args.outdir,name)
    
    for index, images in tqdm(df['images'].items(),desc=f"Works in {input_file} now"):
        try:
            if images.size == 0:
                continue
            new_images = []
            pool = mp.Pool()
            new_images = pool.map(mp_name2url,images)
            # Close the pool to free resources
            pool.close()
            pool.join() 
            # change the df   
            df.loc[index, 'images'] = new_images
        except Exception as e:
            print(f'get error {e} but continue')
            continue
    print('start saving file now')
    try:
        print(f'saving {out_file}')
        df.to_parquet(out_file)
    except Exception as e:
        print(f'get error {e} to save parquet file, try on csv now')
        df.to_csv(out_file.replace('parquet','csv'))
       
if __name__ == '__main__':
    main()