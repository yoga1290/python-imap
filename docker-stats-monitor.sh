#!/bin/sh

TIMESTAMP=$(date "+%s")

docker stats --no-stream \
   --format "{\"timestamp\":\"$TIMESTAMP\", \"name\":\"{{.Name}}\",\"cpu\":\"{{.CPUPerc}}\",\"mem\":\"{{.MemUsage}}\", \"net\":\"{{.NetIO}}\"}" \
    >>docker-stats-monitor.log
