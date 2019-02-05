import argparse

from app import App
from settings import Settings
from subscriber import *

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings', help='Path to settings file', required=False)
args = parser.parse_args()

filename = 'cfg/settings.json'
if args.settings != None:
	filename = args.settings
settings = Settings()
settings.load(filename)

if settings.subscriber_start:
	broker = settings.subscriber_broker
	port = settings.subscriber_port
	topic = settings.subscriber_topic
	subscriber = Subscriber(broker, port, topic)
	subscriber.start()

app = App(settings, subscriber)
app.run()
