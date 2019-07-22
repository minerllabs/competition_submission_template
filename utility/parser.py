#!/usr/bin/env python3
import json
import os
import signal
import sys
import subprocess
import time
import glob

import crowdai_api
import boto3
import uuid

# Where the output files will be located
PERFORMANCE_DIRECTORY = os.getenv('PERFORMANCE_DIRECTORY', 'performance/mc_1/')
# Time (in seconds) to wait before checking the file for lines again
POLL_INTERVAL=1
# How many seconds to let the submission run
SUBMISSION_TIMEOUT = int(os.getenv('SUBMISSION_TIMEOUT', 24*60*60))
# How many seconds to wait before considering the polling a failure
NO_NEW_ENTRY_POLL_TIMEOUT = int(os.getenv('NO_NEW_ENTRY_POLL_TIMEOUT', 180))
# Where to look if submission has finished
EXITED_SIGNAL_PATH = os.getenv('EXITED_SIGNAL_PATH', 'shared/exited')

line_count=0
start_time = time.time()
last_successful_poll_time = start_time
submission_total_runtime = 0

def make_subprocess_call(command, shell=False):
    result = subprocess.run(command.split(), shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    return result.returncode, stdout, stderr

###############################################################
# Helper Functions End
###############################################################
def sigusr1_handler(signum, stackframe):
    print("The evaluator received SIGUSR1... shutting down our operation")
    print("Last successful poll was: {}. Total runtime {}.".format(last_successful_poll_time, submission_total_runtime))
    # Because SIGUSR1 is '10' on Linux
    sys.exit(10)



class AICrowdSubContractorError(Exception):
    pass

class AICrowdSubContractor:

    def __init__(self):
        self.oracle_events = crowdai_api.events.CrowdAIEvents(with_oracle=True)
        self.totalNumberSteps = None
        self.finished = False
        self.payload = None

    def generate_json(self, stage, episodes):
        pass

    def read_json_file(self, path):
        try:
            with open(path) as file:
                return json.load(file), True
        except:
            return {}, False

    def update_status(self, finished=False):
        status_file = PERFORMANCE_DIRECTORY + 'status.json'
        # {'totalNumberSteps': 18012, 'totalNumberEpisodes': 3, 'currentEnvironment': 'MineRLObtainDiamond-v0'}
        payload, found = self.read_json_file(status_file)
        payload['state'] = 'PENDING'
        payload['episodes'] = []
        score = 0.00

        for episode in range(payload['totalNumberEpisodes'] + 1):
            # 000000-MineRLObtainDiamond-v0.json
            episode_file = PERFORMANCE_DIRECTORY + str(episode).zfill(6) + '-' + payload['currentEnvironment'] + '.json'
            episode_info, found = self.read_json_file(episode_file)
            if found:
                # Atleast one file present, so submission has started for sure.
                payload['state'] = 'IN_PROGRESS'
                episode_info['state'] = 'IN_PROGRESS'
                if episode < payload['totalNumberEpisodes']:
                    episode_info['state'] = 'FINISHED'
                episode_info['rewards'] = sum(episode_info['rewards'])
                score += episode_info['rewards']
                payload['episodes'].append(episode_info)
            elif finished and not found and payload['state'] == 'IN_PROGRESS' and episode == payload['totalNumberEpisodes']:
                # One missing is expected in proper finish.
                print('FInished on episode: %s', episode)
                payload['state'] = 'FINISHED'
                payload['score'] = {
                    "score": score,
                    "score_secondary": 0.0
                }
                self.finished = True
                self.payload = payload
                self.handle_success_event(payload)
                return True
            elif finished:
                break

        if finished:
            if self.finished:
                self.handle_success_event(self.payload)
                return True
            # Abrupt exit of agent code.
            payload['state'] = 'ERROR'
            self.handle_error_event(payload)
            return True

        if self.totalNumberSteps != payload['totalNumberSteps']:
            self.totalNumberSteps = payload['totalNumberSteps']
            self.handle_info_event(payload)
            return True

        return False

    def handle_info_event(self, payload):
        print(payload)
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_INFO,
            payload=payload
        )

    def handle_success_event(self, payload):
        print(payload)
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_SUCCESS,
            payload=payload
        )

    def handle_error_event(self, payload):
        print(payload)
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_ERROR,
            payload=payload
        )

if __name__ == '__main__':
    subcontractor = AICrowdSubContractor()
    # Register a signal hanlder for SIGUSR1 that is sent by the wrapper script when it wants to stop the parser
    signal.signal(signal.SIGUSR1, sigusr1_handler)

    status_file = PERFORMANCE_DIRECTORY + 'status.json'
    status_file_found = False

    while True:
        if not status_file_found:
            if not os.path.exists(status_file):
                print("PARSER: Waiting for status file to be generated by instance manager...")
                time.sleep(10)
                continue
            else:
                print("PARSER: Status file found... ({now})".format(now=time.time()))
                status_file_found = True

        submission_total_runtime = time.time() - start_time

        if submission_total_runtime > SUBMISSION_TIMEOUT:
            raise Exception("Submission runtime({runtime}s) exceeded timeout({timeout}s)".format(runtime=submission_total_runtime, timeout=SUBMISSION_TIMEOUT))

        updated = subcontractor.update_status(finished=False)
        if not updated:
            time_since_last_update = time.time() - last_successful_update_time
            if time_since_last_update > NO_NEW_ENTRY_POLL_TIMEOUT:
                raise Exception("Submission update polling timed out (no new update was written in {lsp}s) exceeded poll timeout({timeout}s)".format(lsp=time_since_last_update, timeout=NO_NEW_ENTRY_POLL_TIMEOUT))
        else:
            last_successful_update_time = time.time()

        if os.path.exists(EXITED_SIGNAL_PATH):
            # Sweet time to get performance written after agent exit
            time.sleep(10)
            subcontractor.update_status()
            subcontractor.update_status(finished=True)
            end_time = time.time()
            print("Total time taken:", end_time - start_time)
            break

        time.sleep(POLL_INTERVAL)
