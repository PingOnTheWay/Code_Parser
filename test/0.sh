#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=0
srun /rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/0.py $1 $2 $3
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/$1_${SLURM_JOB_NAME}$2.log
