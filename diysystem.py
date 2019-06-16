#!/usr/bin/python3
""" Diyhas raspberry pi monitor """

import time

import paho.mqtt.client as mqtt

import sysutility

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
    print("msg.payload=", msg.payload)
    if msg.topic == 'diyhas/system/who':
        if msg.payload == b'ON':
            print("who ON")
        else:
            print("who OFF")

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
    print("userdata=%s flags=%s rcdata=%s", userdata, flags, rcdata)
    client.subscribe("diyhas/system/fire", 1)
    client.subscribe("diyhas/system/panic", 1)
    client.subscribe("diyhas/system/who", 1)

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    """ dispatch to the appropriate MQTT topic handler """
    print("userdata=", userdata)
    TOPIC_DISPATCH_DICTIONARY[msg.topic]["method"](client, msg)


if __name__ == '__main__':

    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_message = on_message
    CLIENT.connect("192.168.1.133", 1883, 60)
    CLIENT.loop_start()

    SYSUTILITY = sysutility.SystemUtility(CLIENT)

    # give network time to startup - hack?
    time.sleep(1.0)

    # loop forever checking for interrupts or timed events

    while True:
        time.sleep(10.0)
        check_for_timed_events(SYSUTILITY)
