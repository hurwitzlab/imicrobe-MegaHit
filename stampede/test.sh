#!/bin/bash

#SBATCH -A iPlant-Collabs
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 00:30:00
#SBATCH -p development
#SBATCH -J test-imicrobe-megahit
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user jklynch@email.arizona.edu

module load irods

INPUT_DIR="$SCRATCH/imicrobe-megahit/test/input"
if [[ -d $INPUT_DIR ]]; then
  rm -rf $INPUT_DIR
fi

mkdir -p $INPUT_DIR
iget /iplant/home/shared/imicrobe/projects/264/samples/5279/E_coli_S_flexneri_0.001.fa $INPUT_DIR

INPUT_FILE=${INPUT_DIR}/E_coli_S_flexneri_0.001.fa

OUTPUT_DIR="$SCRATCH/imicrobe-megahit/test/output"
if [[ -d $OUTPUT_DIR ]]; then
  rm -rf $OUTPUT_DIR
fi

mkdir -p $OUTPUT_DIR

./run.sh -r $INPUT_FILE -o $OUTPUT_DIR
