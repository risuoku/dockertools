#!/bin/bash

set +e

COMMAND_TYPE=$1
VOLUMES_OPTION="--volumes-from={{ volume_image_name }}"
APPLICATION_IMAGE_NAME="{{ app_image_name }}"
DOCKER_BIN="{{ docker_bin }}"

case $COMMAND_TYPE in
  "console" )
    $DOCKER_BIN run -it --rm $VOLUMES_OPTION $APPLICATION_IMAGE_NAME /bin/bash
    ;;
  "jupyter" )
    $DOCKER_BIN run -d --rm $VOLUMES_OPTION -p {{ jupyter_port }}:8888 $APPLICATION_IMAGE_NAME jupyter notebook --ip 0.0.0.0 --allow-root --no-browser --NotebookApp.token=''
    ;;
  "command" )
    $DOCKER_BIN run -d --rm $VOLUMES_OPTION $APPLICATION_IMAGE_NAME "${@:2:$#}"
    ;;
  * )
    echo "invalid type!"
    ;;
esac
