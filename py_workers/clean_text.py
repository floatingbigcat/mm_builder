import pandas as pd
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import re
import argparse
import os
from tqdm import tqdm

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        help="path to articles xml",
        default="/home/lfsm/code/mm_builder/dataset/wiki/en/interleaved_url/enwiki-20230501-pages-articles-multistream9.parquet-p2936261p4045402",
    )
    parser.add_argument(
        "--outdir",
        "-o",
        help="dir path to the transformed file",
        default="/home/lfsm/code/mm_builder/dataset/wiki/en/cleaned",
    )
    args = parser.parse_args()
    return args

def clean_string(string):
    string = string.replace('* ','')
    string = string.replace(' *','')
    string = string.replace('thumb|','')
    string = string.replace('right|','')
    string = string.replace(']]','')
    string = re.sub(r'=+', '', string) # remove all title symbol
    string = re.sub(r'\{.*?\}', '', string) # remove all the chart   
    return string

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
    df = df[df['texts'].apply(lambda x: len(x) >= 1 and len(x[0]) >= 100 )]
    for index, texts in tqdm(df['texts'].items(),desc=f"Works in {input_file} now"):
        new_texts = []
        for text in texts:
            new_texts.append(clean_string(text))
        # change the df   
        df.loc[index, 'texts'] = new_texts
    print('start saving file now')
    print(f'saving {out_file}')
    df.to_parquet(out_file,index=False)
       
if __name__ == '__main__':
    main()