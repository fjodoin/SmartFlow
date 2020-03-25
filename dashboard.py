#!/usr/bin/env python3
import sys
import datetime
import json
import time
import threading
from collections import deque

import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output


################################ LOG LISTENING ################################
ecosystem_status = {
	'kitchen_light': 0,
	'kitchen_motion_sensor': 0,
	'kitchen_door_sensor': 0,
	'kitchen_temperature': 0,
	'office_light': 0,
	'office_motion_sensor': 0,
	'office_temperature': 0,
	'living_room_light': 0,
	'living_room_motion_sensor': 0,
	'living_room_door_sensor': 0,
	'living_room_temperature': 0,
	'bedroom_light': 0,
	'bedroom_motion_sensor': 0,
	'bedroom_temperature': 0,
	'smartflow_status': 0
}


class EventAgentThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		counter_check = 0
		global ecosystem_status
		while True:
			try:
				# print("waiting...")
				data = sys.stdin.readline()
			except KeyboardInterrupt:
				break
			if not data:
				break
			data_dict = json.loads(data)
			# print(data_dict)
			counter_check += 1
			ecosystem_status = data_dict
			# print(counter_check)
			# print(ecosystem_status)

event_agent_thread = EventAgentThread()
event_agent_thread.start()			
################################ END OF LOG LISTENING ################################

################################ VARIABLES ################################
max_length = 20
temperature_max_length = 1
overview_max_length = 50

times = deque(maxlen=max_length)
temperature_times = deque(maxlen=temperature_max_length)
overview_times = deque(maxlen=overview_max_length)

# KITCHEN devices
kitchen_light = deque(maxlen=max_length)
kitchen_motion_sensor = deque(maxlen=max_length)
kitchen_door_sensor = deque(maxlen=max_length)
kitchen_temperature = deque(maxlen=temperature_max_length)

# OFFICE devices
office_light = deque(maxlen=max_length)
office_motion_sensor = deque(maxlen=max_length)
office_temperature = deque(maxlen=temperature_max_length)

# LIVING ROOM devices
living_room_light = deque(maxlen=max_length)
living_room_motion_sensor = deque(maxlen=max_length)
living_room_door_sensor = deque(maxlen=max_length)
living_room_temperature = deque(maxlen=temperature_max_length)

# BEDROOM devices
bedroom_light = deque(maxlen=max_length)
bedroom_motion_sensor = deque(maxlen=max_length)
bedroom_temperature = deque(maxlen=temperature_max_length)

#OVERVIEW
overview_devices_on = deque(maxlen=overview_max_length)
overview_smartflow_status = deque(maxlen=overview_max_length)

data = {
    # Room 1; KITCHEN
    'kitchen_light': kitchen_light,
    'kitchen_motion_sensor': kitchen_motion_sensor,
    'kitchen_door_sensor': kitchen_door_sensor,
    'kitchen_temperature': kitchen_temperature,
    # Room 2; OFFICE
    'office_light': office_light,
    'office_motion_sensor': office_motion_sensor,
    'office_temperature': office_temperature,
    
    # Room 3; LIVING ROOM
    'living_room_light': living_room_light,
    'living_room_motion_sensor': living_room_motion_sensor,
    'living_room_door_sensor': living_room_door_sensor,
    'living_room_temperature': living_room_temperature,

    # Room 4; BEDROOM
    'bedroom_light': bedroom_light,
    'bedroom_motion_sensor': bedroom_motion_sensor,
    'bedroom_temperature': bedroom_temperature,

    # OVERVIEW
    'overview_devices_on': overview_devices_on,
    'overview_smartflow_status': overview_smartflow_status
}

app = dash.Dash(__name__)
################################ END OF VARIABLES ################################

################################ DASHBOARD LAYOUT ################################
app.layout = html.Div(
    html.Div([
        html.H2('[---SMARTFLOW Dashboard---]', style={'color': "#282828"}),
        html.Div(id='live-update-text'),
        dcc.Graph(id='kitchen-graph'),
        dcc.Graph(id='office-graph'),
        dcc.Graph(id='living-room-graph'),
        dcc.Graph(id='bedroom-graph'),
        dcc.Graph(id='overview-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 2000,  # in milliseconds
            n_intervals=0
        )
    ], style={'textAlign': 'center'})
)
app.title = 'SMARTFLOW'

