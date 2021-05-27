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
    
import time
import datetime
import paho.mqtt.client as mqtt
import threading

import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout
from plotly.subplots import make_subplots

sensor_data_time = []
sensor_data_temperature = []
sensor_data_humidity = []

# Mapbox token for satellite plot:
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

def network_to_host(payload):
    #print(type(payload))
    #print()
    payload = payload.decode("utf-8")
    return float(payload)

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print()

def on_message_temperature(mqttc, obj, msg):
    global sensor_data_time
    global sensor_data_temperature

    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Temperature
    print("Temperature: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
        
    sensor_data_time.append(datetime.datetime.now())
    sensor_data_temperature.append(network_to_host(msg.payload))

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
 
    sensor_data_humidity.append(network_to_host(msg.payload))

    # For debugging. Disable once testing is completed.
    #print('Debug -> Time:')
    #print(sensor_data_time)
    #print()
    #print('Debug -> Temperature:')
    #print(sensor_data_temperature)
    #print()
    #print('Debug -> Humidity:')
    #print(sensor_data_humidity)
    #print()
        
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    print()

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    print()

def on_log(mqttc, obj, level, string):
    print(string)
    print()

# Called by the MQTT Sensor Data Collector thread
def do_mqtt_processing_forever():
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

t = threading.Thread(target=do_mqtt_processing_forever, name="MQTTThread")
t.daemon = True # Being a daemon here implies thread will also be killed if the main thread context ends.
t.start()

# Dashboard graphing is in the main thread context after we have waited 
# sufficiently enough for a meaningful range of sensor values to accumulate:
while True:
    # Wait for 2 minutes
    time.sleep(120)

    if sensor_data_time and sensor_data_temperature and sensor_data_humidity:
        # Grab data accumulated thus far and plot it:
        figure1 = make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    
        trace0 = go.Scatter(
            x=sensor_data_time,
            y=sensor_data_temperature,
            mode='lines+markers',
            name='DHT11 Temperature Readings',
            text=sensor_data_time
        )

        trace1 = go.Scatter(
            x=sensor_data_time,
            y=sensor_data_humidity,
            mode='lines+markers',
            name='DHT11 Humidity Readings',
            text=sensor_data_time
        )
        
        figure1.add_trace(
            trace0,
            row=1, col=1
        )

        figure1.add_trace(
            trace1,
            row=2, col=1
        )
        
        figure1.update_layout(
            title="DHT11 Temperature and Humidity Readings",
            xaxis_title="Timestamp",
            yaxis_title="Sensor Read Value"
        )
        figure1.show()
