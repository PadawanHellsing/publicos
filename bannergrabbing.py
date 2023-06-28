#!/usr/bin/python
import socket,sys

ip = sys.argv[1]
porta = int(sys.argv[2])

meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
meusocket.connect_ex((ip,porta))
banner = meusocket.recv(1024)
print(banner)
