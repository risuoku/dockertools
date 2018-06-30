#!/bin/bash
{{ docker_bin }} create -v {{ volume_image_name }}:{{ docker_volume_dir }} --name {{ volume_image_name }} busybox
