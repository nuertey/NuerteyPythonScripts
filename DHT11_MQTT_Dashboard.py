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
import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import plotly
import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

sensor_data = {
    'Time': [],
    'Temperature': [],
    'Humidity': []
}

token = open(".mapbox_token").read() 

figure1 = go.Figure()

figure1.update_layout(
    title='Buffalo Grove - Illinois',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=token,
        bearing=0,
        center=dict(
            lat=42.1689,
            lon=87.9629
        ),
        pitch=0,
        zoom=12,
        style='satellite-streets'
    ),
)

figure1.show()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print()

def on_message_temperature(mqttc, obj, msg):
    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Temperature
    print("Temperature: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
    
    time_now = datetime.datetime.now()
    sensor_data['Time'].append(time_now)
    sensor_data['Temperature'].append(msg.payload)

def on_message_humidity(mqttc, obj, msg):
    # This callback will only be called for messages with topics that match:
    #
    # /Nuertey/Nucleo/F767ZI/Humidity
    print("Humidity: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print()
    
    sensor_data['Humidity'].append(msg.payload)
    print('Debug -> Cumulative Sensor Data:')
    print(sensor_data)
    print()

    print('Debug -> Dimensions of Cumulative Sensor Data:')
    print(sensor_data.shape)
    print()

    # Create the graph with subplots
    figure2 = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    figure2['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    figure2['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    figure2.append_trace({
        'x': sensor_data['Time'],
        'y': sensor_data['Temperature'],
        'name': 'DHT11 Temperature Readings',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    figure2.append_trace({
        'x': sensor_data['Time'],
        'y': sensor_data['Humidity'],
        'text': sensor_data['Time'],
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

mqttc.loop_forever()


# ============================================
# Some column data visualizations, line graph:
# ============================================
figure1 = go.Figure()
figure1.add_trace(go.Scatter(x=airbnb_data_dropped['host_since'], 
                            y=airbnb_data_dropped['number_of_reviews'],
                            mode='markers',
                            name='Number of Reviews',
                            line=dict(color='red', width=1)
))
figure1.update_layout(title='Amsterdam, Noord-Holland - Airbnb Host Since Date/Number Of Reviews',
                     xaxis_title='Airbnb Host Since Date',
                     yaxis_title='Number Of Reviews')
figure1.show()


# Attempt to make the background transparent.
#figure2.update_layout({
#     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
#})
