# Original server code written by joonty/Jonathan Cairns
# https://gist.github.com/joonty/6463568

import sys
import select
import socket
import threading
import time
from queue import Queue

class SocketServer(threading.Thread):
    STOP_COMMAND = "stop"

    def __init__(self, host, port, bufsize, command_queue, message_queue):
        self.host = host
        self.port = port
        self.bufsize = bufsize
        self.command_queue = command_queue
        self.message_queue = message_queue
        self.running_number = 0
        self.count = 0
        threading.Thread.__init__(self)

    def run(self):
        print('Starting server')
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setblocking(0)
            server.bind((self.host, self.port))
            server.listen(5)

            inputs = [server]
            outputs = []
            # message_queues = {}

            while inputs:
                if self.should_exit():
                    print('should_exit!')
                    break
                readable, writable, exceptional = select.select(inputs, outputs, inputs)

                print("count", self.count)
                self.count += 1

                if self.should_exit():
                    print('should_exit!')
                    break

                for sock in readable:
                    if sock is server:
                        connection, client_address = sock.accept()
                        print("client connected", connection, client_address)
                        connection.setblocking(0)
                        inputs.append(connection)
                        # message_queues[connection] = Queue(0)
                    else:
                        data = sock.recv(1024)
                        if data:
                            decoded_data = data.decode().strip()
                            print("received", decoded_data)
                            # message_queues[sock].put(data)

                            self.message_queue.put_nowait(decoded_data)
                            self.running_number += 1
                            response = "recv:{}:{}\n".format(self.running_number, len(data))
                            sock.send(response.encode())

                            if sock not in outputs:
                                outputs.append(sock)
                        else:
                            if sock in outputs:
                                outputs.remove(sock)
                            inputs.remove(sock)
                            sock.close()
                            print('client disconnected')
                            # del message_queues[sock]

                # for sock in writable:
                #     try:
                #         next_msg = message_queues[sock].get_nowait()
                #     except:# queue.Empty:
                #         outputs.remove(sock)
                #     else:
                #         sock.send(next_msg)

                for sock in exceptional:
                    inputs.remove(sock)
                    if sock in outputs:
                        output.remove(sock)
                    sock.close()
                    print('client disconnected')
                    # del message_queues[sock]

                time.sleep(0.1)

        except Exception:
            print('# WTF')
            print(sys.exc_info())

        print('Stopping server')
        sys.exit()

        # done = False
        # while not done:
        #     try:
        #         self.check_exit()
        #         client, address = sock.accept()
        #         print('Client connected', client, address)
        #         while True:
        #             self.check_exit()
        #             # done = self.should_exit()
        #             # if done or not self.handle_client(client):
        #             if not self.handle_client(client):
        #                 client.close()
        #                 done = True
        #                 break
        #     except socket.error:
        #         pass

    # def handle_client(self, client):
    #     data = client.recv(self.bufsize).decode()
    #     if data == '':
    #         print('Client disconnected')
    #         return False
    #     else:
    #         self.message_queue.put_nowait(data)
    #         self.count += 1
    #         response = "recv:{}:{}\n".format(self.count, len(data))
    #         client.send(response.encode())
    #         return True

    # def check_exit(self):
    #     try:
    #         print("check exit")
    #         if self.command_queue.get_nowait() == STOP_COMMAND:
    #             raise Exception("Exiting")
    #     except:
    #         pass

    def should_exit(self):
        try:
            print("checking command queue")
            if self.command_queue.empty() == False:
                if self.command_queue.get_nowait() == STOP_COMMAND:
                    print("received exit command")
                    return True
                else:
                    print("command queue empty")
        except:
            return True
        return False

class SocketServerControl:
    def __init__(self):
        self.command_queue = Queue(0)
        self.message_queue = Queue(0)
        self.server = None

    def start(self, host, port, bufsize):
        self.server = SocketServer(host, port, bufsize, self.command_queue, self.message_queue)
        self.server.start()

    def stop(self):
        print('adding stop command')
        self.command_queue.put(SocketServer.STOP_COMMAND)
        # self.server.join(3)

    def has_pending_messages(self):
        return self.message_queue.empty() == False

    def get_message(self):
        try:
            if self.has_pending_messages():
                return self.message_queue.get_nowait()
        except:
            pass
        return None
