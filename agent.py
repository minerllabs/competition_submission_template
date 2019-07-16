# Simple env test.
import json
import select
import time
import logging
import os

import gym
import matplotlib.pyplot as plt
import minerl
import numpy as np
from minerl.env.core import MineRLEnv

import coloredlogs
coloredlogs.install(logging.DEBUG)


#import minerl.env.bootstrap
#minerl.env.bootstrap._check_port_avail = lambda _,__: True

NUM_EPISODES = int(os.getenv('MINERL_NUM_EPISODES', 1))
MINERL_GYM_ENV = os.getenv('MINERL_GYM_ENV', 'MineRLObtainDiamond-v0')

def main():
    """
    Tests running a simple environment.
    """
    env = gym.make(MINERL_GYM_ENV)

    actions = [env.action_space.sample() for _ in range(2000)]
    xposes = []
    for _ in range(NUM_EPISODES):
        obs, info = env.reset()
        done = False
        netr = 0
        while not done:
            random_act = env.action_space.sample()
            
            random_act['camera'] = [0,0]
            random_act['back'] = 0
            random_act['forward'] = 1
            random_act['jump'] = 1
            random_act['attack'] = 1
            # print(random_act)
            obs, reward, done, info = env.step(
                random_act)
            netr += reward
            print(reward, netr)
            env.render()



    print("Demo complete.")

if __name__ == "__main__":
    main()
