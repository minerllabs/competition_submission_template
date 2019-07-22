#!/bin/bash
# Run local name server
pyro4-ns &
NS_PID=$!

# Run instance manager to generate performance report
export EVALUATION_STAGE='manager'
python3 run.py --seed 1 & > /dev/null 2>&1
MANAGER_PID=$!

# Run the evaluation
sleep 2
export MINERL_INSTANCE_MANAGER_REMOTE="1"
export EVALUATION_STAGE='testing'
export EVALUATION_RUNNING_ON='local'
export EXITED_SIGNAL_PATH='shared/exited'
python3 run.py & > /dev/null 2>&1
SUBMISSION_PID=$!

# View the evaluation state
python3 utility/parser.py
kill $(jobs -p)
