#!/bin/bash -xe

module load tacc-singularity

MEGAHIT_CMD_LINE_ARGS=`singularity exec imicrobe-megahit.img python3 /scripts/agave_to_megahit_cmd_line_args.py $@`

echo "megahit command line args: \"${MEGAHIT_CMD_LINE_ARGS}\""

singularity run imicrobe-megahit.img ${MEGAHIT_CMD_LINE_ARGS}
