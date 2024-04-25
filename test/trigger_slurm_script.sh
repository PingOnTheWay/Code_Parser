#!/bin/bash

#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable  /home/hr546787/Code_Parser/test/0.sh 608316 NoDependency 0)
JOB_ID_1=$(sbatch --nodes=1 --ntasks=1 --parsable  /home/hr546787/Code_Parser/test/1.sh 608316 NoDependency 1)
JOB_ID_2=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 608316 2 0.2)
JOB_ID_3=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 608316 2 0.4)
JOB_ID_4=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 /home/hr546787/Code_Parser/test/2.sh 608316 2 0.7)
sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/trigger_608316_log.log
