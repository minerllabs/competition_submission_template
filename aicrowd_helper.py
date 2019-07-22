#!/usr/bin/env python
import crowdai_api
import os
import logging

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()
current_phase = None
training_progress = 0.0

def inference_start():
    ########################################################################
    # Register Inference Start event
    ########################################################################
    logging.info("Inference Start...")
    global current_phase
    current_phase = "inference"
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="inference_started",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:inference_started"
                    }
                )

def inference_end():
    ########################################################################
    # Register Inference End event
    ########################################################################
    logging.info("Inference End...")
    global current_phase
    current_phase = None
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="inference_ended",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:inference_ended"
                    }
                )

def inference_error():
    ########################################################################
    # Register Inference Error event
    ########################################################################
    logging.error("Inference Failed...")
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="inference_error",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:inference_error"
                    }
                )

def training_start():
    ########################################################################
    # Register Training Start event
    ########################################################################
    logging.info("Training Start...")
    global current_phase
    current_phase = "training"
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="training_started",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:training_started"
                    }
                )

def training_end():
    ########################################################################
    # Register Training End event
    ########################################################################
    logging.info("Training End...")
    register_progress(1.0)
    global current_phase
    current_phase = None
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="training_ended",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:training_ended"
                    }
                )

def training_error():
    ########################################################################
    # Register Training Error event
    ########################################################################
    logging.error("Training Failed...")
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="training_error",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:training_error"
                    }
                )


def register_progress(progress):
    ########################################################################
    # Register Evaluation Progress event
    # progress : float [0, 1]
    ########################################################################
    logging.info("Progress : {}".format(progress))
    global training_progress, current_phase
    if current_phase is None:
        raise Exception('Please register current phase by calling `training_start` \
                         or `inference_start` before sending progress.')
    if current_phase == "training":
        if progress < training_progress:
            logging.warn('Invalid progress update to %f while you are already \
                          at %f. Skipping it...', progress, training_progress)
            return
        training_progress = progress

    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="register_progress",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:register_progress",
                    "training_progress" : training_progress
                    }
                )

def submit(payload={}):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    logging.info("AIcrowd Submit")
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_SUCCESS,
                message="submit",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:submit",
                    },
                blocking=True
                )

def execution_error(error):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_ERROR,
                message="execution_error",
                payload={ #Arbitrary Payload
                    "event_type": "minerl_challenge:execution_error",
                    "error" : error
                    },
                blocking=True
                )
