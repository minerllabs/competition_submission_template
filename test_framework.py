import json
import logging
import os
import threading

import aicrowd_helper
import gym
import minerl

from test_submission_code import MineRLAgent, Episode, EpisodeDone

import coloredlogs
coloredlogs.install(logging.DEBUG)


# Read aicrowd.json for the tag on which env to use for the evaluation
aicrowd_json = None
with open("aicrowd.json") as f:
    aicrowd_json = json.load(f)
assert aicrowd_json["tags"] in ["research", "intro"], "aicrowd.json 'tag' needs to be one of ['research', 'intro']"
is_research_track = aicrowd_json["tags"] == "research"

# All the evaluations will be evaluated on MineRLObtainDiamondVectorObf-v0 or MineRLObtainDiamond-v0 environment
MINERL_GYM_ENV = "MineRLObtainDiamondVectorObf-v0" if is_research_track else "MineRLObtainDiamond-v0"
MINERL_MAX_EVALUATION_EPISODES = int(os.getenv('MINERL_MAX_EVALUATION_EPISODES', 5))

# Parallel testing/inference, **you can override** below value based on compute
# requirements, etc to save OOM in this phase.
EVALUATION_THREAD_COUNT = int(os.getenv('EPISODES_EVALUATION_THREAD_COUNT', 2))

####################
# EVALUATION CODE  #
####################

def main():
    agent = MineRLAgent()
    agent.load_agent()

    assert MINERL_MAX_EVALUATION_EPISODES > 0
    assert EVALUATION_THREAD_COUNT > 0

    # First call to reset will build/create the environment,
    # but since MineRL v0.4 this works on Linux
    envs = []
    for _ in range(EVALUATION_THREAD_COUNT):
        env = gym.make(MINERL_GYM_ENV)
        envs.append(env)

    episodes_per_thread = [MINERL_MAX_EVALUATION_EPISODES // EVALUATION_THREAD_COUNT for _ in range(EVALUATION_THREAD_COUNT)]
    episodes_per_thread[-1] += MINERL_MAX_EVALUATION_EPISODES - EVALUATION_THREAD_COUNT *(MINERL_MAX_EVALUATION_EPISODES // EVALUATION_THREAD_COUNT)

    # A simple function to evaluate on episodes!
    def evaluate(i, env):
        print("[{}] Starting evaluator.".format(i))
        for i in range(episodes_per_thread[i]):
            try:
                agent.run_agent_on_episode(Episode(env))
            except EpisodeDone:
                print("[{}] Episode complete".format(i))
                pass

    evaluator_threads = [threading.Thread(target=evaluate, args=(i, envs[i])) for i in range(EVALUATION_THREAD_COUNT)]
    for thread in evaluator_threads:
        thread.start()

    # wait fo the evaluation to finish
    for thread in evaluator_threads:
        thread.join()


if __name__ == "__main__":
    main()
