#!/bin/bash
source ./ci_scripts/common/common_var.sh
echo "Build ${STOREFRONT_CONTAINER_NAME} ...."
docker-compose -f ./ci_docker/storefront_app/docker-compose.yml build
