#!/usr/bin/env python3
import sys, os, re, json, time, requests
import pickle
import joblib


joblib_model = joblib.load('joblib_saved_model')


class OpenhabAgent:
	def __init__(self, ip='127.0.0.1', port=8080):
		self.base_url = "http://localhost:8080/rest/items"
		self.header = {'accept': 'application/json'}
		self.params = {'text': ""}
		self.post = 'curl -X POST --header "Content-type: text/plain" --header "Accept: application/json" -d' 
		try:
			# NOTE: openHAB api GET responds normally with python requests lib
			openhab_response = requests.get(self.base_url, headers=self.header, params=self.params)
			print("Connection established with openHAB")
		except:
			print("Failed connection to openHAB ....")
			sys.exit()

	# NOTE: MUST use curl for openHAB api POST as python requests lib does NOT trigger physical light change; although it does trigger an event...
	def on(self, item):
		# print("TURNING ON: " + item)
		os.system(self.post + ' "ON" "' + self.base_url+item)

	def off(self, item):
		# print("TURNING OFF: " + item)
		os.system(self.post + ' "OFF" "' + self.base_url+item)


def log_system_status(smartflow_status):
    """"""
    for key, value in smartflow_status.items():
    	print(key,value)
    log_info_string = json.dumps(smartflow_status)
    with open("smartflow_events.log", "a") as log_file:
        log_file.write(log_info_string + "\n")
        log_file.close()


def analyze_smart_home(smart_flow_dict):
    """"""
    s_flow_dict = smart_flow_dict
    smartflow_list = [[
        0.0, # Time
        # Kitchen
        s_flow_dict['kitchen_light'],
        s_flow_dict['kitchen_motion_sensor'],
        s_flow_dict['kitchen_door_sensor'],

        # Office
        s_flow_dict['office_light'],
        s_flow_dict['office_motion_sensor'],

        # Living Room
        s_flow_dict['living_room_light'],
        s_flow_dict['living_room_motion_sensor'],
        s_flow_dict['living_room_door_sensor'],
        
        # Bedroom
        s_flow_dict['bedroom_light'],
        s_flow_dict['bedroom_motion_sensor']
    ]]
# TODO: CRASHING HERE BECAUSE DIMENSIONS DONT MATCH ML MODEL ATM!!!    
    # smartflow_status = joblib_model.predict(smartflow_list)
    # print(f'Status of Smart Home: {smartflow_status}')

    # s_flow_dict.update({"smartflow_status": str(smartflow_status[0])})
# HARDCODED STATUS TO 0 UNTIL NEW MODEL IS CREATED BY A.S
    s_flow_dict.update({"smartflow_status": str("0")})
    log_system_status(s_flow_dict)


# Define Machine Learning Dataset parameters (except for temperature)
smartflow_dict = {
    'date': "null",
    'time': "null",  # Time of day; hardcoded to 0.0 for now
    'kitchen_light': 0.0,  # Kitchen(M019)
    'kitchen_motion_sensor': 0.0,  # Kitchen (TBD)
    'kitchen_door_sensor': 0.0,  # Back Window(D002)
    'kitchen_temperature': 0.0,
    'office_light': 0.0,  # Office(M027)
    'office_motion_sensor': 0.0,  # Office(TBD)
    'office_temperature': 0.0,
    'living_room_light': 0.0,  # Living Room(TBD)
    'living_room_motion_sensor': 0.0,  # Living Room(M020)
    'living_room_door_sensor': 0.0,  # Front Door(D001)
    'living_room_temperature': 0.0,
    'bedroom_light': 0.0,  # Master Bedroom(M007)
    'bedroom_motion_sensor': 0.0,  # Bedroom(TBD)
    'bedroom_temperature': 0.0
}

openhab_agent = OpenhabAgent()
# openhab_agent.on('/hue_0107_ecb5fa1b9120_7_presence"')
# print(smartflow_dict['kitchen_motion_sensor'])
# time.sleep(3)
# openhab_agent.off('/hue_0107_ecb5fa1b9120_7_presence"')
# print(smartflow_dict['kitchen_motion_sensor'])

kitchen_light_id = '/hue_0100_ecb5fa1b9120_1_brightness"'
kitchen_motion_sensor_id = '/hue_0107_ecb5fa1b9120_7_presence"'

office_light_id = '/hue_0100_ecb5fa1b9120_2_brightness"'
office_motion_sensor_id = '/hue_0107_ecb5fa1b9120_2_presence"'

living_room_light_id = '/hue_0100_ecb5fa1b9120_3_brightness"'
living_room_motion_sensor_id = '/hue_0107_ecb5fa1b9120_29_presence"'

bedroom_light_id = '/hue_0100_ecb5fa1b9120_4_brightness"'
bedroom_motion_sensor_id = '/hue_0107_ecb5fa1b9120_18_presence"'

