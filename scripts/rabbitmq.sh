#!/bin/bash
# call "rabbitmqctl stop" when exiting
trap "{ echo Stopping rabbitmq; rabbitmqctl stop_app; exit 0; }" EXIT

echo Starting rabbitmq
rabbitmq-server
