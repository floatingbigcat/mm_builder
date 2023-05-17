#!/bin/bash
#YBATCH -r epyc-7543_2
#SBATCH -N 1
#SBATCH -o .out/wiki.out
#SBATCH --time=6:00:00
#SBATCH -J wiki2itl 
#SBATCH --error .out/wiki%j.err

echo "Begin works!"
bash run.sh
echo "Done!"
