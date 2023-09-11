# mm_builder
This repo is used to create a multimodal wikipedia from wiki dump file.  
Now support the japanese and english.   
There are still many imporvement can be made for good quality

processed en interleaved wiki is here https://huggingface.co/datasets/lfsm/multimodal_wiki/tree/main

## Data Format
The interleaved wiki contain serveral parquet files, each file contain two columns,texts and images.
each row represent one article.
Take one row as a example:

texts column:  
array(['Ruined church and graveyard in Kilmacar]] Kilmocar or Kilmacar () is a townland and civil parish in County Kilkenny, Ireland. The ruins of a medieval church lie within Kilmacar townland. ==References== Category:Civil parishes of County Kilkenny '],
      dtype=object)

images column:  
array([{'image_index': 0, 'index': 0, 'url': 'https://upload.wikimedia.org/wikipedia/commons/3/38/Church_as_graveyard_Kilmacar_%28geograph_4996021%29.jpg'}],
      dtype=object)

For tests column, 
text of the article is **splited into a lists** by images, len is 1 in this case,  

regarding images column, 
- **image_index** means its order in images under the article.
- **index** means where should it be inserted in the text lists, the image should be put next to the first item of the text lists in this case
- **url** is the actual image address, you can use wget to download the image directly.

## How to use

### Download and uncompress the dump file
you can download the dump file from the wiki website, or

```
cd your_dump_dir
wget -i ./data/en_urls.txt
```
modify path in unzip.sh and run
```
bash unzip.sh
```

### Convert dump file into interleaved format
The wiki dump file don't contain image url address, in this step, we will extract all the image name from each article of dump files into "images" columns and spilte text of each article by images.
modify paths in en_wiki2itl.sh and run
```
bash en_wiki2itl.sh
```
### Replace the image name into real image url
In this step, we try to get the real image url by the image name.
modify paths in name2url.sh and run
```
bash name2url.sh
```

### Further clean the texts
this will further clean the texts
modify paths in clean.sh and run
```
bash clean.sh
```

