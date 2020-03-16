#!/usr/bin/env bash
echo [SMARTFLOW] openhab2/events.log monitoring scripted launched [...]
tail -n0 -f /var/log/openhab2/events.log | python3 /home/corelee/Desktop/winter2020/coen490/events_parser.py
#tail -n0 -f /home/corelee/Desktop/winter2020/coen490/events_log.log | python3 /home/corelee/Desktop/winter2020/coen490/events_parser.py
