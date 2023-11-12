#!/bin/bash
USAGE="Usage: $0 IP1 IP2 IP3 ..."

if [ "$#" == "0" ]; then
	echo "$USAGE"
	exit 1
fi

MASTER="$1"
COMMAND = ssh student@$MASTER "docker swarm leave --force > /dev/null; docker swarm init --advertise-addr $MASTER | grep "docker swarm" | head -n 1"
shift
while (( "$#" )); do
    COMMAND = ssh student@$1 "docker swarm leave --force > /dev/null; $COMMAND"
    shift
done