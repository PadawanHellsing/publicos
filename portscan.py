#!/usr/bin/python
import socket,sys

for porta in range(1,65565):

  meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if meusocket.connect_ex((sys.argv[1],porta)) == 0:
    print(f"Porta {porta}, aberta.")
    meusocket.close()
