FROM {{ base_image_name }}

WORKDIR {{ docker_working_dir }}

ENV APPLICATION_ENV docker
ENV PYTHONPATH {{ docker_working_dir }}

ENV LC_ALL ja_JP.UTF-8
ENV CLOUD_SDK_REPO cloud-sdk-xenial

COPY . .
