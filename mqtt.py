from pydoc_data.topics import topics
import paho.mqtt.client as mqtt
from topic import Topic

class MqttClient:


    def __init__(self, url : str, port : int, keep_alive : int, topics : list, on_message):
        self.topics = topics
        self.url = url
        self.port = port
        self.keep_alive = keep_alive
        self.client = mqtt.Client()
        self.client.on_message = on_message


    def connect(self):
        self.client.connect(self.url, self.port, self.keep_alive)

    def publish(self, topic : str, message : str):
        self.client.publish(topic, message, 2, True)

    def trigger_fire_sensor(self):
        for i in topics:
            self.publish(i.path, '1')


    def subscribe(self, topic : Topic):
        self.client.subscribe(topic.path, 2)

    def shutdown_fire_sensor(self):
        for i in topics:
            self.publish(i.path, '0')

