import datetime
import json
import random
import time
from collections import deque
import requests
import threading
import numpy
import pandas

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

from elasticsearch import Elasticsearch, RequestsHttpConnection
from bs4 import BeautifulSoup


ecosystem_status = {
	# KITCHEN
	'kitchen_light': "0",
    'kitchen_motion_sensor': "0",
    'kitchen_door_sensor': "0",
    'kitchen_temperature': "0",
    
    # OFFICE
    'office_light': "0",
    'office_motion_sensor': "0",
    'office_temperature': "0",
    
    # LIVING ROOM
    'living_room_light': "0",
    'living_room_motion_sensor': "0",
    'living_room_door_sensor': "0",
    'living_room_temperature': "0",
    
    # BEDROOM
    'bedroom_light' : "0",
    'bedroom_motion_sensor': "0",
    'bedroom_temperature': "0",

    'smartflow_status': "0",
    'timestamp': "0"
}

max_length = 20
temperature_max_length = 1
times = deque(maxlen=max_length)

# KITCHEN devices
kitchen_light = deque(maxlen=max_length)
kitchen_motion_sensor = deque(maxlen=max_length)
kitchen_door_sensor = deque(maxlen=max_length)
kitchen_temperature = deque(maxlen=temperature_max_length)

# OFFICE devices
office_light = deque(maxlen=max_length)
office_motion_sensor = deque(maxlen=max_length)

# LIVING ROOM devices
living_room_light = deque(maxlen=max_length)
living_room_motion_sensor = deque(maxlen=max_length)
living_room_door_sensor = deque(maxlen=max_length)

# BEDROOM devices
bedroom_light = deque(maxlen=max_length)
bedroom_motion_sensor = deque(maxlen=max_length)

app = dash.Dash(__name__)

data = {
    # Room 1; KITCHEN
    'kitchen_light': kitchen_light,
    'kitchen_motion_sensor': kitchen_motion_sensor,
    'kitchen_door_sensor': kitchen_door_sensor,
    'kitchen_temperature' : kitchen_temperature,
    # Room 2; OFFICE
    'office_light': office_light,
    'office_motion_sensor': office_motion_sensor,
    
    # Room 3; LIVING ROOM
    'living_room_light': living_room_light,
    'living_room_motion_sensor': living_room_motion_sensor,
    'living_room_door_sensor': living_room_door_sensor,
    
    # Room 4; BEDROOM
    'bedroom_light': bedroom_light,
    'bedroom_motion_sensor': bedroom_motion_sensor,
}

app.layout = html.Div(
    html.Div([
        html.H4('SMARTFLOW Dashboard'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='kitchen-graph'),
        dcc.Graph(id='office-graph'),
        dcc.Graph(id='living-room-graph'),
        dcc.Graph(id='bedroom-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1500,  # in milliseconds
            n_intervals=0
        )
    ], style={'textAlign': 'center'})
)


# KITCHEN GRAPH
@app.callback(Output('kitchen-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    times.append(datetime.datetime.now())
    # Room 1; KITCHEN
    kitchen_light.append(ecosystem_status['kitchen_light'])
    kitchen_motion_sensor.append(ecosystem_status['kitchen_motion_sensor'])
    kitchen_door_sensor.append(ecosystem_status['kitchen_door_sensor'])
    counter = 0
    if (counter % 2) == 0:
    	kitchen_temperature.append(str(ecosystem_status['kitchen_temperature']) + "°C")
    	counter += 1

    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(
    	rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, {"colspan": 2}, None, None, None]],
    	subplot_titles=("[-KITCHEN-]", "temperature: °C", "", "", "", "", "", "", "", ""))
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
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['kitchen_motion_sensor']),
        'name': 'Motion Sensor',
        'mode': 'lines+markers',
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)
    fig.append_trace({
        'x': list(times),
        'y': list(data['kitchen_door_sensor']),
        'name': 'Door Sensor',
        'mode': 'lines+markers',
        'type': 'scatter',
        'opacity': 0.5,
        'fill': 'tozeroy'
    }, 1, 2)
    fig.append_trace({
    	'x': list(times),
    	'y': list(data['kitchen_temperature']),
    	'text': list(data['kitchen_temperature']),
    	'textposition': 'top center',
    	'name': 'Temperature',
    	'mode': 'markers+text',
    	'marker' : dict(size=25),
    	'type': 'scatter'
    }, 1, 7)

    fig.update_layout(
    	font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#DBDBDB',
    	plot_bgcolor='#DBDBDB', 
    	height=250)
    return fig

