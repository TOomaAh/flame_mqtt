from pydoc_data.topics import topics
import paho.mqtt.client as mqtt
from topic import Topic

class MqttClient:


    def __init__(self, url : str, port : int, keep_alive : int, username: str, password: str, topics : list, on_message):
        self.topics = topics
        self.url = url
        self.port = port
        self.keep_alive = keep_alive
        self.username = username
        self.password = password
        self.on_message = on_message
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.subscribe(Topic("group3/homebridge/buzzer/value", None, None))
            self.client.on_message = self.on_message
        else:
            print(f"Failed to connect, return code \n", rc)

    def __on_connect_fail(self):
        print("error during broker connect....")

    def connect(self):
        self.client.connect(self.url, self.port, self.keep_alive)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.__on_connect_fail
        
        

    def publish(self, topic : str, message : str):
        self.client.publish(topic = topic, payload = message, qos = 2, retain = True)

    def trigger_fire_sensor(self):
        for i in self.topics:
            self.publish(i.path, i.on_value)

    def set_on_message(self, on_message):
        self.client.on_message = on_message


    def subscribe(self, topic : Topic):
        self.client.subscribe(topic.path, 2)

    def shutdown_fire_sensor(self):
        for i in self.topics:
            self.publish(i.path, i.off_value)

    def loop_forever(self):
        self.client.loop_start()
