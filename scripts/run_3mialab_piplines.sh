#!/bin/bash

# SLURM Settings
#SBATCH --job-name="run_3mialab_piplines"
#SBATCH --time=24:00:00
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=128G
#SBATCH --partition=epyc2
#SBATCH --qos=job_epyc2
#SBATCH --mail-user=aaron.colombo@students.unibe.ch
#SBATCH --mail-type=ALL
#SBATCH --chdir=../bin
#SBATCH --output=../scripts/%x_%j.out
#SBATCH --error=../scripts/%x_%j.err

# Load Anaconda3
module load Anaconda3
eval "$(conda shell.bash hook)"

# Load your environment
conda activate mialab

# Label separation
srun python3 label_separation.py --multirun pipeline=pipeline_big,pipeline_small

# Pipelines
srun python3 main.py --multirun pipeline=pipeline_all,pipline_big,pipeline_small

# Comparison
srun pyhton3 comparison_segmentations.py