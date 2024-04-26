#!/bin/bash

#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable  /home/hr546787/Code_Parser/test/0.sh 551156 NoBranch 0)
JOB_ID_1=$(sbatch --nodes=1 --ntasks=1 --parsable  /home/hr546787/Code_Parser/test/1.sh 551156 NoBranch 1)
JOB_ID_2=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 551156 0 0.2)
JOB_ID_3=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 551156 1 0.4)
JOB_ID_4=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 551156 2 0.7)
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/551156_trigger.log
