#!/bin/bash -xe

module load singularity

singularity run imicrobe-MegaHit.img $@
