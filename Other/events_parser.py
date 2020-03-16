import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random

from elasticsearch import Elasticsearch
import json
from time import sleep
import requests
from bs4 import BeautifulSoup

from elasticsearch import Elasticsearch, RequestsHttpConnection
import datetime
import re

test_data = [
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'crQXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T16:59:47.651Z', 'window_sensor': 0, 'time': '11:08:32.704', 'light_2': 1,
                 'motion_sensor': 0, 'ecs': {'version': '1.4.0'}, 'door_sensor': 0,
                 'error': {'message': "Key 'log' not found", 'type': 'json'}, 'light_1': 1, 'light_3': 1,
                 'date': '2020-02-05',
                 'log': {'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}, 'offset': 71484},
                 'input': {'type': 'log'}, 'host': {'name': 'Corelee-Laptop'},
                 'agent': {'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6', 'hostname': 'Corelee-Laptop',
                           'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a', 'version': '7.6.0', 'type': 'filebeat'}}},
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'c7QXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T16:59:52.651Z', 'light_1': 1, 'ecs': {'version': '1.4.0'},
                 'log': {'offset': 71643, 'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}},
                 'light_2': 1, 'window_sensor': 0, 'error': {'type': 'json', 'message': "Key 'log' not found"},
                 'motion_sensor': 1, 'time': '11:08:36.810',
                 'agent': {'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a', 'version': '7.6.0', 'type': 'filebeat',
                           'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6', 'hostname': 'Corelee-Laptop'},
                 'door_sensor': 0, 'light_3': 1, 'input': {'type': 'log'}, 'host': {'name': 'Corelee-Laptop'},
                 'date': '2020-02-05'}},
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'dLQXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T16:59:57.651Z', 'date': '2020-02-05', 'input': {'type': 'log'},
                 'log': {'offset': 71802, 'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}},
                 'light_1': 1, 'motion_sensor': 0, 'time': '11:09:10.153', 'window_sensor': 0,
                 'ecs': {'version': '1.4.0'}, 'error': {'message': "Key 'log' not found", 'type': 'json'}, 'light_2': 1,
                 'host': {'name': 'Corelee-Laptop'},
                 'agent': {'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6', 'hostname': 'Corelee-Laptop',
                           'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a', 'version': '7.6.0', 'type': 'filebeat'},
                 'light_3': 1, 'door_sensor': 0}},
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'dbQXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T17:00:02.651Z', 'light_2': 1, 'motion_sensor': 1, 'light_3': 1,
                 'log': {'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}, 'offset': 71961},
                 'host': {'name': 'Corelee-Laptop'}, 'window_sensor': 0,
                 'error': {'message': "Key 'log' not found", 'type': 'json'}, 'light_1': 1, 'date': '2020-02-05',
                 'ecs': {'version': '1.4.0'}, 'time': '11:09:24.512', 'input': {'type': 'log'}, 'door_sensor': 0,
                 'agent': {'type': 'filebeat', 'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6',
                           'hostname': 'Corelee-Laptop', 'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a',
                           'version': '7.6.0'}}},
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'drQXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T17:00:07.651Z',
                 'log': {'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}, 'offset': 72120},
                 'window_sensor': 0, 'input': {'type': 'log'}, 'light_2': 1, 'light_3': 1,
                 'host': {'name': 'Corelee-Laptop'}, 'ecs': {'version': '1.4.0'},
                 'error': {'type': 'json', 'message': "Key 'log' not found"}, 'light_1': 1, 'door_sensor': 0,
                 'motion_sensor': 0, 'date': '2020-02-05', 'time': '11:10:34.310',
                 'agent': {'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6', 'hostname': 'Corelee-Laptop',
                           'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a', 'version': '7.6.0', 'type': 'filebeat'}}},
    {'_index': 'filebeat-7.6.0-2020.02.17-000001', '_type': '_doc', '_id': 'd7QXVHABxSfDv-iv3Yu4', '_score': 1.0,
     '_source': {'@timestamp': '2020-02-26T17:00:12.651Z', 'motion_sensor': 1, 'light_3': 1, 'date': '2020-02-05',
                 'ecs': {'version': '1.4.0'},
                 'agent': {'id': '52e4386a-d2f0-471b-a145-f69cf5471a3a', 'version': '7.6.0', 'type': 'filebeat',
                           'ephemeral_id': '55e455af-bd36-49aa-a24e-8199b5b1aea6', 'hostname': 'Corelee-Laptop'},
                 'door_sensor': 0, 'input': {'type': 'log'}, 'light_2': 1, 'light_1': 1,
                 'log': {'offset': 72279, 'file': {'path': '/home/corelee/Desktop/coen490/events_log.log'}},
                 'window_sensor': 0, 'host': {'name': 'Corelee-Laptop'},
                 'error': {'type': 'json', 'message': "Key 'log' not found"}, 'time': '11:10:35.338'}}
]


