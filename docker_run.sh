#!/bin/bash


if [ -e environ_secret.sh ]
then
    echo "Note: Gathering environment variables from environ_secret.sh"
    source environ_secret.sh
else
    echo "Note: Gathering environment variables from environ.sh"
    source environ.sh
fi

# Expected Env variables : in environ.sh
sudo nvidia-docker run \
    --net=host \
    -v $(pwd)/../gradle-data-init/downloads:/home/aicrowd/.gradle:z \
    -v /tmp/shared:/shared:z \
    --user 0 \
    -e CROWDAI_IS_GRADING=True \
    -e CROWDAI_DEBUG_MODE=True \
    -it ${IMAGE_NAME}:${IMAGE_TAG} \
    xvfb-run --auto-servernum --server-args='-screen 0 640x480x24' \
    /home/aicrowd/run.sh
