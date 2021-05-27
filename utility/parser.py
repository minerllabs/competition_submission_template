#!/usr/bin/env python3
import copy
import json
import os
import signal
import sys
import subprocess
import time
import glob

import crowdai_api
import uuid


class AICrowdSubContractor:
    def __init__(self):
        self.debug = False
        self.oracle_events = crowdai_api.events.CrowdAIEvents(with_oracle=True)

    def handle_event(self, payload):
        if self.debug:
            print(payload)
        if payload['state'] == 'FINISHED':
            self.handle_success_event(payload)
        elif payload['state'] == 'ERROR':
            self.handle_error_event(payload)
        else:
            self.handle_info_event(payload)

    def handle_info_event(self, payload):
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_INFO,
            payload=payload
        )

    def handle_success_event(self, payload):
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_SUCCESS,
            payload=payload
        )

    def handle_error_event(self, payload):
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_ERROR,
            payload=payload
        )


class Parser:
    def __init__(self, directory, allowed_environment=None, maximum_instances=None, maximum_steps=None, raise_on_error=True, no_entry_poll_timeout=1800, submission_timeout=None, initial_poll_timeout=30*60, debug=False):
        self.directory = directory
        self.allowed_environment = allowed_environment
        self.maximum_instances = maximum_instances
        self.maximum_steps = maximum_steps
        self.raise_on_error = raise_on_error
        self.no_entry_poll_timeout = no_entry_poll_timeout
        self.submission_timeout = submission_timeout
        self.initial_poll_timeout = initial_poll_timeout

        self.aicrowd_subcontractor = AICrowdSubContractor()
        self.aicrowd_subcontractor.debug = debug
        self.start_time = time.time()
        self.current_state = {}
        self.finished = {}
        self.last_change_time = {}
        self.totalInstances = 0
        self.payload = {
            'state': 'PENDING',
            'score': {},
            'instances': []
        }
        self.freeze = False

    def add_instance(self, instance_id):
        self.current_state[instance_id] = {
            'state': 'PENDING',
            'episodes': [],
            'score': {},
            'totalNumberSteps': 0
        }
        self.finished[instance_id] = False
        self.last_change_time[instance_id] = time.time()
        self.totalInstances += 1

    def read_json_file(self, path):
        try:
            with open(path) as file:
                return json.load(file), True
        except:
            return {}, False

    def send_information_to_sourcerer(self):
        if not self.freeze:
            instance_started = False
            instance_running = False
            for instance_id in self.current_state:
                instance_state = self.current_state[instance_id]['state']
                if instance_state != 'PENDING':
                    instance_started = True
                if instance_state != 'FINISHED' and instance_state != 'ERROR':
                    instance_running = True
            if instance_started:
                self.payload['state'] = 'RUNNING'
            if self.totalInstances > 0 and not instance_running:
                self.payload['state'] = 'FINISHED'
            self.payload['instances'] = self.current_state

            score = 0.0
            instances = 0
            for state in self.current_state:
                episodes = self.current_state[state]['episodes']
                for episode in episodes:
                    score += episode['rewards']
                    instances += 1
            if instances > 0:
                score = str(round(score/instances, 2))
            self.payload['score'] = {
                'score': score,
                'score_secondary': sum(self.current_state[x]['score']['score_secondary'] for x in self.current_state)
            }

        self.aicrowd_subcontractor.handle_event(self.payload)


    def update_instance_if_changed(self, instance_id, currentInformation):
        updated = False
        if self.finished[instance_id]:
            return False

        previousInformation = self.current_state[instance_id]
        if previousInformation['totalNumberSteps'] != currentInformation['totalNumberSteps']:
            updated = True
        self.current_state[instance_id] = copy.deepcopy(currentInformation)
        return updated

    def check_for_condition_breach(self):
        breached = False
        if self.totalInstances > self.maximum_instances:
            breached = True
            self.payload['reason'] = 'You started more instances (%d) then allowed limit (%d).' % (self.totalInstances, self.maximum_instances)
        totalSteps = sum(self.current_state[x]["totalNumberSteps"] for x in self.current_state)
        if self.maximum_steps and totalSteps > self.maximum_steps:
            breached = True
            self.payload['reason'] = 'Steps (%d) are more then allowed limit (%d).' % (totalSteps, self.maximum_steps)
        if (time.time() - self.start_time) > self.submission_timeout:
            breached = True
            self.payload['reason'] = 'Submission time increased the threshold (%d seconds).' % (self.submission_timeout)
        if self.totalInstances == 0 and (time.time() - self.start_time) > self.initial_poll_timeout:
            breached = True
            self.payload['reason'] = 'No instance started in threshold (%d seconds).' % (self.initial_poll_timeout)

        if breached:
            self.payload['state'] = 'ERROR'
        return breached

    def update_information(self, finished=False):
        if self.freeze:
            return

        any_instance_updated = False
        instance_folders = list(filter(lambda x: os.path.isdir(os.path.join(self.directory, x)), os.listdir(self.directory)))
        for instance_folder in instance_folders:
            instance_id = instance_folder.split('mc_')[1]
            if instance_id not in self.current_state:
                self.add_instance(instance_id)

            currentInformation = self.read_instance_information(instance_id, '/'.join([self.directory, instance_folder]))
            updated = self.update_instance_if_changed(instance_id, currentInformation)

            if updated:
                self.last_change_time[instance_id] = time.time()

            if (not updated and not self.finished[instance_id]) or finished:
                currentTime = time.time()
                if (currentTime - self.last_change_time[instance_id]) > self.no_entry_poll_timeout or finished:
                    if 'totalNumberEpisodes' in currentInformation and len(currentInformation['episodes']) == currentInformation['totalNumberEpisodes']:
                        currentInformation['state'] = 'FINISHED'
                    else:
                        currentInformation['state'] = 'ERROR'
                    self.update_instance_if_changed(instance_id, currentInformation)
                    self.finished[instance_id] = True
                    updated = True

            if updated:
                any_instance_updated = True

        if any_instance_updated:
            self.send_information_to_sourcerer()
        if self.check_for_condition_breach():
            self.freeze = True
            self.send_information_to_sourcerer()
        if finished and not self.freeze:
            return

    def check_for_allowed_environment(self, environment, payload):
        if self.allowed_environment is not None:
            if not environment in self.allowed_environment:
                payload['state'] = 'ERROR'
                payload['reason'] = 'Wrong environment used, you should use "%s" instead of "%s"' \
                                    % (MINERL_GYM_ENV, payload['currentEnvironment'])
                if self.raise_on_error:
                    raise Exception(payload['reason'])
                return False
        return True

    def read_instance_information(self, instance_id, instance_directory):
        status_file = instance_directory + '/status.json'
        # {'totalNumberSteps': 18012, 'totalNumberEpisodes': 3, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0'}
        payload, found = self.read_json_file(status_file)
        payload['state'] = 'PENDING'
        payload['episodes'] = []
        score = 0.00

        if 'currentEnvironment' in payload:
            self.check_for_allowed_environment(payload['currentEnvironment'], payload)

        for episode in range(payload.get('totalNumberEpisodes', -1) + 1):
            # 000000-MineRLObtainDiamondVectorObf-v0.json
            episode_file = instance_directory + '/' + str(episode).zfill(6) + '-' + payload['currentEnvironment'] + '.json'
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
            else:
                break

        if len(payload['episodes']) > 0:
            score = str(round(score/len(payload['episodes']), 2))

        payload['score'] = {
            "score": score,
            "score_secondary": 0.0
        }

        if 'totalNumberSteps' not in payload:
            payload['totalNumberSteps'] = 0
        return payload

