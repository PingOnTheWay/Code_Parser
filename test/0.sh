#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=0
#SBATCH --output=/dev/null

srun /rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/0.py $1 $2 $3
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > ${SLURM_JOB_ID}_${job_index}_log.log
