#!/bin/bash
set -e
./utility/verify_or_download_data.sh
export EVALUATION_STAGE='training'
python3 run.py
