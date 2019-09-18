#!/usr/bin/env bash

DIR=$(cd "$(dirname "$0")"; pwd)

docker build -t transport4j-build .
docker run -d -v $DIR/neo4j:/transport4j/neo4j transport4j-build neo4j/input