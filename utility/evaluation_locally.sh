#!/bin/bash
set -e


AICROWD_DATA_ENABLED="YES"
if [[ " $@ " =~ " --no-data " ]]; then
   AICROWD_DATA_ENABLED="NO"
else
    python3 ./utility/verify_or_download_data.py
fi


EXTRAOUTPUT=" > /dev/null 2>&1 "
if [[ " $@ " =~ " --verbose " ]]; then
   EXTRAOUTPUT=""
fi

# Fixes for the new MineRL code
export PYRO_SERIALIZERS_ACCEPTED='pickle'
export PYRO_SERIALIZER='pickle'

# Run local name server
eval "pyro4-ns $EXTRAOUTPUT &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# Run instance manager to generate performance report
export EVALUATION_STAGE='manager'
eval "python3 run.py --seeds 1 $EXTRAOUTPUT &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# Run the evaluation
sleep 2
export MINERL_INSTANCE_MANAGER_REMOTE="1"
export EVALUATION_STAGE='testing'
export EVALUATION_RUNNING_ON='local'
export EXITED_SIGNAL_PATH='shared/exited'
rm -f $EXITED_SIGNAL_PATH
export ENABLE_AICROWD_JSON_OUTPUT='False'
eval "python3 run.py $EXTRAOUTPUT && touch $EXITED_SIGNAL_PATH || touch $EXITED_SIGNAL_PATH &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# View the evaluation state
export ENABLE_AICROWD_JSON_OUTPUT='True'
python3 utility/parser.py || true
kill $(jobs -p)
