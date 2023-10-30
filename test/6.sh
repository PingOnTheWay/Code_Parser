#!/usr/local_rwth/bin/zsh
#SBATCH --mem-per-cpu=6G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1

export LD_LIBRARY_PATH="/usr/local_rwth/sw/python/3.8.7/x86_64/lib/:${LD_LIBRARY_PATH}"
srun /usr/local_rwth/sw/python/3.8.7/x86_64/bin/python3.8 /home/hr546787/Code_Parser/test/6.py