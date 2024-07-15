#!/bin/bash

dir=$(dirname $0)

INPUT_FILE_PATH=$1
OUTPUT_FILE_PATH=$2

python3 $dir/scripts/anonymize/anonymize.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
python3 $dir/scripts/evaluate/utilityScore0_progressbar.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH

