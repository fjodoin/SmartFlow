#!/usr/bin/env bash
echo [SMARTFLOW] openhab2/events.log monitoring scripted launched [...]
tail -n0 -f /home/corelee/Desktop/SmartFlow/smartflow_events.log | python3 /home/corelee/Desktop/SmartFlow/dashboard.py
