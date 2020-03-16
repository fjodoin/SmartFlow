#!/usr/bin/env python3
import sys, re, json, time
from random import seed, randint
seed(1)
while True:
    data = "1234 yyyy-mm-dd hh:mm:ss.ddd [vent.ItemStateChangedEvent] - device:info:xyz changed from previous value to"
    random_number = randint(0, 100)
    data = data + " " + str(random_number)
    log = re.match(r'(.*) - (.*)', data)
    log_info_list = log.group(1).split()
    log_info_dict = {
    "events_log_id": log_info_list[0],
    "events_log_datestamp": log_info_list[1],
    "events_log_timestamp": log_info_list[2],
    "events_log_type": log_info_list[3].strip("[|]"),
    }
    if(log_info_dict['events_log_type'] == 'vent.ItemStateChangedEvent'):
        log_info = re.match(r'(.*) changed .* to (.*)', log.group(2))
#        print(log_info)
        my_value = int(log_info.group(2))
        log_info_dict.update({"events_hardware_id" : log_info.group(1)})
        log_info_dict.update({"events_value" : my_value})
        log_info_string = json.dumps(log_info_dict)
    else:
        log_info_dict.update({"events_log_info" : log.group(2)})
        log_info_string = json.dumps(log_info_dict)

    with open("temp_events_log.log", "a") as log_file:
        log_file.write(log_info_string + "\n")
        log_file.close()
    time.sleep(3)
sys.exit()
