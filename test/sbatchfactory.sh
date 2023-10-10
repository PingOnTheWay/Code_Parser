#!/bin/bash

#SBATCH --nodes=21
#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable 0.sh)
JOB_ID_1=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 1.sh 0.2)
JOB_ID_2=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1 2.sh)
JOB_ID_3=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 4.sh)
JOB_ID_4=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1 3.sh)
JOB_ID_5=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 1.sh 0.4)
JOB_ID_6=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_5 2.sh)
JOB_ID_7=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_5,$JOB_ID_6 4.sh)
JOB_ID_8=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_5 3.sh)
JOB_ID_9=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 1.sh 0.7)
JOB_ID_10=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_9 2.sh)
JOB_ID_11=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_9,$JOB_ID_10 4.sh)
JOB_ID_12=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_9 3.sh)
JOB_ID_13=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 6.sh)
JOB_ID_14=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_13 8.sh)
JOB_ID_15=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_13,$JOB_ID_14 5.sh)
JOB_ID_17=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_13 9.sh 1)
JOB_ID_18=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_13 9.sh 2)
JOB_ID_19=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_13 9.sh 3)
JOB_ID_20=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 7.sh)
