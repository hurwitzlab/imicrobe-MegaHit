#!/bin/bash -xe

module load singularity

OUT_DIR="-o $PWD/megahit-out"

while getopts :o OPT; do
  case $OPT in
    o)
      OUT_DIR="$OPTARG"
      ;;
    :)
      echo "Error: Option -$OPTARG requires an argument."
      exit 1
      ;;
    # allow options like -r and -12 to pass through
    #\?)
    #  echo "Error: Invalid option: -${OPTARG:-""}"
    #  exit 1
  esac
done

echo "output directory   :   \"${OUT_DIR}\""
echo "all other arguments:   \"$@\""

singularity run imicrobe-megahit.img ${OUT_DIR} $@