# OFFICE GRAPH
@app.callback(Output('office-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
	# Room 2; OFFICE
    office_light.append(ecosystem_status['office_light'])
    office_motion_sensor.append(ecosystem_status['office_motion_sensor'])

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
    	rows=1, cols=10,
    	specs=[[None, {"colspan": 4}, None, None, None, None, None, None, None, None]],
    	subplot_titles=("[-OFFICE-]", "", "", "", "", "", "", "", "", ""))
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
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)

    fig.update_layout(font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#D4DCF2',
    	plot_bgcolor='#D4DCF2', 
    	height=250)
    return fig

# LIVING ROOM GRAPH
@app.callback(Output('living-room-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n): 
	# Room 3; LIVING ROOM
    living_room_light.append(ecosystem_status['living_room_light'])
    living_room_motion_sensor.append(ecosystem_status['living_room_motion_sensor'])
    living_room_door_sensor.append(ecosystem_status['living_room_door_sensor'])

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
        rows=1, cols=10,
        specs=[[None, {"colspan": 4}, None, None, None, None, None, None, None, None]],
        subplot_titles=("[-LIVING ROOM-]", "", "", "", "", "", "", "", "", ""))
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
        'type': 'scatter',
        'opacity': 0.5,
        'fill': 'tozeroy'
    }, 1, 2)

    fig.update_layout(font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#DBDBDB',
    	plot_bgcolor='#DBDBDB', 
    	height=250)
    return fig

# BEDROOM GRAPH
@app.callback(Output('bedroom-graph', 'figure'),
				[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
	    # Room 4; BEDROOM
    bedroom_light.append(ecosystem_status['bedroom_light'])
    bedroom_motion_sensor.append(ecosystem_status['bedroom_motion_sensor'])

	# Create the graph with subplots
    fig = plotly.subplots.make_subplots(
        rows=1, cols=10,
        specs=[[None, {"colspan": 4}, None, None, None, None, None, None, None, None]],
        subplot_titles=("[-BEDROOM-]", "", "", "", "", "", "", "", "", ""))
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
        'type': 'scatter',
        'fill': 'tozeroy',
        'line': {'dash': 'dashdot'}
    }, 1, 2)

    fig.update_layout(font=dict(family='Courier New, monospace',color='#1A1A1A'),
    	paper_bgcolor='#D4DCF2',
    	plot_bgcolor='#D4DCF2', 
    	height=250)
    return fig


class ElasticAgentThread(threading.Thread):
	def __init__(self, _elastic_agent):
		threading.Thread.__init__(self)
		self.ElasticAgent = _elastic_agent
	def run(self):
		while True:
			self.ElasticAgent.search()
			time.sleep(1)

class ElasticAgent:
    es = None

    def __init__(self, ip='127.0.0.1', port=9200):
        '''
            ip : is the ip address of elasticsearch on cluster, type str
            port: is the elasticsearch port in cluster, the defaulte port is 9200, type int
        '''

        try:
            # Setup the connection ip address
            self.es = Elasticsearch([{'host': ip, 'port': port}])
            #print(self.es.info())
            print("\nEleasticsearch running ....")
            # NOTE: the INDEX name below changes to the date modifications are made to the /etc/filebeat/filebeat.yml file
            self.es.indices.refresh(index="filebeat-7.6.1-2020.03.16-000001")


        except:
            print("Fail to connect to elasticsearch ....")

    def search(self):
    	# NOTE: the INDEX name below changes to the date modifications are made to the /etc/filebeat/filebeat.yml file
        res = self.es.search(index="filebeat-7.6.1-2020.03.16-000001",
                             body={"size" : 10,
                             			"sort": [
                             					{"@timestamp": {"order": "desc"}}
                             			],
                             			"query": {"match_all" : {}}
                             	})
        
        # print(res)

        # print(type(res))
        hits = res['hits']['hits']
        # print(type(hits))
        # for entry in hits:
        # 	print(entry['_source']['@timestamp'], entry['_source']['']"\n")
        
