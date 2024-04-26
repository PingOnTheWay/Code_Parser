#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=7
srun /rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/7.py $1 $2 $3
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test3/${SLURM_JOB_ID}_$1_log.log
