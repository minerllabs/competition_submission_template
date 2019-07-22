# Simple env test.
import json
import select
import time
import logging
import os

import aicrowd_helper
import gym
import minerl

import coloredlogs
coloredlogs.install(logging.DEBUG)

# All the evaluations will be evaluated on MineRLObtainDiamond-v0 environment
MINERL_GYM_ENV = os.getenv('MINERL_GYM_ENV', 'MineRLObtainDiamond-v0')
# You need to ensure that your submission is trained in under MINERL_MAX_SAMPLES samples
MINERL_TRAINING_MAX_SAMPLES = int(os.getenv('MINERL_TRAINING_MAX_SAMPLES', 10))
# You need to ensure that your submission is trained within allowed training time.
# Round 1: Training timeout is 5 minutes
# Round 2: Training timeout is 4 days
MINERL_TRAINING_TIMEOUT = int(os.getenv('MINERL_TRAINING_TIMEOUT_MINUTES', 5))
# The dataset is available in data/ directory from repository root.
MINERL_DATA_ROOT = os.getenv('MINERL_DATA_ROOT', 'data/')

def main():
    """
    This function will be called for training phase.
    """
    # How to sample minerl data is document here:
    # http://minerl.io/docs/tutorials/data_sampling.html
    data = minerl.data.make(MINERL_GYM_ENV, data_dir=MINERL_DATA_ROOT)

    # Sample code for illustration, add your training code below
    env = gym.make(MINERL_GYM_ENV)

    actions = [env.action_space.sample() for _ in range(MINERL_TRAINING_MAX_SAMPLES)]
    xposes = []
    for _ in range(1):
        obs, info = env.reset()
        done = False
        netr = 0

        while not done:
            random_act = env.action_space.noop()
            random_act['camera'] = [0, 0.2]
            random_act['back'] = 0
            random_act['forward'] = 1
            random_act['jump'] = 1
            random_act['attack'] = 1
            obs, reward, done, info = env.step(random_act)
            netr += reward
            env.render()
            # To get better view in your training phase, it is suggested
            # to register progress continuously, example when 54% completed
            # aicrowd_helper.register_progress(0.54)

    # Save trained model to train/ directory
    # Training 100% Completed
    aicrowd_helper.register_progress(1)
    env.close()


if __name__ == "__main__":
    main()