# KITCHEN GRAPH
@app.callback(Output('kitchen-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    t = datetime.datetime.now()
    # Synchronize TIME
    times.append(t)
    temperature_times.append(t)
    overview_times.append(t)
    
    # Room 1; KITCHEN
    # print(ecosystem_status)
    kitchen_light.append(ecosystem_status['kitchen_light'])
    kitchen_motion_sensor.append(ecosystem_status['kitchen_motion_sensor'])
    kitchen_door_sensor.append(ecosystem_status['kitchen_door_sensor'])
    kitchen_temperature.append(str(ecosystem_status['kitchen_temperature']) + "°C")

    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(
    	rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, {"colspan": 3}, None, None, None]],
    	subplot_titles=("Active Devices", "temperature: °C", "", "", "", "", "", "", "", ""))
    fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 0, 't': 50
    }
    fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': -0.01,
                               'y': 1
                               }

    # Room 1; KITCHEN
    fig.append_trace({
        'x': list(times),
        'y': list(data['kitchen_light']),
        'name': 'Light',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#FFFF00'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['kitchen_motion_sensor']),
        'name': 'Motion Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#124653'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['kitchen_door_sensor']),
        'name': 'Door Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10),
        'type': 'scatter',
        'opacity': 0.5,
        'fill': 'tozeroy'
    }, 1, 2)
    fig.append_trace({
    	'x': list(temperature_times),
    	'y': list(data['kitchen_temperature']),
    	'text': list(data['kitchen_temperature']),
    	'textposition': 'top center',
    	'name': 'Temperature',
    	'mode': 'markers+text',
    	'marker' : dict(size=30,
    					color='#FE8D8F'),
    	'type': 'scatter',
    }, 1, 7)

    fig.update_layout(title_text="[---KITCHEN---]", font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#C2C5CC',
    	plot_bgcolor='#C2C5CC', 
    	height=250,
    	yaxis=dict(
    		range=(0, 1)),
    	xaxis=dict(
    		constrain="domain")
    	)
    return fig

# OFFICE GRAPH
@app.callback(Output('office-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
	# Room 2; OFFICE
    office_light.append(ecosystem_status['office_light'])
    office_motion_sensor.append(ecosystem_status['office_motion_sensor'])
    office_temperature.append(str(ecosystem_status['office_temperature']) + "°C")

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
    	rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, {"colspan": 3}, None, None, None]],
    	subplot_titles=("Active Devices", "temperature: °C", "", "", "", "", "", "", "", ""))
    fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 0, 't': 50
    }
    fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': -0.01,
                               'y': 1
                               }
    # Room 2; OFFICE
    fig.append_trace({
        'x': list(times),
        'y': list(data['office_light']),
        'text': list(times),
        'name': 'Light',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#FFFF00'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['office_motion_sensor']),
        'text': list(times),
        'name': 'Motion Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#124653'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)
    fig.append_trace({
    	'x': list(temperature_times),
    	'y': list(data['office_temperature']),
    	'text': list(data['office_temperature']),
    	'textposition': 'top center',
    	'name': 'Temperature',
    	'mode': 'markers+text',
    	'marker' : dict(size=30,
    					color='#FE8D8F'),
    	'type': 'scatter',
    }, 1, 7)

    fig.update_layout(title_text="[---OFFICE---]", font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#B8D1FD',
    	plot_bgcolor='#B8D1FD', 
    	height=250,
    	yaxis=dict(
    		range=(0, 1)),
    	xaxis=dict(
    		constrain="domain"))
    return fig

# LIVING ROOM GRAPH
@app.callback(Output('living-room-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n): 
	# Room 3; LIVING ROOM
    living_room_light.append(ecosystem_status['living_room_light'])
    living_room_motion_sensor.append(ecosystem_status['living_room_motion_sensor'])
    living_room_door_sensor.append(ecosystem_status['living_room_door_sensor'])
    living_room_temperature.append(str(ecosystem_status['living_room_temperature']) + "°C")

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
        rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, {"colspan": 3}, None, None, None]],
        subplot_titles=("Active Devices", "temperature: °C", "", "", "", "", "", "", "", ""))
    fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 0, 't': 50
    }
    fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': -0.01,
                               'y': 1
                               }
    # Room 3; LIVING ROOM
    fig.append_trace({
        'x': list(times),
        'y': list(data['living_room_light']),
        'text': list(times),
        'name': 'Light',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#FFFF00'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['living_room_motion_sensor']),
        'text': list(times),
        'name': 'Motion Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#124653'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['living_room_door_sensor']),
        # 'text': list(times),
        'name': 'Door Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10),
        'type': 'scatter',
        'opacity': 0.5,
        'fill': 'tozeroy'
    }, 1, 2)
    fig.append_trace({
    	'x': list(temperature_times),
    	'y': list(data['living_room_temperature']),
    	'text': list(data['living_room_temperature']),
    	'textposition': 'top center',
    	'name': 'Temperature',
    	'mode': 'markers+text',
    	'marker' : dict(size=30,
    					color='#FE8D8F'),
    	'type': 'scatter',
    }, 1, 7)

    fig.update_layout(title_text="[---LIVING ROOM---]", font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#C2C5CC',
    	plot_bgcolor='#C2C5CC', 
    	height=250,
    	yaxis=dict(
    		range=(0, 1)),
    	xaxis=dict(
    		constrain="domain"))
    return fig

