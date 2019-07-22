#!/bin/bash

if [ -d data/MineRLObtainDiamond-v0 ]
then
    exit 0
else
    echo "Downloaded data not found, we will be downloading data for you. This will be one time process."
    echo "If you don't want data to be download, please do `mkdir data/MineRLObtainDiamond-v0` at repository root, or place data manually."
    python3 -c 'import minerl; minerl.data.download("data/")'
fi
