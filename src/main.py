from app import App
from settings import Settings
from subscriber import *

filename = 'cfg/settings.json'
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
