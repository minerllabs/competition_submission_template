#!/bin/bash

if [ -e environ_secret.sh ]
then
    source utility/environ_secret.sh
else
    source utility/environ.sh
fi

# Expected Env variables : in environ.sh

REPO2DOCKER="$(which aicrowd-repo2docker)"

sudo ${REPO2DOCKER} --no-run \
  --user-id 1001 \
  --user-name aicrowd \
  --image-name ${IMAGE_NAME}:${IMAGE_TAG} \
  --debug .

#sudo docker push "${IMAGE_NAME}:${IMAGE_TAG}"
