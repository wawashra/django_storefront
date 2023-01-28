#!/bin/bash
source ./ci_scripts/common/common_var.sh
args="${1}"

if [ "$(docker ps | grep ${STOREFRONT_CONTAINER_NAME})" ]; then
    echo "${STOREFRONT_CONTAINER_NAME} already running."
    echo "Will exec: ${args}, via ${STOREFRONT_CONTAINER_NAME}, container"
    docker exec -it ${STOREFRONT_CONTAINER_NAME} ${args}
else
    echo "${STOREFRONT_CONTAINER_NAME} is not up & running."
fi