def synchronize_lights(current_room):
	# Turn off all lights not in current_room
	if current_room is "kitchen":
		# if smartflow_dict['office_light'] == 1.0:
		openhab_agent.off(office_light_id)
		if smartflow_dict['office_motion_sensor'] == 1.0:
			openhab_agent.off(office_motion_sensor_id)
		# if smartflow_dict['living_room_light'] == 1.0:
		openhab_agent.off(living_room_light_id)
		if smartflow_dict['living_room_motion_sensor'] == 1.0:
			openhab_agent.off(living_room_motion_sensor_id)
		# if smartflow_dict['bedroom_light'] == 1.0:
		openhab_agent.off(bedroom_light_id)
		if smartflow_dict['bedroom_motion_sensor'] == 1.0:
			openhab_agent.off(bedroom_motion_sensor_id)	
	elif current_room is "office":
		# if smartflow_dict['kitchen_light'] == 1.0:
		openhab_agent.off(kitchen_light_id)
		if smartflow_dict['kitchen_motion_sensor'] == 1.0:
			openhab_agent.off(kitchen_motion_sensor_id)
		# if smartflow_dict['living_room_light'] == 1.0:
		openhab_agent.off(living_room_light_id)
		if smartflow_dict['living_room_motion_sensor'] == 1.0:
			openhab_agent.off(living_room_motion_sensor_id)
		# if smartflow_dict['bedroom_light'] == 1.0:
		openhab_agent.off(bedroom_light_id)
		if smartflow_dict['bedroom_motion_sensor'] == 1.0:
				openhab_agent.off(bedroom_motion_sensor_id)	
	elif current_room is "living_room":
		# if smartflow_dict['kitchen_light'] == 1.0:
		openhab_agent.off(kitchen_light_id)
		if smartflow_dict['kitchen_motion_sensor'] == 1.0:
				openhab_agent.off(kitchen_motion_sensor_id)
		# if smartflow_dict['office_light'] == 1.0:
		openhab_agent.off(office_light_id)
		if smartflow_dict['office_motion_sensor'] == 1.0:
				openhab_agent.off(office_motion_sensor_id)
		# if smartflow_dict['bedroom_light'] == 1.0:
		openhab_agent.off(bedroom_light_id)
		if smartflow_dict['bedroom_motion_sensor'] == 1.0:
				openhab_agent.off(bedroom_motion_sensor_id)
	elif current_room is "bedroom":
		# if smartflow_dict['kitchen_light'] == 1.0:
		openhab_agent.off(kitchen_light_id)
		if smartflow_dict['kitchen_motion_sensor'] == 1.0:
				openhab_agent.off(kitchen_motion_sensor_id)
		# if smartflow_dict['office_light'] == 1.0:
		openhab_agent.off(office_light_id)
		if smartflow_dict['office_motion_sensor'] == 1.0:
				openhab_agent.off(office_motion_sensor_id)
		# if smartflow_dict['living_room_light'] == 1.0:
		openhab_agent.off(living_room_light_id)
		if smartflow_dict['living_room_motion_sensor'] == 1.0:
				openhab_agent.off(living_room_motion_sensor_id)


# MAIN LOOP
while True:
    # Read from std input
    try:
        data = sys.stdin.readline()
    except KeyboardInterrupt:
        break
    if not data:
        break
    # print(data)
    # PARSING LOGIC
    log = re.match(r'(.*) - (.*)', data)
    log_id = log.group(1).split()
    log_status = log.group(2).split()
    smartflow_dict['date'] = log_id[0]
    smartflow_dict['time'] = log_id[1]

    # ML Model Population
    if log_id[2] == '[vent.ItemStateChangedEvent]':
        # KITCHEN
        if "_1_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['kitchen_light'] = 1.0
            else:
                smartflow_dict['kitchen_light'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_7_presence" in log_status[0]:
            if log_status[5] == "ON":
                smartflow_dict['kitchen_motion_sensor'] = 1.0
                synchronize_lights("kitchen")
            else:
                smartflow_dict['kitchen_motion_sensor'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_4_temperature" in log_status[0]:
        	print(log_status[5])
        	smartflow_dict['kitchen_temperature'] = log_status[5]
        	analyze_smart_home(smartflow_dict)
        # OFFICE
        elif "_2_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['office_light'] = 1.0
            else:
                smartflow_dict['office_light'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_2_presence" in log_status[0]:
            if log_status[5] == "ON":
                smartflow_dict['office_motion_sensor'] = 1.0
                synchronize_lights("office")
            else:
                smartflow_dict['office_motion_sensor'] = 0.0
            analyze_smart_home(smartflow_dict)

        # LIVING ROOM
        elif "_3_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['living_room_light'] = 1.0
            else:
                smartflow_dict['living_room_light'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_29_presence" in log_status[0]:
            if log_status[5] == "ON":
                smartflow_dict['living_room_motion_sensor'] = 1.0
                synchronize_lights("living_room")
            else:
                smartflow_dict['living_room_motion_sensor'] = 0.0
            analyze_smart_home(smartflow_dict)

        # BEDROOM
        elif "_4_brightness" in log_status[0]:
            light_brightness = log_status[5]
            if int(light_brightness) > 1:
                smartflow_dict['bedroom_light'] = 1.0
            else:
                smartflow_dict['bedroom_light'] = 0.0
            analyze_smart_home(smartflow_dict)
        elif "_18_presence" in log_status[0]:
            if log_status[5] == "ON":
                smartflow_dict['bedroom_motion_sensor'] = 1.0
                synchronize_lights("bedroom")
            else:
                smartflow_dict['bedroom_motion_sensor'] = 0.0
            analyze_smart_home(smartflow_dict)

    # CUSTOM PARSING due to API issues with Samsung devices; requires internet connection
    elif log_id[2] == '[temChannelLinkRemovedEvent]':
        if "Multipurpose_Sensor_1" in log_status[1]:
            smartflow_dict['living_room_door_sensor'] = 1.0
        else:
            smartflow_dict['kitchen_door_sensor'] = 1.0
        analyze_smart_home(smartflow_dict)
    elif log_id[2] == '[.ItemChannelLinkAddedEvent]':
        if "Multipurpose_Sensor_1" in log_status[1]:
            smartflow_dict['living_room_door_sensor'] = 0.0
        else:
            smartflow_dict['kitchen_door_sensor'] = 0.0
        analyze_smart_home(smartflow_dict)
        