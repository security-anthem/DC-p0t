#!/usr/bin/bash

sudo rm -rf var/log/docker_log/*
mkdir -p var/log/
sudo docker diff victim | sed 's/^C //g' | sed 's/^A //g' | while read line
do
    TOTAL=$(sudo docker exec victim ls -l $line | head -n 1 | cut -c 1-5)
    if test "$TOTAL" != "total" ; then
        mkdir -p var/log/docker_log/$(dirname $line)
        sudo docker cp victim:$line var/log/docker_log/$line
    fi
done
sudo docker diff victim > var/log/docker_diff_result.txt
sudo docker logs victim > var/log/docker_logs_result.txt
