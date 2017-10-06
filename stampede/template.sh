#!/bin/bash

# Usage:
#   run.sh -1 <forward read file> -2 <reverse read file>
#   run.sh -12 <interleaved paired end read file>
#   run.sh -r <single end read file>
#
# Required arguments:
#  -1 FORWARD_READS (input FASTA file)
#  -2 REVERSE_READS (input FASTA file)
# OR
#  -12 INTERLEAVED_READS (input FASTA file)
# OR
#  -r SINGLE_ENDED_READS (input FASTA file)
#
# Options (default in parentheses):
#

echo "FORWARD_READS        \"${FORWARD_READS}\""
echo "REVERSE_READS        \"${REVERSE_READS}\""
echo "INTERLEAVED_READS    \"${INTERLEAVED_READS}\""
echo "SINGLE_ENDED_READS   \"${SINGLE_ENDED_READS}\""
echo "ADDITIONAL_ARGS      \"${ADDITIONAL_ARGS}\""

echo "Started $(date)"

sh run.sh ${FORWARD_READS} ${REVERSE_READS} ${INTERLEAVED_READS} ${SINGLE_ENDED_READS} ${ADDITIONAL_ARGS}

echo "Ended $(date)"
exit 0