# Debug the aicrowd json
ENABLE_AICROWD_JSON_OUTPUT = bool(os.getenv('ENABLE_AICROWD_JSON_OUTPUT', 'True'))
# Where the output files will be located
PERFORMANCE_DIRECTORY = os.getenv('PERFORMANCE_DIRECTORY', 'performance/')
# Time (in seconds) to wait before checking performance directory updates
POLL_INTERVAL=1
# How many seconds to let the submission run
SUBMISSION_TIMEOUT = int(os.getenv('SUBMISSION_TIMEOUT', 24*60*60))
# How many seconds to wait before first instance start running
INITIAL_POLL_TIMEOUT = int(os.getenv('INITIAL_POLL_TIMEOUT', 3*60))
# How many seconds to wait before considering instance manager is dead
NO_NEW_ENTRY_POLL_TIMEOUT = int(os.getenv('NO_NEW_ENTRY_POLL_TIMEOUT', 180))
# Maximum number of instances to launch
MAX_ALLOWED_INSTANCES = int(os.getenv('MAX_ALLOWED_INSTANCES', 2))
# Maximum number of steps
MAX_ALLOWED_STEPS = int(os.getenv('MAX_ALLOWED_STEPS', 0)) or None
# All the evaluations will be allowed to run only below gym environment
MINERL_GYM_ENV = os.getenv('MINERL_GYM_ENV', 'MineRLObtainDiamondVectorObf-v0,MineRLObtainDiamond-v0')

# Where to look if submission has finished
EXITED_SIGNAL_PATH = os.getenv('EXITED_SIGNAL_PATH', 'shared/exited')


###############################################################
# Helper Functions End
###############################################################
def sigusr1_handler(signum, stackframe):
    print("The evaluator received SIGUSR1... shutting down our operation")
    sys.exit(10)


if __name__ == '__main__':
    parser = Parser(PERFORMANCE_DIRECTORY,
                    allowed_environment=MINERL_GYM_ENV,
                    maximum_instances=MAX_ALLOWED_INSTANCES,
                    maximum_steps=MAX_ALLOWED_STEPS,
                    raise_on_error=True,
                    no_entry_poll_timeout=NO_NEW_ENTRY_POLL_TIMEOUT,
                    submission_timeout=SUBMISSION_TIMEOUT,
                    initial_poll_timeout=INITIAL_POLL_TIMEOUT,
                    debug=ENABLE_AICROWD_JSON_OUTPUT)

    while True:
        parser.update_information()

        if os.path.exists(EXITED_SIGNAL_PATH):
            # Sweet time to get performance written after agent exit
            time.sleep(10)
            parser.update_information(finished=True)
            break

        time.sleep(POLL_INTERVAL)
