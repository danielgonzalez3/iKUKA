import socket
import time
import io


# The Windows interface is a virtual interface of the KLI. It has a preconfigured static IP address:
host = '172.31.1.147'
port = '30001'


class KUKA:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.buff = io.StringIO('2048')
        time.sleep(3)

    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("connection disconnected")
            totalsent = totalsent + sent

    def receive(self):
        output = []
        while True:
            data = self.sock.recv(1)
            if data == '\n':
                break
            self.buff.write(data)
        output = self.buff.getvalue()
        self.buff.truncate(0)
        return output

    def close(self):
        self.sock.send('end\n')
        time.sleep(1)
        self.sock.close()
