#!/bin/bash

# SLURM Settings
#SBATCH --job-name="run_mialab_pipline"
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=128G
#SBATCH --partition=epyc2
#SBATCH --qos=job_epyc2
#SBATCH --mail-user=aaron.colombo@students.unibe.ch
#SBATCH --mail-type=ALL
#SBATCH --chdir=../bin
#SBATCH --output=../scripts/ubelix_files/%x_%j.out
#SBATCH --error=../scripts/ubelix_files/%x_%j.err

# Load Anaconda3
module load Anaconda3
eval "$(conda shell.bash hook)"

# Load your environment
conda activate mialab

# Run your code
srun python3 main.py pipeline=pipeline_big