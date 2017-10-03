#!/bin/bash -xe

INPUT_FILE=$1
OUTPUT_DIR=$2

module load singularity

#export LAUNCHER_DIR="$HOME/src/launcher"
#export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins
#export LAUNCHER_WORKDIR=$OUTPUT_DIR
#export LAUNCHER_RMI=SLURM

#export LAUNCHER_JOB_FILE=`pwd`/launcher_jobfile
#echo ${LAUNCHER_JOB_FILE}

singularity run imicrobe-MegaHit.img

#$LAUNCHER_DIR/paramrun
#echo "Ended launcher"