# BEDROOM GRAPH
@app.callback(Output('bedroom-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Room 4; BEDROOM
    bedroom_light.append(ecosystem_status['bedroom_light'])
    bedroom_motion_sensor.append(ecosystem_status['bedroom_motion_sensor'])
    bedroom_temperature.append(str(ecosystem_status['bedroom_temperature']) + "°C")

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
        rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, {"colspan": 3}, None, None, None]],
        subplot_titles=("Active Devices", "temperature: °C", "", "", "", "", "", "", "", ""))
    fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 0, 't': 50
    }
    fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': -0.01,
                               'y': 1
                               }
	 # Room 4
    fig.append_trace({
        'x': list(times),
        'y': list(data['bedroom_light']),
        'text': list(times),
        'name': 'Light',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#FFFF00'),
        'type': 'scatter',
    	'fill': 'tozeroy',
        'line': {'dash': 'dot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['bedroom_motion_sensor']),
        'text': list(times),
        'name': 'Motion Sensor',
        'mode': 'lines+markers',
        'marker' : dict(size=10, color='#124653'),
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)
    fig.append_trace({
    	'x': list(temperature_times),
    	'y': list(data['bedroom_temperature']),
    	'text': list(data['bedroom_temperature']),
    	'textposition': 'top center',
    	'name': 'Temperature',
    	'mode': 'markers+text',
    	'marker' : dict(size=30,
    					color='#FE8D8F'),
    	'type': 'scatter',
    }, 1, 7)

    fig.update_layout(title_text="[---BEDROOM---]", font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#B8D1FD',
    	plot_bgcolor='#B8D1FD', 
    	height=250,
    	yaxis=dict(
    		range=(0, 1)),
    	xaxis=dict(
    		constrain="domain"))
    return fig

def set_color(latest_value):
	if latest_value is 0:
		return "#32CD32"
	else:
		return "#FF0000"

# OVERVIEW GRAPH
@app.callback(Output('overview-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
	devices_on = 0
	for key, value in ecosystem_status.items():
		# print(key, value)
		if value == 1:
			devices_on += 1
	overview_devices_on.append(devices_on)
	overview_smartflow_status.append(int(ecosystem_status['smartflow_status']))

    # Create the graph with subplots
	fig = plotly.subplots.make_subplots(
        rows=3, cols=10,
        specs=[[{'type': 'domain', "colspan": 3, "rowspan": 3}, None, None, {"colspan": 6}, None, None, None, None, None, None],
        		[None, None, None, {"colspan": 6, "rowspan": 2}, None, None, None, None, None, None],
        		[None, None, None, None, None, None, None, None, None, None]],
        subplot_titles=("", "Status", "Active Devices", "", "", "", "", "", "", "",
        				"", "", "", "", "", "", "", "", "", ""),
        shared_xaxes=True)
	fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 0, 't': 50
    }
	fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': -0.01,
                               'y': 1
                               }
	device_bar = go.Bar(
                	x=list(overview_times),
                	y=list(overview_devices_on),
                	name='Devices Active',
                	text=list(overview_devices_on),
                	textposition='outside',
                	marker=dict(color='#0000FF'))
	labels=['Anomalous', 'Normal']
	normal = 0
	anomalous = 0
	for entry in list(overview_smartflow_status):
		if entry is 0:
			normal += 1
		elif entry is 1:
			anomalous += 1
	print(list(overview_smartflow_status))
	values = [anomalous, normal]
	
	colors=['#FF0000', '#32CD32']
	system_pie = go.Pie(
					labels=labels,
					hole=.3,
					values=values,
					hoverinfo='label+percent',
					marker=dict(colors=colors))

	fig.append_trace({
		'x': list(overview_times),
		'y': list(overview_smartflow_status),
		'yaxis': 'y2',
		'name': 'Smartflow Status',
		'mode': 'markers+lines',
		'fill': 'tozeroy',
		'marker' : dict(size=15,
    					color=(set_color(list(overview_smartflow_status)[len(list(overview_smartflow_status))-1]))),
    	'type': 'scatter',	
	}, 1, 4)
	fig.append_trace(system_pie, 1, 1)
	fig.append_trace(device_bar, 2, 4)
	
	fig.update_layout(title_text='[---OVERVIEW---]', font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#C2C5CC',
    	plot_bgcolor='#C2C5CC', 
    	height=500,
    	yaxis=dict(range=(0, 1)),
    	yaxis2=dict(range=(0, 10)))
	return fig
################################ END OF DASHBOARD LAYOUT ################################


app.run_server(debug=True)
