#!/usr/bin/python3
""" Diyhas raspberry pi monitor """

import time

import paho.mqtt.client as mqtt

import diyoled128x64

import sysutility

OLED = diyoled128x64.DiyOLED128x64()

def check_system_status(utility):
    ''' display systems status '''
    utility.check_system_status()

def last_timed_event():
    ''' reset the timed events dictionary '''
    for key in TIMED_EVENTS_DICTIONARY:
        TIMED_EVENTS_DICTIONARY[key]["executed"] = False

TIMED_EVENTS_DICTIONARY = {
    "01": {"method":check_system_status, "executed":False},
    "11": {"method":check_system_status, "executed":False},
    "21": {"method":check_system_status, "executed":False},
    "31": {"method":check_system_status, "executed":False},
    "41": {"method":check_system_status, "executed":False},
    "51": {"method":check_system_status, "executed":False}
    }

def check_for_timed_events(utility):
    ''' see if its time to capture and publish metrics '''
    minute_string = time.strftime("%M")
    if minute_string == "59":
        last_timed_event()
    elif minute_string in TIMED_EVENTS_DICTIONARY:
        if not TIMED_EVENTS_DICTIONARY[minute_string]["executed"]:
            TIMED_EVENTS_DICTIONARY[minute_string]["executed"] = True
            TIMED_EVENTS_DICTIONARY[minute_string]["method"](utility)

def system_message(msg):
    """ process system messages"""
    global SYSUTILITY
    if msg.topic == 'diyhas/system/who':
        if msg.payload == b'ON':
            OLED.set(0, SYSUTILITY.host + ": " + SYSUTILITY.ip_address)
            OLED.set(1, "U: an    R: buster")
            OLED.set(2, "C: " + SYSUTILITY.cpu + "% " + SYSUTILITY.celsius + "C ")
            OLED.set(3, "M: " + SYSUTILITY.memory + "MB A: " + SYSUTILITY.available + "MB")
            OLED.set(4, "D: " + SYSUTILITY.disk + "GB F: " + SYSUTILITY.free + "GB")
            OLED.show()
        else:
            OLED.clear()

# use a dispatch model for the subscriptions
TOPIC_DISPATCH_DICTIONARY = {
    "diyhas/system/fire":
        {"method":system_message},
    "diyhas/system/panic":
        {"method":system_message},
    "diyhas/system/who":
        {"method":system_message}
    }

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rcdata):
    """ if we lose the connection & reconnect, subscriptions will be renewed """
    client.subscribe("diyhas/system/fire", 1)
    client.subscribe("diyhas/system/panic", 1)
    client.subscribe("diyhas/system/who", 1)

def on_disconnect(client, userdata, rc):
    client.connected_flag=False
    client.disconnect_flag=True

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    """ dispatch to the appropriate MQTT topic handler """
    TOPIC_DISPATCH_DICTIONARY[msg.topic]["method"](msg)

if __name__ == '__main__':

    global SYSUTILITY

    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.on_message = on_message
    CLIENT.connect("192.168.1.17", 1883, 60)
    CLIENT.loop_start()

    SYSUTILITY = sysutility.SystemUtility(CLIENT)

    # give network time to startup - hack?
    time.sleep(1.0)

    # loop forever checking for interrupts or timed events

    while True:
        time.sleep(10.0)
        check_for_timed_events(SYSUTILITY)
