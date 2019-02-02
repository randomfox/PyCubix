# Original server code written by joonty/Jonathan Cairns
# https://gist.github.com/joonty/6463568

import sys
import socket
import threading
from queue import Queue

class SocketServer(threading.Thread):
    STOP_COMMAND = "stop"

    def __init__(self, host, port, bufsize, command_queue, message_queue):
        self.host = host
        self.port = port
        self.bufsize = bufsize
        self.command_queue = command_queue
        self.message_queue = message_queue
        self.count = 0
        threading.Thread.__init__(self)

    def run(self):
        print('Starting server')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.bind((self.host, self.port))
            s.listen(5)

            done = False
            while not done:
                try:
                    client, address = s.accept()
                    print('Client connected', client, address)
                    while True:
                        done = self.should_exit()
                        if done or not self.handle_client(client):
                            client.close()
                            done = True
                            break
                except socket.error:
                    pass
        except Exception:
            print('# WTF')
            print(sys.exc_info())
        print('Stopping server')

    def handle_client(self, client):
        data = client.recv(self.bufsize).decode()
        if data == '':
            print('Client disconnected')
            return False
        else:
            self.message_queue.put_nowait(data)
            self.count += 1
            response = "recv:{}:{}\n".format(self.count, len(data))
            client.send(response.encode())
            return True

    def should_exit(self):
        try:
            if self.command_queue.empty() == False:
                if self.command_queue.get_nowait() == SocketServer.STOP_COMMAND:
                    return True
        except:
            return True
        return False

class SocketServerControl:
    def __init__(self):
        self.command_queue = Queue(0)
        self.message_queue = Queue(0)

    def start(self, host, port, bufsize):
        server = SocketServer(host, port, bufsize, self.command_queue, self.message_queue)
        server.start()

    def stop(self):
        self.message_queue.put(SocketServer.STOP_COMMAND)

    def has_pending_messages(self):
        return self.message_queue.empty() == False

    def get_message(self):
        try:
            if self.has_pending_messages():
                return self.message_queue.get_nowait()
        except:
            pass
        return None
