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
first_time = True

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
        zoom=15,
        style='satellite-streets'
    ),
)

figure0_1.show()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print()

def on_message_temperature(mqttc, obj, msg):
    # In order to be able to assign to the global name, we need to tell 
    # the parser to use the global name rather than bind a new local name
    # - which is what the 'global' keyword does.
    global sensor_data_time
    global sensor_data_temperature

    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Temperature
    print("Temperature: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
        
    sensor_data_time.append(datetime.datetime.now())
    sensor_data_temperature.append(float(msg.payload))

def on_message_humidity(mqttc, obj, msg):
    global first_time
    global sensor_data_time
    global sensor_data_temperature
    global sensor_data_humidity
    
    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Humidity
    print("Humidity: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
 
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

    if first_time:
        first_time = False

        trace0 = go.Scatter(
            x=sensor_data_time,
            y=sensor_data_temperature,
            mode='lines+markers',
            name='DHT11 Temperature Readings',
            text=sensor_data_time)
        )

        trace1 = go.Scatter(
            x=sensor_data_time,
            y=sensor_data_humidity,
            mode='lines+markers',
            name='DHT11 Humidity Readings',
            text=sensor_data_time)
        )

        layout = dict(
            title={
                "text": "DHT11 Temperature and Humidity Readings"
            },
            xaxis={
                "title": "Timestamp"
            },
            yaxis={
                "title": "Sensor Read Value"
            },
            autosize=True,
            hovermode="closest",
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "xanchor": "center",
                "y": 1,
                "x": 0.5
            }
        )
        
        data = [trace0, trace1]
        plot_url = plotly.plot(data, layout=layout)

    else:
        trace2 = go.Scatter(
            x=sensor_data_time[-1], # Shortest and most Pythonic way to get the last element.
            y=sensor_data_temperature[-1],
            mode='lines+markers',
            name='DHT11 Temperature Readings',
            text=sensor_data_time[-1])
        )
        
        trace3 = go.Scatter(
            x=sensor_data_time[-1],
            y=sensor_data_humidity[-1],
            mode='lines+markers',
            name='DHT11 Humidity Readings',
            text=sensor_data_time[-1])
        )
        
        data = [trace2, trace3]
        
        # Extend the traces on the plot with the data in the order supplied.
        plot_url = plotly.plot(data, fileopt='extend')

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
