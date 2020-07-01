# Simple env test.
import json
import select
import time
import logging
import os
import threading

import aicrowd_helper
import gym
import minerl

import coloredlogs
coloredlogs.install(logging.DEBUG)

# All the evaluations will be evaluated on MineRLObtainDiamond-v0 environment
MINERL_GYM_ENV = os.getenv('MINERL_GYM_ENV', 'MineRLObtainDiamondVectorObf-v0')
MINERL_MAX_EVALUATION_EPISODES = int(os.getenv('MINERL_MAX_EVALUATION_EPISODES', 5))

# Parallel testing/inference, **you can override** below value based on compute
# requirements, etc to save OOM in this phase.
EVALUATION_THREAD_COUNT = os.getenv('EPISODES_EVALUATION_THREAD_COUNT', 4)
EVALUATION_EPISODES_PROCESSED = 0
EVALUATION_EPISODES_PROCESSED_LOCK = threading.Lock()


class MineRLInference:
    """
    Random agent inference, implement this class for testing/inference phase.
    """

    def __init__(self):
        # Sample code for illustration, add your code below to run in test phase.
        # Load trained model from train/ directory, any preprocessing required, etc.
        pass


    def inference(self):
        # Implement per-episodee inference code
        obs = self.env.reset()
        done = False
        while not done:
            random_act = self.env.action_space.noop()
            random_act['camera'] = [0, 0.3]
            random_act['back'] = 0
            random_act['forward'] = 1
            random_act['jump'] = 1
            random_act['attack'] = 1
            obs, reward, done, info = self.env.step(random_act)


    def run(self):
        global EVALUATION_THREAD_COUNT
        threads = [threading.Thread(target=self.evaluation_thread) for _ in range(EVALUATION_THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def evaluation_thread(self):
        global EVALUATION_EPISODES_PROCESSED_LOCK, EVALUATION_EPISODES_PROCESSED, MINERL_MAX_EVALUATION_EPISODES
        self.env = gym.make(MINERL_GYM_ENV)
        while True:
            run_next_episode = False

            EVALUATION_EPISODES_PROCESSED_LOCK.acquire()
            if EVALUATION_EPISODES_PROCESSED < MINERL_MAX_EVALUATION_EPISODES:
                run_next_episode = True
                EVALUATION_EPISODES_PROCESSED += 1
            EVALUATION_EPISODES_PROCESSED_LOCK.release()

            if run_next_episode:
                self.inference()
            else:
                break
        self.env.close()


def main():
    minerl_inference_obj = MineRLInference()
    minerl_inference_obj.run()


if __name__ == "__main__":
    main()
