#!/bin/bash
# Specify the folder path
dump_path="your_wiki_dump_path"
out_path="your_tmp_interleaved_wiki_path" 
# Iterate over each file in the folder
for file in "$dump_path"/*; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Display the file names
        echo "Processing $file..." &
        python py_workers/wiki2itl.py \
            --input $file \
            --outdir $out_path \
            --lang en &
    fi
done
wait
echo "Finish"



