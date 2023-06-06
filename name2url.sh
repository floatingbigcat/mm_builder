#!/bin/bash
#YBATCH -r epyc-7543_4
#SBATCH -N 1
#SBATCH -o .out/wiki%j.out
#SBATCH --time=72:00:00
#SBATCH -J name2url
#SBATCH --error .out/wiki%j.err
source activate
conda activate /home/lfsm/anaconda3/envs/nlp
# Specify the folder path
folder_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/interleaved"
out_path="/home/lfsm/code/mm_builder/dataset/wiki/ja/interleaved_url"
cd /home/lfsm/code/mm_builder
# Iterate over each file in the folder
for file in "$folder_path"/*; do
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



