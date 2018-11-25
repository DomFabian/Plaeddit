#!/bin/bash

# this script is to start the docker image that handles the live stream
# it is currently configured to run in the background
docker start cam

# if you want to get some stats about the CPU usage, etc., run
# `docker stats`
