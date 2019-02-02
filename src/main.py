from app import App
from settings import Settings
from socketserver import SocketServerControl

filename = 'cfg/settings.json'
settings = Settings()
settings.load(filename)

server_control = SocketServerControl()
if settings.server_start:
	host = settings.server_host
	port = settings.server_port
	server_control.start(host, port)
else:
	print('Not starting socket server')

app = App(settings, server_control)
app.run()
