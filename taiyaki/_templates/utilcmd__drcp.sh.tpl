#!/bin/bash

DOCKER_BIN="{{ docker_bin }}"
CONTAINER_ID=$1
TARGET_DIR=$2

if [ -z $CONTAINER_ID ]; then
  echo "no container id"
  exit 1
fi

if [ -z $TARGET_DIR ]; then
  echo "no target dir"
  exit 1
fi


for a in `$DOCKER_BIN exec $CONTAINER_ID "find $TARGET_DIR -type f"`
do
  mkdir -p `dirname $a` && $DOCKER_BIN cp $CONTAINER_ID:{{ docker_working_dir }}/$a $a
done
