#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --mail-user=lmjone@uoregon.edu     #optional: if you'd like email
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --cpus-per-task=1                #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB
#SBATCH --nodes=1                        #optional: number of nodes

conda activate base

./base_distribution.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz  -l 8 -o index_1