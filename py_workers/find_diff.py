import os

a = '/home/lfsm/code/mm_builder/dataset/wiki/en/interleaved'
b = '/home/lfsm/code/mm_builder/dataset/wiki/en/interleaved_url'

afs = os.listdir(a)
bfs = os.listdir(b)

for ai in afs:
    if ai not in bfs:
        print(ai)

# fn = 'enwiki-20230501-pages-articles-multistream17.parquet-p23570393p23716197'
# fn_p = os.path.join(a,fn)
# import pandas as pd
# df = pd.read_parquet(fn_p)
# print(fn_p)
# print(df)

