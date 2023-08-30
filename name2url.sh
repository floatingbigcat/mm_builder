#!/bin/bash
# Specify the folder path
interleaved_path="outpath_of_last_step"
out_path="new_folder_path" 
# Iterate over each file in the folder
for file in "$interleaved_path"/*; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Display the file names
        echo "Processing $file..." & 
        python py_workers/name2url.py \
            --input $file \
            --outdir $out_path &
    fi
done
wait
echo "Done!"



