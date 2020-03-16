import datetime
import json
import random
import time
from collections import deque
import requests
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

from elasticsearch import Elasticsearch, RequestsHttpConnection
from bs4 import BeautifulSoup

ecosystem_status = {
	'light_1': "0",
    'light_2': "0",
    'light_3': "0",
    'motion_sensor_1': "0",
    'motion_sensor_2': "0",
    'motion_sensor_3': "0",
    'motion_sensor_4': "0",
    'door_sensor': "0",
    'window_sensor': "0",
    'smartflow_status': "0",
    'timestamp': "0"
}

max_length = 20
times = deque(maxlen=max_length)

# Room 1 devices
light_1 = deque(maxlen=max_length)
motion_sensor_1 = deque(maxlen=max_length)
door_sensor = deque(maxlen=max_length)

# Room 2 devices
light_2 = deque(maxlen=max_length)
motion_sensor_2 = deque(maxlen=max_length)

# Room 3 devices
light_3 = deque(maxlen=max_length)
motion_sensor_3 = deque(maxlen=max_length)

# Room 4 devices
#light_4 = deque(maxlen=max_length)
motion_sensor_4 = deque(maxlen=max_length)
window_sensor = deque(maxlen=max_length)

external_stylesheets = ['/home/corelee/Desktop/winter2020/coen490/SMARTFLOW/stylesheet/smartflow_dashboard_css.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = {
    'light_1': light_1,
    'light_2': light_2,
    'light_3': light_3,
    #'light_4': light_4,
    'motion_sensor_1': motion_sensor_1,
    'motion_sensor_2': motion_sensor_2,
    'motion_sensor_3': motion_sensor_3,
    'motion_sensor_4': motion_sensor_4,
    'door_sensor': door_sensor,
    'window_sensor': window_sensor
}

app.layout = html.Div(
    html.Div([
        html.H4('SMARTFLOW Dashboard'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 3000,  # in milliseconds
            n_intervals=0
        )
    ], style={'textAlign': 'center'})
)

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # print(time.time())
    times.append(datetime.datetime.now())
    if len(times) == 1:
        # Room 1; KITCHEN
        light_1.append(ecosystem_status['light_1'])
        motion_sensor_1.append(ecosystem_status['motion_sensor_1'])
        window_sensor.append(ecosystem_status['window_sensor'])

        # Room 2; OFFICE
        light_2.append(ecosystem_status['light_2'])
        motion_sensor_2.append(ecosystem_status['motion_sensor_2'])

        # Room 3; LIVING ROOM
        door_sensor.append(ecosystem_status['door_sensor'])
        motion_sensor_3.append(ecosystem_status['motion_sensor_3'])

        # Room 4; BEDROOM
        light_3.append(ecosystem_status['light_3'])
        motion_sensor_4.append(ecosystem_status['motion_sensor_4'])

    else:
        # Room 1; KITCHEN
        light_1.append(ecosystem_status['light_1'])
        motion_sensor_1.append(ecosystem_status['motion_sensor_1'])
        window_sensor.append(ecosystem_status['window_sensor'])

        # Room 2; OFFICE
        light_2.append(ecosystem_status['light_2'])
        motion_sensor_2.append(ecosystem_status['motion_sensor_2'])

        # Room 3; LIVING ROOM
        door_sensor.append(ecosystem_status['door_sensor'])
        motion_sensor_3.append(ecosystem_status['motion_sensor_3'])

        # Room 4; BEDROOM
        light_3.append(ecosystem_status['light_3'])
        motion_sensor_4.append(ecosystem_status['motion_sensor_4'])

    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(rows=4, cols=2, vertical_spacing=0.05)
    fig['layout']['margin'] = {
        'l': 100, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'orientation': 'v',
                               'borderwidth': 2,
                               'x': 0.5,
                               'y': 1
                               }

    # Room 1; KITCHEN
    fig.append_trace({
        'x': list(times),
        'y': list(data['light_1']),
        # 'text': list(times),
        'name': 'Light 1',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_1']),
        # 'text': list(times),
        'name': 'Kitchen Motion Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['window_sensor']),
        # 'text': list(times),
        'name': 'Window Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    # Room 2; OFFICE
    fig.append_trace({
        'x': list(times),
        'y': list(data['light_2']),
        'text': list(times),
        'name': 'Light 2',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_2']),
        'text': list(times),
        'name': 'Office Motion Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    # Room 3; LIVING ROOM
    fig.append_trace({
        'x': list(times),
        'y': list(data['door_sensor']),
        'text': list(times),
        'name': 'Door Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_3']),
        'text': list(times),
        'name': 'Living Room Motion Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)

    # Room 4
    # fig.append_trace({
    #     'x': list(times),
    #     'y': list(data['light_4']),
    #     'text': list(times),
    #     'name': 'Light 4',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, 4, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_4']),
        'text': list(times),
        'name': 'Bedroom Motion Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['light_3']),
        'text': list(times),
        'name': 'Bedroom Light',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)

    fig.update_layout(height=800)

    return fig


class ElasticAgentThread(threading.Thread):
	def __init__(self, _elastic_agent):
		threading.Thread.__init__(self)
		self.elastic_agent = _elastic_agent
	def run(self):
		while True:
			self.elastic_agent.search()
			time.sleep(3)

class elastic_agent:
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
            self.es.indices.refresh(index="filebeat-7.6.0-2020.02.17-000001")


        except:
            print("Fail to connect to elasticsearch ....")

    def search(self):
        res = self.es.search(index="filebeat-7.6.0-2020.02.17-000001",
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
        ecosystem_status['timestamp'] = smartflow_ecosystem_dict['@timestamp'][:19]
        ecosystem_status['light_1'] = smartflow_ecosystem_dict['light_1']
        ecosystem_status['light_2'] = smartflow_ecosystem_dict['light_2']
        ecosystem_status['light_3'] = smartflow_ecosystem_dict['light_3']
        ecosystem_status['motion_sensor_1'] = smartflow_ecosystem_dict['motion_sensor_1']
        ecosystem_status['window_sensor'] = smartflow_ecosystem_dict['window_sensor']
        ecosystem_status['door_sensor'] = smartflow_ecosystem_dict['door_sensor']
        ecosystem_status['smartflow_status'] = smartflow_ecosystem_dict['smartflow_status']       
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


elastic_agent007 = elastic_agent()
elastic_agent_thread = ElasticAgentThread(elastic_agent007)
elastic_agent_thread.start()

app.run_server(debug=True)

# while True:
# 	elastic_agent007.search()
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
