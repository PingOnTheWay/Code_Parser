#!/bin/bash

#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable  /home/hr546787/Code_Parser/test/0.sh 645910 NoDependency 0)
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/trigger_645910_log.log
