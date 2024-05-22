from socketIO_client import SocketIO

socketIO = SocketIO('localhost', 5010)
print('[*] Socket.IO connection established on domain: localhost and port: 5010')

def on_message(*args):
    print('[*] Message received: ', args[0], ' from domain: localhost on port: 5010')

socketIO.on('message', on_message)
socketIO.emit('message', 'Hello, server!')
socketIO.wait(seconds=1)