
import pypandoc
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

add_md = False
add_html = False
# Set the input file path
input_file= '/home/lfsm/datasets/wiki_ja/jawiki-20230401-pages-articles-multistream1.xml-p1p114794'
# init dataframe
data = {
    'xml': [],
    'markdown': [],
    'html': [],
    'pairs': []
}
df = pd.DataFrame(data)

# Parse the XML file
print('start reading file')
tree = ET.parse(input_file)
print('finish read file!')
root = tree.getroot()

i=0
# Loop over each page in the XML file
for page in tqdm(root.iter('{http://www.mediawiki.org/xml/export-0.10/}page')):
    
    # i+=1
    # if i > 1000:
    #     df.to_parquet('test.parquet')
    #     break
    
    # Get the page title and content
    title = page.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
    content = page.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text').text
    
    # find image_file_names and the desired pattern
    patterns = [r'\[\[:(?:ファイル|画像):(.*?)\|',r'\[\[(?:ファイル|画像):(.*?)\|'] 
    for pattern in patterns:
        image_file_names = list(set(re.findall(pattern, content))) 
        if len(image_file_names) != 0:
            break
    
    # splite content along img_name, and remove r
    splite_content = list(set(re.split(pattern, content)))

    # replace img_name with label ###img#i### and record
    pairs = []
    idx = 0
    for i in range(len(splite_content)):
        if splite_content[i] in image_file_names:
            label = f'###img#{idx}###' 
            pairs.append([label, splite_content[i]])
            splite_content[i] = label
            idx += 1 
    
    md_content = []
    if add_md:
        # get markdown format
        def wiki2md(content):
            try:
                return pypandoc.convert_text(content, format='mediawiki', to='gfm')
            except:
                return content
        for item in splite_content:
            if not item.startswith('###img#'): 
                item = wiki2md(item) 
            md_content.append(item)
    html_content = []
    if add_html:    
        # get html format
        def wiki2html(content):
            try:
                return pypandoc.convert_text(content, format='mediawiki', to='html')
            except:
                return content
        for item in splite_content:
            if not item.startswith('###img#'): 
                item = wiki2html(item) 
            html_content.append(item)

    # add row to df
    # import pdb;pdb.set_trace()
    new_row = {'xml':splite_content , 'markdown': md_content, 'html': html_content, 'pairs': pairs}
    # new_row_df = pd.DataFrame(new_row, index=[0])
    # new_row_df = pd.Series(new_row)
    df = df.append(new_row, ignore_index=True)
    # df = pd.concat([df, new_row_df],axis=0,ignore_index=True)
    
df.to_parquet('../data/wiki_itl.parquet')