class elastic_agent:
    es = None

    def __init__(self, ip='127.0.0.1', port=9200):
        """
            ip : is the ip address of elasticsearch on cluster, type str
            port: is the elasticsearch port in cluster, the default port is 9200, type int
        """

        try:
            # Setup the connection ip address
            self.es = Elasticsearch([{'host': ip, 'port': port}])
            print(self.es.info())
            print("\nEleasticsearch running ....")
        except:
            print("Fail to connect to elasticsearch ....")

    def search(self):

        # print(datetime.datetime.now(datetime.timezone.utc))
        # print("2020-02-26 16:59:42.726522+00:00")
        # print("2020-02-26T17:00:12.651Z")
        test_date_time = "2020-02-17 10:59:42.726522+00:00"

        es_structured_date_time = re.match(r'(.*) (.*)', test_date_time)
        # print(es_structured_date_time.group(1))
        # print(es_structured_date_time.group(2))
        es_structured_time = es_structured_date_time.group(2)[:12] + "Z"
        es_structured_date_time = es_structured_date_time.group(1) + "T" + es_structured_time
        print(es_structured_date_time)
        lastest_timestamp = ""
        res = self.es.search(index="filebeat-7.6.0-2020.02.17-000001",
                             body={"query": {
                                 "range": {
                                     "@timestamp": {
                                         "gte": es_structured_date_time
                                     }
                                 }
                             }, 'size': 10000
                             })
        for hit in res['hits']['hits']:
            print(hit)
            lastest_timestamp = hit['_source']['@timestamp']
            try:
                print(hit['_source']['@timestamp'], hit['_source']['light_1'], hit['_source']['light_2'],
                      hit['_source']['light_3'], hit['_source']['door_sensor'], hit['_source']['window_sensor'],
                      hit['_source']['motion_sensor'])
            except:
                print("Value not found!")
        print(lastest_timestamp)

    def check_index(self, index):
        """
            index = index that you want to check if it is in cluster or not, type str
            return value boolean
        """
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


def dummy_es_response():
    return_dict = {
        "light_1": random.randrange(0, 1),
        "light_2": random.randrange(0, 1),
        "light_3": random.randrange(0, 1),
        "door_sensor": random.randrange(0, 1),
        "window_sensor": random.randrange(0, 1),
        "motion_sensor": random.randrange(0, 1)
    }
    return return_dict


# elastic_agent007 = elastic_agent()
# elastic_agent007.search()

################################################# DASH #################################################################
"""try:
	r = requests.get(u, headers=headers)

if r.status_code == 200:
	print("200")"""

max_length = 20
times = deque(maxlen=max_length)
test_temp = deque(maxlen=max_length)
test_temp2 = deque(maxlen=max_length)
other_test_temp = deque(maxlen=max_length)


data_dict = {"Test Temperature": test_temp,
             "Test Temperature 2" : test_temp2,
             "Other Test Temp": other_test_temp}


def update_obd_values(times, test_temp, test_temp2, other_test_temp):
    times.append(time.time())
    if len(times) == 1:
        # starting relevant values
        test_temp.append(random.randrange(10, 150))
        test_temp2.append(random.randrange(10, 150))
        other_test_temp.append(random.randrange(10, 150))
    else:
        for data_of_interest in [test_temp, test_temp2, other_test_temp]:
            data_of_interest.append(random.randrange(10, 150))

    return times, test_temp, test_temp2, other_test_temp


times, test_temp, test_temp2, other_test_temp = update_obd_values(times, test_temp, test_temp2, other_test_temp)

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

], className="container", style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000})


# Updater function
@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('test-data-name', 'value'),
     dash.dependencies.Input('graph-update', 'n_intervals')],
)
def update_graph(data_names, n):
    graphs = []
    update_obd_values(times, test_temp, test_temp2, other_test_temp)
    if len(data_names) > 2:
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
        data2 = go.Bar(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Bar',
        )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data, data2], 'layout': go.Layout(
                                                        xaxis=dict(range=[min(times), max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),
                                                                          max(data_dict[data_name])]),
                                                        yaxis2=dict(range=[min(data_dict[data_name],
                                                                               max(data_dict[data_name]))]),
                                                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                                                        title='{}'.format(data_name))}
        ), className=class_choice))

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)
