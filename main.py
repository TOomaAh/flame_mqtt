#!/usr/bin/python
from FlameSensor import FlameSensor
import RPi.GPIO as GPIO
import time
from buzzer import Buzzer
from mqtt import MqttClient
import os

from topic import Topic

#GPIO SETUP
flame_sensor_pin = 26
buzzer_pin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


buzzer = Buzzer(buzzer_pin)

#MQTT SETUP
env = os.environ.get("ENV")

topics = [
    Topic("group3/homebridge/firesensor/value"),
    Topic("group3/homebridge/garagedoor/value"),
    Topic("group3/homebridge/windowblinds/value"),
    Topic("group3/homebridge/buzzer/value")
]


def on_message(_, __, message):
    if message.payload == '1':
        buzzer.start()
        for i in range(1, len(Buzzer.song)):
            buzzer.change_frequency(Buzzer.song[i])
            time.sleep(Buzzer.beat[i]*0.13)
        buzzer.stop()
    else:
        buzzer.stop()
        time.sleep(0.5)



if env == "PROD":
    mqtt = MqttClient("lesepices.local", 1883, 60, topics, on_message)
else:
    mqtt = MqttClient("test.mosquitto.org", 1883, 60, topics, on_message)



mqtt.connect()
mqtt.subscribe(Topic("group3/homebridge/buzzer/value"))





def callback():
    print("flame detected")
    mqtt.trigger_fire_sensor()


flame_sensor = FlameSensor(flame_sensor_pin, callback)

# infinite loop
while True:
    time.sleep(1)
