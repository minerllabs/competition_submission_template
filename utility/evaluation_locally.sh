#!/bin/bash
./utility/verify_or_download_data.sh

EXTRAOUTPUT=" > /dev/null 2>&1 "
if [[ " $@ " =~ " --verbose " ]]; then
   EXTRAOUTPUT=""
fi

# Run local name server
eval "pyro4-ns $EXTRAOUTPUT &"
trap "kill -11 $!" EXIT

# Run instance manager to generate performance report
export EVALUATION_STAGE='manager'
eval "python3 run.py --seed 1 $EXTRAOUTPUT &"
trap "kill -11 $!" EXIT

# Run the evaluation
sleep 2
export MINERL_INSTANCE_MANAGER_REMOTE="1"
export EVALUATION_STAGE='testing'
export EVALUATION_RUNNING_ON='local'
export EXITED_SIGNAL_PATH='shared/exited'
eval "python3 run.py $EXTRAOUTPUT &"
trap "kill -11 $!" EXIT

# View the evaluation state
python3 utility/parser.py || true
kill $(jobs -p)
