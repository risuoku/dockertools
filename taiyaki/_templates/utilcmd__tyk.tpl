#!/bin/bash

HOST_LOCATION="{{ hostname }}"

FIRST_COMMAND=$1
ALL_COMMAND=$@

if [ $FIRST_COMMAND = "runwithgpu" ]; then
  DOCKER_RUN_OPTION="--runtime=nvidia"
  ALL_COMMAND=`echo $ALL_COMMAND | sed -E 's/^runwithgpu //g'`
  ALL_COMMAND="run ${DOCKER_RUN_OPTION} ${ALL_COMMAND}"
fi

# execute
docker -H tcp://${HOST_LOCATION} $ALL_COMMAND
