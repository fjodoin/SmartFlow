#!/usr/bin/env bash
TEST_VAR=$(wc -l /var/log/openhab2/events.log | awk '{print $1}')
echo $TEST_VAR
#tail /var/log/openhab2/events.log
