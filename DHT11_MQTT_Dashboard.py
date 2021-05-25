#***********************************************************************
# @file
#
# Python script for visualizing DHT11 sensor temperature and humidity
# readings for Buffalo Grove. The readings are obtained via MQTT 
# subscriptions.
#
# @note None
#
# @warning  None
#
#  Created: May 24, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import datetime
import pandas as pd
import paho.mqtt.client as mqtt
import plotly
import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

sensor_data_time = []
sensor_data_temperature = []
sensor_data_humidity = []

token = open(".mapbox_token").read() 

figure0_1 = go.Figure(go.Scattermapbox(
    mode = "markers+text+lines",
    lon = [-87.961640], lat = [42.152030],
    marker = {'size': 20, 'symbol': ["car"]},
    text = ["Transportation"],textposition = "bottom right"))

figure0_1.update_layout(
    title='Buffalo Grove - Illinois',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=token,
        bearing=0,
        center=dict(
            lat=42.152030,
            lon=-87.961640
        ),
        pitch=0,
        zoom=20,
        style='satellite-streets'
    ),
)

figure0_1.show()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print()

def on_message_temperature(mqttc, obj, msg):
    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Temperature
    print("Temperature: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
        
    # In order to be able to assign to the global name, we need to tell 
    # the parser to use the global name rather than bind a new local name
    # - which is what the 'global' keyword does.
    sensor_data_time.append(datetime.datetime.now())
    sensor_data_temperature.append(float(msg.payload))

def on_message_humidity(mqttc, obj, msg):
    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Humidity
    print("Humidity: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()

    # In order to be able to assign to the global name, we need to tell 
    # the parser to use the global name rather than bind a new local name
    # - which is what the 'global' keyword does.    
    sensor_data_humidity.append(float(msg.payload))

    print('Debug -> Time:')
    print(sensor_data_time)
    print()
    print('Debug -> Temperature:')
    print(sensor_data_temperature)
    print()
    print('Debug -> Humidity:')
    print(sensor_data_humidity)
    print()

    # Create the graph with subplots
    figure2 = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    figure2['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    figure2['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    figure2.append_trace({
        'x': sensor_data_time,
        'y': sensor_data_temperature,
        'name': 'DHT11 Temperature Readings',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    figure2.append_trace({
        'x': sensor_data_time,
        'y': sensor_data_humidity,
        'text': sensor_data_time, # TBD, Nuertey Odzeyem, is this line really needed?
        'name': 'DHT11 Humidity Readings',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    
    figure2.show()

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    print()

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    print()

def on_log(mqttc, obj, level, string):
    print(string)
    print()

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("/Nuertey/Nucleo/F767ZI/Temperature", on_message_temperature)
mqttc.message_callback_add("/Nuertey/Nucleo/F767ZI/Humidity", on_message_humidity)

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("10.50.10.25", 1883, 60)
mqttc.subscribe("/Nuertey/Nucleo/F767ZI/#", 0)
mqttc.loop_forever()
