#!/bin/bash

# Specify the folder path
folder_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/dump"
out_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/interleaved" 
cd /home/lfsm/code/mm_builder
# Iterate over each file in the folder
for file in "$folder_path"/*; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Display the file names
        echo "Processing $file..." &
        python py_workers/wiki2itl.py \
            --input $file \
            --outdir $out_path \
            --lang ja &
    fi
done

