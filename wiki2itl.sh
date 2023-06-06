#!/bin/bash
#YBATCH -r epyc-7543_4
#SBATCH -N 1
#SBATCH -o .out/wiki%j.out
#SBATCH --time=72:00:00
#SBATCH -J ja-wiki2itl 
#SBATCH --error .out/wiki%j.err

source activate
conda activate /home/lfsm/anaconda3/envs/nlp

# Specify the folder path
folder_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/dump"
out_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/interleaved" 
# jawiki-20230501-pages-articles-multistream2.xml-p114795p390428
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
wait
echo "Finish"



