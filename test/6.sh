#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=6
srun /rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/6.py $1 $2 $3
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test3/$1_${SLURM_JOB_NAME}$2.log
