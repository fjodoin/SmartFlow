#!/usr/bin/env bash
echo [SMARTFLOW] openhab2/events.log monitoring scripted launched [...]
tail -n0 -f /var/log/openhab2/events.log | python3 /home/corelee/Desktop/SmartFlow/events_parser.py