## STATUS PART
        
        smartflow_ecosystem_dict = hits[0]['_source']
        
        # STATUS
        ecosystem_status['smartflow_status'] = hits[0]['_source']['smartflow_status']       
        
        # TIMESTAMP
        ecosystem_status['timestamp'] = hits[0]['_source']['@timestamp'][:19]

        # TEMPERATURE SENSORS
        ecosystem_status['kitchen_temperature'] = hits[0]['_source']['kitchen_temperature']

        # DOOR SENSORS
        ecosystem_status['kitchen_door_sensor'] = hits[0]['_source']['kitchen_door_sensor']
        ecosystem_status['living_room_door_sensor'] = hits[0]['_source']['living_room_door_sensor']
        
        # LIGHT & MOTION SENSORS
        if hits[0]['_source']['kitchen_motion_sensor'] is 1:
        	ecosystem_status['kitchen_light'] = 1
        	ecosystem_status['kitchen_motion_sensor'] = 1
        	ecosystem_status['office_light'] = 0
        	ecosystem_status['office_motion_sensor'] = 0
        	ecosystem_status['living_room_light'] = 0
        	ecosystem_status['living_room_motion_sensor'] = 0
        	ecosystem_status['bedroom_light'] = 0
        	ecosystem_status['bedroom_motion_sensor'] = 0
        elif hits[0]['_source']['office_motion_sensor'] is "1":
        	ecosystem_status['kitchen_light'] = 0
        	ecosystem_status['kitchen_motion_sensor'] = 0
        	ecosystem_status['office_light'] = 1
        	ecosystem_status['office_motion_sensor'] = 1
        	ecosystem_status['living_room_light'] = 0
        	ecosystem_status['living_room_motion_sensor'] = 0
        	ecosystem_status['bedroom_light'] = 0
        	ecosystem_status['bedroom_motion_sensor'] = 0
        elif hits[0]['_source']['living_room_motion_sensor'] is "1":
        	ecosystem_status['kitchen_light'] = 0
        	ecosystem_status['kitchen_motion_sensor'] = 0
        	ecosystem_status['office_light'] = 0
        	ecosystem_status['office_motion_sensor'] = 0
        	ecosystem_status['living_room_light'] = 1
        	ecosystem_status['living_room_motion_sensor'] = 1
        	ecosystem_status['bedroom_light'] = 0
        	ecosystem_status['bedroom_motion_sensor'] = 0
        elif hits[0]['_source']['bedroom_motion_sensor'] is "1":
        	ecosystem_status['kitchen_light'] = 0
        	ecosystem_status['kitchen_motion_sensor'] = 0
        	ecosystem_status['office_light'] = 0
        	ecosystem_status['office_motion_sensor'] = 0
        	ecosystem_status['living_room_light'] = 0
        	ecosystem_status['living_room_motion_sensor'] = 0
        	ecosystem_status['bedroom_light'] = 1
        	ecosystem_status['bedroom_motion_sensor'] = 1
        else:


        	# KITCHEN
        	ecosystem_status['kitchen_light'] = hits[0]['_source']['kitchen_light']
        	ecosystem_status['kitchen_motion_sensor'] = hits[0]['_source']['kitchen_motion_sensor']
        
        	# OFFICE
        	ecosystem_status['office_light'] = hits[0]['_source']['office_light']
        	ecosystem_status['office_motion_sensor'] = hits[0]['_source']['office_motion_sensor']

        	# LIVING ROOM
        	ecosystem_status['living_room_light'] = hits[0]['_source']['living_room_light']
        	ecosystem_status['living_room_motion_sensor'] = hits[0]['_source']['living_room_motion_sensor']        

        	# BEDROOM
        	ecosystem_status['bedroom_light'] = hits[0]['_source']['bedroom_light']
        	ecosystem_status['bedroom_motion_sensor'] = hits[0]['_source']['bedroom_motion_sensor']        
        
        
        # print("##############################################")
        # for key, value in smartflow_ecosystem_dict.items():
        # 	print(key, value)
