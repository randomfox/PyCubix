from queue import Queue
import paho.mqtt.client as mqtt

# broker = 'iot.eclipse.org'
# topic = '$SYS/#'

class Subscriber:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.message_queue = Queue(0)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def start(self):
        print('Starting subscriber {}:{}'.format(self.broker, self.port))
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def stop(self):
        print('Stopping subscriber')
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print('Subscriber connected {} ({})'.format(self.topic, str(rc)))
        self.client.subscribe(self.topic)

    def on_disconnect(self, client, userdata, rc=0):
        print('Subscriber disconnected', str(rc))
        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode('utf-8'))
        topic = message.topic
        print('message topic:{} payload:{}'.format(topic, payload))
        if topic == self.topic:
            self.message_queue.put_nowait(payload)

    def has_pending_messages(self):
        return self.message_queue.empty() == False

    def get_message(self):
        try:
            return self.message_queue.get_nowait()
        except:
            pass
        return None
