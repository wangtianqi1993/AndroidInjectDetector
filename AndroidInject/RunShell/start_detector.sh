#!/bin/bash

rm -f tpid
nohup python /root/AndroidInject/web/main.py > /root/AndroidInject/inject_dump.log &

tail -f /root/AndroidInject/inject_dump.log
echo $! > tpid
