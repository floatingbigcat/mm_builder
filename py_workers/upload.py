from huggingface_hub import HfApi
import glob
import asyncio
import os

folder = r'/home/lfsm/code/mm_builder/dataset/wiki/en/interleaved_url'

api = HfApi()
for root, dirs, files in os.walk(folder):
    for file in files:
        par_path = os.path.join(root,file)
        while True:
            try:
                api.upload_file(
                path_or_fileobj=par_path,
                path_in_repo=file,
                repo_id="lfsm/multimodal_wiki",
                repo_type="dataset",
                token="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",
                create_pr=False,
                )
                print(f'{par_path} successfully upload!')
                break
                # os.remove(str(n)+".parquet")
            except Exception as e:
                continue
