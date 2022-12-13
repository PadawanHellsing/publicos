#!/bin/python
from ipaddress import IPv4Network

ip = input("Digite o IP e a rede que deseja utilizar (Formato: 192.168.0.0/24): ")

for addr in IPv4Network(ip):
  f = open("IPList.txt", "a")
  f.write(f"{addr}\r\n")
print('Lista salva em "IPList.txt".')
f.close()
exit
