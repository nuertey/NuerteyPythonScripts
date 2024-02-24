#!/usr/bin/env python3.9

# TBD Nuertey Odzeyem; Create a versioned requirements.txt with pipreqs:
import os
import sys
import logging
import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep
from time import time
from argparse import ArgumentParser


from pprint import pprint
from pprint import pformat
from binascii import hexlify

#global_mqtt_sender_logger.info(f' {hexlify(composed_aos_bytes)}\n')

class MQTTClientBase(Thread):
    def __init__(self, creator, mqtt_port, mqtt_host, verbose=False, keepalive=60):
        super().__init__()
        
        self.creator = creator 
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.keepalive = keepalive
        self.verbose = verbose
        self.the_mqtt_client = None  
        #self.logger_filename = self.creator + '_Logger.log'
        
        # set up logging to file
        logging.basicConfig(
             filename=self.logger_filename,
             level=logging.DEBUG, 
             format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
             datefmt='%Y-%m-%dT%H:%M:%SZ'
         )

        # set up logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

        self.logger = logging.getLogger('')
        
    def run(self):
        self.the_mqtt_client.loop_forever()  
        
    def publish(self, topic, payload=None, qos=0, retain=False):
        self.the_mqtt_client.publish(topic, payload, qos, retain)
        
    # MQTT callback method within which message subscriptions could potentially happen. Written in such
    # a manner so that on reconnections, topics will be properly re-subscribed to, that is, if the user of this class,  
    # overrides this method to indeed subscribe to pertinent MQTT topics of interest. Otherwise, user can just 'pass',
    # or simply rely on this base class implementation in situ.
    def on_connect(self, client, userdata, flags, rc):
        if self.verbose:
            self.logger.info(f' MQTT Client {self.creator} connected.\n')
            
    # MQTT callback method within which message handling/processing occurs.        
    def on_message(self, client, userdata, message):
        if self.verbose:
            self.logger.info(f' MQTT Client {self.creator} message topic = {message.topic}')
            self.logger.info(f' MQTT Client {self.creator} message qos = {message.qos}')
            self.logger.info(f' MQTT Client {self.creator} message retain flag = {message.retain}\n')
            
            self.logger.info(f' MQTT Client {self.creator} message received = {str(message.payload)}\n')
    
    # MQTT callback method.
    def on_publish(self, client, userdata, mid):
        if self.verbose:
            self.logger.debug(f' MQTT Client {self.creator} message published mid: {str(mid)}\n')
    
    # MQTT callback method.
    def on_subscribe(self, client, userdata, mid, granted_qos):
        if self.verbose:
            self.logger.debug(f' MQTT Client {self.creator} message subscribed: {str(mid)} {str(granted_qos)}\n')
    
    # MQTT callback method. For thoroughness.     
    def on_unsubscribe(self, client, userdata, mid):
        if self.verbose:
            self.logger.debug(f' MQTT Client {self.creator} message unsubscribed mid: {str(mid)}\n')
            
    # MQTT callback method.
    def on_log(self, client, userdata, level, buf):
        if self.verbose:
            self.logger.debug(f' MQTT Client {self.creator} log: {buf}\n')         
