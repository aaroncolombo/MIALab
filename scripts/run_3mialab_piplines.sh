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
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Load Anaconda3
module load Anaconda3
eval "$(conda shell.bash hook)"

# Load your environment
conda activate mialab

# Run your code
srun --task=1 --cpus-per-task=1 python3 main.py &
srun --task=1 --cpus-per-task=1 python3 main.py &
srun --task=1 --cpus-per-task=1 python3 main.py &
wait