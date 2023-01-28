#!/bin/bash
source ./ci_scripts/common/common_var.sh

if [ "$(docker ps | grep ${STOREFRONT_DATABASE_CONTAINER_NAME})" ]; then
    echo "${STOREFRONT_DATABASE_CONTAINER_NAME} already up & running."
    echo "Running ${STOREFRONT_CONTAINER_NAME} in global ${STOREFRONT_NETWORK_NAME} network ..."
    docker-compose -f ./ci_docker/storefront_app/docker-compose.yml up
else
    echo "Can't run ${STOREFRONT_CONTAINER_NAME}, because the DB ${STOREFRONT_DATABASE_CONTAINER_NAME} is not up & running."
fi
