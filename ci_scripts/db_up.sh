#!/bin/bash
source ./ci_scripts/common/common_var.sh

if [ ! "$(docker network ls | grep ${STOREFRONT_NETWORK_NAME})" ]; then
    echo "Creating ${STOREFRONT_NETWORK_NAME} network ..."
    docker network create -d bridge ${STOREFRONT_NETWORK_NAME}
fi

echo "Running ${STOREFRONT_DATABASE_CONTAINER_NAME} in global ${STOREFRONT_NETWORK_NAME} network ..."
docker-compose -f ./ci_docker/storefront_database/docker-compose.yml up -d
