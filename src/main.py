import argparse

from app import App
from settings import Settings
from mqttclient import *

parser = argparse.ArgumentParser()
parser.add_argument('--settings', help='Path to settings file', required=False)
parser.add_argument('--glinfo', help='Show OpenGL info', required=False, action="store_true")
args = parser.parse_args()

filename = 'cfg/settings.json'
if args.settings != None:
	filename = args.settings
settings = Settings()
settings.load(filename)

if settings.mqtt_client_start:
	broker = settings.mqtt_client_broker
	port = settings.mqtt_client_port
	topic = settings.mqtt_client_subscribe_topic
	client = MqttClient(broker, port, topic)
	client.start()

glinfo = args.glinfo
app = App(settings, client, glinfo)
app.run()
