#!/usr/bin/env python3
import sys, re, json, time
import pickle
import joblib

joblib_model = joblib.load('joblib_saved_model')


def log_system_status(smartflow_status):
    """"""
    print(smartflow_status)
    log_info_string = json.dumps(smartflow_status)
    with open("events_log.log", "a") as log_file:
        log_file.write(log_info_string + "\n")
        log_file.close()


def analyze_smart_home(smart_flow_dict):
    """"""
    s_flow_dict = smart_flow_dict
    smartflow_list = [[
        0.0,
        s_flow_dict['light_1'],
        s_flow_dict['motion_sensor_1'],
        s_flow_dict['light_2'],
        s_flow_dict['light_3'],
        0.0,
        s_flow_dict['door_sensor'],
        s_flow_dict['window_sensor']
    ]]
    smartflow_status = joblib_model.predict(smartflow_list)
    print(f'Status of Smart Home: {smartflow_status}')

    s_flow_dict.update({"smartflow_status": str(smartflow_status[0])})
    log_system_status(s_flow_dict)


# Define Machine Learning Dataset parameters
smartflow_dict = {
    'date': "null",
    'time': "null",  # Time of day; hardcoded for 0.0 for now
    'light_1': 0.0,  # Kitchen(M019)
    'light_2': 0.0,  # Master Bedroom(M007)
    'light_3': 0.0,  # Office(M027)
    'door_sensor': 0.0,  # Front Door(D001)
    'window_sensor': 0.0,  # Back Window(D002)
    'motion_sensor_1': 0.0  # Living Room(M020)
}

# MAIN LOOP
while True:
    # Read from std input
    try:
        data = sys.stdin.readline()
    except KeyboardInterrupt:
        break
    if not data:
        break
    print(data)
    # PARSING LOGIC
    log = re.match(r'(.*) - (.*)', data)
    log_id = log.group(1).split()
    log_status = log.group(2).split()
    smartflow_dict['date'] = log_id[0]
    smartflow_dict['time'] = log_id[1]

    # ML Model Population
    if log_id[2] == '[vent.ItemStateChangedEvent]':
        if "_1_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['light_1'] = 1.0
            else:
                smartflow_dict['light_1'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_2_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['light_2'] = 1.0
            else:
                smartflow_dict['light_2'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_3_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['light_3'] = 1.0
            else:
                smartflow_dict['light_3'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_presence" in log_status[0]:
            if log_status[5] == "ON":
                smartflow_dict['motion_sensor_1'] = 1.0
            else:
                smartflow_dict['motion_sensor_1'] = 0.0
            analyze_smart_home(smartflow_dict)
    elif log_id[2] == '[temChannelLinkRemovedEvent]':
        if "Multipurpose_Sensor_1" in log_status[1]:
            smartflow_dict['door_sensor'] = 1.0
        else:
            smartflow_dict['window_sensor'] = 1.0
        analyze_smart_home(smartflow_dict)
    elif log_id[2] == '[.ItemChannelLinkAddedEvent]':
        if "Multipurpose_Sensor_1" in log_status[1]:
            smartflow_dict['door_sensor'] = 0.0
        else:
            smartflow_dict['window_sensor'] = 0.0
        analyze_smart_home(smartflow_dict)
        