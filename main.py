#!/usr/bin/python
from threading import Thread
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
    Topic("group3/homebridge/sprinklers/livingroom/value", '1', '0'),
    Topic("group3/homebridge/sprinklers/bathroom/value", '1', '0'),
    Topic("group3/homebridge/sprinklers/kitchen/value", '1', 0),
    Topic("group3/homebridge/firesensor/value", '1', '0'),
    Topic("group3/homebridge/garagedoor/value", '0', '1'),
    Topic("group3/homebridge/buzzer/value", '1', '0'),
    Topic("group3/homebridge/window/targetvalue", '0', '100'),
    Topic("group3/homebridge/window/currentvalue", '0', '100'),
    Topic("group3/homebridge/window/open", 'stop', 'stop'),
]
stop_thread = False

def start_music():
    buzzer.start(50)
    while True:
        for i in range(1, len(Buzzer.song)):
            if stop_thread:
                return
            buzzer.change_frequency(Buzzer.song[i])
            time.sleep(Buzzer.beat[i]*0.13)

buzz_thread = None

def on_message(_, __, message):
    print(message.payload)
    if message.payload == b'\x31':
        buzz_thread = Thread(target = start_music)
        stop_thread = False
        buzz_thread.start()
    else:
        stop_thread = True
        buzzer.stop()


mqtt = MqttClient("localhost", 1883, 60, 'group3', 'Saperlipopette', topics, on_message)
mqtt.connect()



def callback(pin):
    status = GPIO.input(pin)
    if status == 1:
        print("flame detected")
        mqtt.trigger_fire_sensor()
    else:
        mqtt.shutdown_fire_sensor()
        buzzer.stop()


flame_sensor = FlameSensor(flame_sensor_pin, callback)


print("starting project....")
# infinite loop
while True:
    mqtt.loop_forever()
