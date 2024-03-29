import pypandoc
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
from html2text import html2text as htt
import wikitextparser as wtp

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import argparse

pattern = r'\[\[:?(?:ファイル|画像|File|Image|图像):(.*?)(?:\||\]\])'


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

    parser.add_argument(
        "--lang",
        "-l",
        help="which language: ja/en/zh",
    )

    args = parser.parse_args()
    return args

def wiki2md(content):
    try:
        return pypandoc.convert_text(content, format='mediawiki', to='gfm')
    except:
        return content
    
def wiki2html(content):
    try:
        return pypandoc.convert_text(content, format='mediawiki', to='html')
    except:
        return content

def dewiki(text):
    text = wtp.parse(text).plain_text()  # wiki to plaintext 
    text = htt(text)  # remove any HTML
    text = text.replace('\\n',' ')  # replace newlines
    text = re.sub('\s+', ' ', text)  # replace excess whitespace
    text = re.sub(r'^[^\[\]]*?\]\]', '', text)
    return text

def remove_subset(string):
    cleaned_string = re.sub(r'thumb\|.*?\]\]', '', string)
    return cleaned_string

def wiki2itl(input_file):
    # init dataframe
    data = {
        'texts': [],
        # 'markdown': [],
        # 'html': [],
        'images': []
    }
    df = pd.DataFrame(data)
    # Parse the XML file
    print('start reading file')
    tree = ET.parse(input_file)
    root = tree.getroot()
    print('Loop on each page now!')
    for page in tqdm(root.iter('{http://www.mediawiki.org/xml/export-0.10/}page')):
        # Get the page title and content
        title = page.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
        content = page.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text').text
        # find image_file_names and the desired pattern
        try:
            image_file_names = list(re.findall(pattern, content))
            # splite content along img_name
            splite_content = list(re.split(pattern, content))
            images = [] 
            texts = []
            idx = 0
            img_idx = 0
            for item in splite_content:
                if item in image_file_names:
                    meta = dict({
                        'image_index':img_idx,
                        'index':idx,
                        'url':item
                    })
                    images.append(meta)
                    img_idx += 1
                else:
                    item = dewiki(item)
                    if len(item) < 5:
                        continue
                    texts.append(item)
                    idx += 1
            # add row to df
            new_row = {'texts':texts , 
                    'images': images}
            df = df.append(new_row, ignore_index=True)
        except Exception as e:
            print(f"Get some error: {str(e)}, process continue")
            continue
    return df

def main():
    args = get_parser()
    out_file_name = os.path.basename(args.input).replace('.xml', '.parquet')
    out_file = os.path.join(args.outdir,out_file_name)
    if args.lang in ['ja','en']:
        pass
    else:
        raise ValueError(f'{args.lang} is not supported')
    df = wiki2itl(input_file=args.input)
    try:
        df.to_parquet(out_file, engine="pyarrow") 
    except Exception as e:
        print(f'{e} occurs when saving parquet, trying to save into json now')
        df.to_json(out_file.replace('.parquet','.json'))

if __name__ == '__main__':
    main()
