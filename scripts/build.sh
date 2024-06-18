#!/bin/bash

build_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")"/. && pwd)"
image_name="crypto-api:latest"

docker rmi "$image_name" > /dev/null 2>&1 || true
docker build -t "$image_name" -f "$build_directory/Dockerfile" "$build_directory/.."

kind load docker-image docker.io/library/crypto-api:latest --name asansaz

release_name="crypto-api"
helm uninstall $release_name > /dev/null 2>&1 || true
helm install $release_name "$build_directory/../deployment"
