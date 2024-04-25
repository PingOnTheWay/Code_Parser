#!/bin/bash

#SBATCH --ntasks-per-node=1
JOB_ID_0=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 0.sh 836266 NoDependency 0)
JOB_ID_1=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 1.sh 836266 NoDependency 1)
JOB_ID_2=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 2.sh 836266 NoDependency 2)
JOB_ID_3=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 3.sh 836266 3 0)
JOB_ID_4=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 3.sh 836266 3 1)
JOB_ID_5=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 3.sh 836266 3 2)
JOB_ID_6=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 3.sh 836266 3 3)
JOB_ID_7=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0,$JOB_ID_1,$JOB_ID_2 3.sh 836266 3 4)
JOB_ID_9=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_1 4.sh 836266 NoDependency 4)
JOB_ID_10=$(sbatch --nodes=1 --ntasks=1 --parsable NoDependency 5.sh 836266 NoDependency 5)
JOB_ID_11=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 6.sh 836266 NoDependency 6)
JOB_ID_12=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:$JOB_ID_0 7.sh 836266 NoDependency 7)