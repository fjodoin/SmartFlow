#!/usr/bin/env bash
LAST_NUM_LINE=1
while :
do
    NEW_NUM_LINE=$(wc -l /var/log/openhab2/events.log | awk '{print $1}')
    echo $NEW_NUM_LINE
    if test $NEW_NUM_LINE -gt $LAST_NUM_LINE
    then
      cat -n /var/log/openhab2/events.log | awk '$1>='$LAST_NUM_LINE | python3 /home/corelee/Desktop/coen490/events_parser.py
      LAST_NUM_LINE=$NEW_NUM_LINE
    fi  
  sleep 5
done
