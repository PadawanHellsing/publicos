#!/bin/python
import argparse
from ipaddress import IPv4Network

def main():
  parser = argparse.ArgumentParser(description="Gerador de IP's em um range")
  parser.add_argument("-o", "--output", help="Nome do arquivo final", default="IPList.txt")
  parser.add_argument("-r", "--range", help="Digite o IP e a rede que deseja utilizar (Formato: 192.168.0.0/24): ")
  args = parser.parse_args()
  generateRange(args.output, args.range) if args.range else print("Digite -h para ver as opcoes disponiveis.")

def generateRange(filename, range):
  with open(filename, "w") as f: 
    for ip in IPv4Network(range): f.write(f"{ip}\n")
  print(f"Lista salva em {filename}.")

if __name__ == "__main__":
  try: main()
  except Exception as err: print(f"Error:{err}")
  
