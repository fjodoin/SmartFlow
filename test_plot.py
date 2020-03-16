import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import random
from collections import deque
import time

# pip install pyorbital
# from pyorbital.orbital import Orbital

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
light_4 = deque(maxlen=max_length)
motion_sensor_4 = deque(maxlen=max_length)
window_sensor = deque(maxlen=max_length)

external_stylesheets = ['/home/corelee/Desktop/winter2020/coen490/SMARTFLOW/stylesheet/smartflow_dashboard_css.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = {
    'light_1': light_1,
    'light_2': light_2,
    'light_3': light_3,
    'light_4': light_4,
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
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
    ], style={'textAlign': 'center'})
)


# @app.callback(Output('live-update-text', 'children'),
#               [Input('interval-component', 'n_intervals')])
# def update_metrics(n):
#     l1, l2, l3, l4, ds, ws, ms1, ms2, ms3, ms4 = 1, 0, 0, 1, 0, 0, 1, 0, 0, 0
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         html.Span('Light 1: {0:.2f}'.format(l1), style=style),
#         # html.Span('Light 2: {0:.2f}'.format(l2), style=style),
#         # html.Span('Light 3: {0:0.2f}'.format(l3), style=style),
#         # html.Span('Light 4: {0:0.2f}'.format(l3), style=style),
#         html.Span('Door Sensor: {0:0.2f}'.format(ds), style=style),
#         # html.Span('Window Sensor: {0:0.2f}'.format(ws), style=style),
#         html.Span('Motion Sensor 1: {0:0.2f}'.format(ms1), style=style),
#         # html.Span('Motion Sensor 2: {0:0.2f}'.format(ms2), style=style),
#         # html.Span('Motion Sensor 3: {0:0.2f}'.format(ms3), style=style),
#         # html.Span('Motion Sensor 4: {0:0.2f}'.format(ms4), style=style)
#     ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    print(time.time())
    times.append(time.time())
    if len(times) == 1:
        # Room 1
        light_1.append(random.randrange(0, 3))
        motion_sensor_1.append(random.randrange(0, 3))
        door_sensor.append(random.randrange(0, 3))

        # Room 2
        light_2.append(random.randrange(0, 3))
        motion_sensor_2.append(random.randrange(0, 3))

        # Room 3
        light_3.append(random.randrange(0, 3))
        motion_sensor_3.append(random.randrange(0, 3))

        # Room 4
        light_3.append(random.randrange(0, 3))
        motion_sensor_3.append(random.randrange(0, 3))
        window_sensor.append(random.randrange(0, 3))

    else:
        for data_of_interest in [light_1, motion_sensor_1, door_sensor,
                                 light_2, motion_sensor_2,
                                 light_3, motion_sensor_3,
                                 light_4, motion_sensor_4, window_sensor]:
            data_of_interest.append(random.randrange(0, 3))

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

    # Room 1
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
        'name': 'Motion Sensor 1',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['door_sensor']),
        # 'text': list(times),
        'name': 'Door Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    # Room 2
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
        'name': 'Motion Sensor 2',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    # Room 3
    fig.append_trace({
        'x': list(times),
        'y': list(data['light_3']),
        'text': list(times),
        'name': 'Light 3',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_3']),
        'text': list(times),
        'name': 'Motion Sensor 3',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)

    # Room 4
    fig.append_trace({
        'x': list(times),
        'y': list(data['light_4']),
        'text': list(times),
        'name': 'Light 4',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['motion_sensor_4']),
        'text': list(times),
        'name': 'Motion Sensor 4',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)
    fig.append_trace({
        'x': list(times),
        'y': list(data['window_sensor']),
        'text': list(times),
        'name': 'Window Sensor',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)

    fig.update_layout(height=800)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
