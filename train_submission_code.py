import json
import select
import time
import logging
import os

import numpy as np
import aicrowd_helper
import gym
import minerl
from utility.parser import Parser

import coloredlogs
coloredlogs.install(logging.DEBUG)

# --- NOTE ---
# This code is only used for "Research" track submissions
# ------------

# All research-tracks evaluations will be ran on the MineRLObtainDiamondVectorObf-v0 environment
MINERL_GYM_ENV = os.getenv('MINERL_GYM_ENV', 'MineRLObtainDiamondVectorObf-v0')
# You need to ensure that your submission is trained in under MINERL_TRAINING_MAX_STEPS steps
MINERL_TRAINING_MAX_STEPS = int(os.getenv('MINERL_TRAINING_MAX_STEPS', 8000000))
# You need to ensure that your submission is trained by launching less than MINERL_TRAINING_MAX_INSTANCES instances
MINERL_TRAINING_MAX_INSTANCES = int(os.getenv('MINERL_TRAINING_MAX_INSTANCES', 5))
# You need to ensure that your submission is trained within allowed training time.
# Round 1: Training timeout is 5 minutes
# Round 2: Training timeout is 4 days
MINERL_TRAINING_TIMEOUT = int(os.getenv('MINERL_TRAINING_TIMEOUT_MINUTES', 4 * 24 * 60))
# The dataset is available in data/ directory from repository root.
MINERL_DATA_ROOT = os.getenv('MINERL_DATA_ROOT', 'data/')

# Optional: You can view best effort status of your instances with the help of parser.py
# This will give you current state like number of steps completed, instances launched and so on. Make your you keep a tap on the numbers to avoid breaching any limits.
parser = Parser(
    'performance/',
    allowed_environment=MINERL_GYM_ENV,
    maximum_instances=MINERL_TRAINING_MAX_INSTANCES,
    maximum_steps=MINERL_TRAINING_MAX_STEPS,
    raise_on_error=False,
    no_entry_poll_timeout=600,
    submission_timeout=MINERL_TRAINING_TIMEOUT * 60,
    initial_poll_timeout=600
)


def main():
    """
    This function will be called for training phase.
    """
    # How to sample minerl data is document here:
    # http://minerl.io/docs/tutorials/data_sampling.html
    data = minerl.data.make(MINERL_GYM_ENV, data_dir=MINERL_DATA_ROOT)

    # Sample code for illustration, add your training code below
    env = gym.make(MINERL_GYM_ENV)

    # For an example, lets just run one episode of MineRL for training
    obs = env.reset()
    done = False
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
        # Do your training here

        # To get better view in your training phase, it is suggested
        # to register progress continuously, example when 54% completed
        # aicrowd_helper.register_progress(0.54)

        # To fetch latest information from instance manager, you can run below when you want to know the state
        #>> parser.update_information()
        #>> print(parser.payload)
        # .payload: provide AIcrowd generated json
        # Example: {'state': 'RUNNING', 'score': {'score': 0.0, 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 2001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamond-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 2001, 'environment': 'MineRLObtainDiamond-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': 0.0, 'score_secondary': 0.0}}}}
        # .current_state: provide indepth state information avaiable as dictionary (key: instance id)

    # Save trained model to train/ directory
    # For a demonstration, we save some dummy data.
    # NOTE: During Round 1 submission you upload trained agents as part of the git repository.
    #       The training code is only ran for 5 minutes (i.e. no proper training), so you might
    #       want to avoid overwriting any existing files here!
    #       Remember to enable it for Round 2 submission, though!
    np.save("./train/parameters.npy", np.random.random((10,)))

    # Training 100% Completed
    aicrowd_helper.register_progress(1)
    env.close()


if __name__ == "__main__":
    main()
