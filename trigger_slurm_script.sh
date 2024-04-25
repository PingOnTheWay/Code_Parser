#!/bin/bash

#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 0.sh 515105 NoDependency 0)
JOB_ID_1=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 1.sh 515105 NoDependency 1)
JOB_ID_2=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 2.sh 515105 2 0.2)
JOB_ID_3=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 2.sh 515105 2 0.4)
JOB_ID_4=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 2.sh 515105 2 0.7)