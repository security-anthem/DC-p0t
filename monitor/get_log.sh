#!/usr/bin/bash

sudo rm -rf log/docker_log/*
mkdir -p log/
sudo docker diff victim | sed 's/^C //g' | sed 's/^A //g' | while read line
do
    TOTAL=$(sudo docker exec victim ls -l $line | head -n 1 | cut -c 1-5)
    if test "$TOTAL" != "total" ; then
        mkdir -p log/docker_log/$(dirname $line)
        sudo docker cp victim:$line log/docker_log/$line
    fi
done
sudo docker diff victim > log/docker_diff_result.log
sudo docker logs victim > log/docker_logs_result.log
