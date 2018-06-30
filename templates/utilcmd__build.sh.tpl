#!/bin/bash

APPLICATION_IMAGE_NAME="{{ app_image_name }}"
DOCKER_BIN="{{ docker_bin }}"

$DOCKER_BIN ps --filter "ancestor=${APPLICATION_IMAGE_NAME}" --format="{% raw %}{{.ID}}{% endraw %}" | xargs $DOCKER_BIN stop
$DOCKER_BIN rmi $APPLICATION_IMAGE_NAME

$DOCKER_BIN build -t $APPLICATION_IMAGE_NAME ./
