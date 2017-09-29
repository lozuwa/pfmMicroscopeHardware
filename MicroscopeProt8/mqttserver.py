"""
Author: Rodrigo Loza
Company: pfm 
Description: Main program for microscope's hardware
Documentation:
* /zu -> controls the z axis to move up
* /zd -> controls the z axis to move down
* /led -> turns on the led
* /steps -> controls the number of steps for XY axis
* /home -> resets the motors of the microscope
* /movefieldx -> controls the x axis
* /movefieldy -> controls the y axis
"""
# MQTT
import paho.mqtt.client as mqtt
# General purpose
import os
import time
import datetime
# Tensor manipulation
import numpy as np
# Supporting libraries
from interface import *
from autofocus import *
from utils import *
from ops import *

# Initialize mqtt client
client = mqtt.Client()

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Microscope hardware
    client.subscribe("/zu")
    client.subscribe("/zd")
    client.subscribe("/led")
    client.subscribe("/steps")
    client.subscribe("/home")
    client.subscribe("/movefieldx")
    client.subscribe("/movefieldy")
    # Autofocus
    client.subscribe("/autofocus")
    client.subscribe("/variance")
    # Microscope
    client.subscribe("/microscope")
    # Automatic
    client.subscribe("/automatic")

# Reply messages
def on_message(client, userdata, msg):
    global STEPSZ, TIME
    global procZUp, procZDown
    global autofocusState, hardwareCode, countFrames
    global countPositions, saveAutofocusCoef
    print(msg.topic, msg.payload)
    if msg.topic == MOVEFIELDX_TOPIC:
        moveFieldX(msg.payload)
    elif msg.topic == MOVEFIELDY_TOPIC:
        moveFieldY(msg.payload)
    elif msg.topic == HOME_TOPIC:
        home()
    elif msg.topic == STEPS_TOPIC:
        STEPSZ = float(msg.payload)*3
    elif msg.topic == LED_TOPIC:
        led(msg.payload)
    ##################################################################################
    elif msg.topic == AUTOFOCUS_TOPIC:
        pass
    ##################################################################################
    elif msg.topic == VARIANCE_TOPIC:
        pass
    ##################################################################################
    elif msg.topic == "/automatic":
        # Home
        homeXY()
        # Direction x
        directionX = True
        # Start at home
        for i in range(1600):
            publishMessage(topic = "/microscope",\
                            message = "pic;sample",\
                            qos = 2)
            # Move X
            if directionX:
                moveFieldX(1)
            else:
                moveFieldX(0)
            # Move Y
            if (i % 50 == 0):
                moveFieldY(0)
                moveFieldY(0)
                # Invert X direction
                directionX = not directionX
                # Take picture
                publishMessage(topic = "/microscope",\
                            message = "pic;sample",\
                            qos = 2)
            elif (i % 75 == 0):
                pass
                #autofocus()
            else:
                pass
    ##################################################################################
    elif msg.topic == ZUP_TOPIC:
        moveFieldZUp(msg.payload)
    elif msg.topic == ZDOWN_TOPIC:
        moveFieldZDown(msg.payload)
    else:
        pass

def publishMessage(topic,
                    message,
                    qos = 2):
    """
    Publishes a mqtt message
    :param topic: input string that defines the target topic
    :param message: input string that denotes the content of the message
    :param qos: input int that defines the type of qos for the mqtt communication
    """
    # Assert variables
    assert type(topic) == str, VARIABLE_IS_NOT_STR
    assert type(message) == str, VARIABLE_IS_NOT_STR
    assert type(qos) == int, VARIABLE_IS_NOT_INT
    # Publish message
    client.publish(topic, message, qos)

if __name__ == "__main__":
    # Autofocus variables
    global autofocusState
    global hardwareCode
    global countFrames
    global countPositions
    global saveAutofocusCoef
    autofocusState = False
    hardwareCode = "o"
    countFrames = 0
    countPositions = 0
    saveAutofocusCoef = []

    # Connect to mqtt client
    client.connect(IP, PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()