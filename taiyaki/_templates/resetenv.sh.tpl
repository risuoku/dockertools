ADDITIONAL_PATH="${PWD}/utilcmd:"
export PATH=`echo $PATH | sed -E "s#${ADDITIONAL_PATH}##g"`
export DOCKER_BIN=""