##


        	# for key, value in entry['_source'].items():
        	# 	print(key, value)
        # print(res['hits']['hits'])
        # print("res")
        # print("Got %d Hits:" & res['hits']['total']['value'])
        # for hit in res['hits']['hits']:
        #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    def check_index(self, index):
        '''
            index = index that you want to check if it is in cluster or not, type str
            return value boolean
        '''
        if self.es.indices.exists(index=index):
            print('{} is already created ...'.format(index))
            return True
        else:
            print('index {} not found, please create new index ...'.format(index))
            return False

    def create_index(self, index):
        if index == None or len(index.strip()) <= 1:
            return False
        request_body = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 2
            },
        }
        response = self.es.indices.create(index=index, body=request_body, ignore=400)
        print(response)

    def delete_index(self, index):
        if index == None or len(index.strip()) <= 1:
            return False
        response = self.es.indices.delete(index=index)
        print(response)

    def add_document(self, index, document, id, type='doc'):
        res = self.es.index(index=index, doc_type=type, id=id, body=document)
        if res['result']:
            print('Document added successfully ...')
        else:
            print('Fail add document id {}'.format(str(id)))

    def edit_document(self, index, document, id, type='doc'):
        res = self.es.update(index=index, doc_type=type, id=id, body={"doc": document})

        if res['result']:
            print('Document updated successfully ...')
        else:
            print('Fail updated document id {}'.format(str(id)))

    def get_document(self, index, id, type='doc'):
        try:
            res = self.es.get(index=index, doc_type=type, id=id)
            print(res)
            return res
        except:
            return {}

    def delete_document(self, index, id, type='doc'):
        res = self.es.delete(index=index, doc_type=type, id=id)
        print(res['result'])


elastic_agent = ElasticAgent()
elastic_agent_thread = ElasticAgentThread(elastic_agent)
elastic_agent_thread.start()

app.run_server(debug=True)

# while True:
# 	elastic_agent.search()
# 	time.sleep(3)

"""try:
	r = requests.get(u, headers=headers)

if r.status_code == 200:
	print("200")"""

"""
max_length = 20
times = deque(maxlen=max_length)
test_temp = deque(maxlen=max_length)
other_test_temp = deque(maxlen=max_length)

data_dict = {"Test Temperature": test_temp,
			"Other Test Temp" : other_test_temp}


def update_obd_values(times, test_temp, other_test_temp):
    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        test_temp.append(random.randrange(10,150))
        other_test_temp.append(random.randrange(10,150))
    else:
        for data_of_interest in [test_temp, other_test_temp]:
            data_of_interest.append(random.randrange(10,150))

    return times, test_temp, other_test_temp


times, test_temp, other_test_temp = update_obd_values(times, test_temp, other_test_temp)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

app = dash.Dash('test-data',
                external_scripts=external_js,
                external_stylesheets=external_css)

app.layout = html.Div([
    html.Div([
        html.H2('Test Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='test-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Test Temperature'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0),

    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

# Updater function
@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('test-data-name', 'value'),
     dash.dependencies.Input('graph-update', 'n_intervals')],
    )
def update_graph(data_names, n):
    graphs = []
    update_obd_values(times, test_temp, other_test_temp)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)
"""
