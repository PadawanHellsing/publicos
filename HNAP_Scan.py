#!/bin/python3

import sys
import requests
import os
import survey   #Para instalar o Survey: pip install survey
import sys
import colorama #Para instalar o Colorama: pip install colorama
from colorama import Fore,Back,Style,init
init(autoreset=True)
from tqdm import tqdm ##Para instalar o tqdm: pip install tqdm
import argparse
import logging
from ipaddress import IPv4Network

import threading
import time

######## Banner ########

def banner():
        print("""
{white}         ===============        =============     ==============      =======   ========  {reset}
{white}         \\{red}%.%.%.%.%.%.%.{white}\\     //{red}.%.%.%.%.%.%.{white}\\   //{red}.%.%.%.%.%.%.{white}\\  \\{red} {white}||{red}.%.%.{white}\\  /{red}%.%.%{white}||{reset}
{white}         ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}%.%.%.{white}\/{red}%.%.%.{white}||     {reset}
{white}         ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}.%.%.%.%.%.%.%{white}|| {reset}
{white}         ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}%.%{white}|{red}%.%.%.%.%.{white}||     {reset}
{white}         ||{red}%.%.{white}||   ||{red}.%_{white}-|| ||-_{red}%.{white}||   ||{red}.%.{white} || ||{red}%.%.{white}||   ||{red}.%{white}_-|| ||-_{red}.{white}|\{red}%.%.%.%.%{white}||     {reset}
{white}         ||{red}.%.%{white}||   ||-'  {white}|| ||  {white}`-||   {white}||{red}%.%.{white}|| ||{red}.%.%{white}||   ||-'  {white}|| ||  {white}`|\_{red}%.%.{white}|{red}.%.{white}||      {reset}
{white}         ||{red}%.%{white}_||   ||    {white}|| ||    {white}||   ||_ . {white}|| || {white}. _||   ||    {white}|| ||   |\ {white}`-_/| . ||    {reset}
{white}         ||{white}_-' ||  .|/    || ||    \|.  || `-_|| ||_-' ||  .|/    || ||   | \  / |-_.||   {reset}
{white}         ||    {white}||_-'      || ||      `-_||    || ||    ||_-'      || ||   | \  / |  `||   {reset}
{white}         ||    {white}`'         || ||         `'    || ||    `'         || ||   | \  / |   ||   {reset}
{white}         ||            {white}.===' `===.         .==='.`===.         .===' /==. |  \/  |   ||   {reset}
{white}         ||         {white}.=='   \_|-_ `===. .==='   _|_   `===. .===' _-|/   `==  \/  |   ||   {reset}
{white}         ||      {white}.=='    _-'    `-_  `='    _-'   `-_    `='  _-'   `-_  /|  \/  |   ||   {reset}
{white}         ||   {white}.=='    _-'          `-__\._-'         `-_./__-'         `' |. /|  |   ||   {reset}
{white}         ||.=='    _-'                                                     `' |  /==.||  {reset}
{white}         =='    _-'                                                            \/   `==  {reset}
{white}         \   _-'                                                                `-_   /  {reset}
{white}          `''                                                                      ``'   {reset}
{white}================================================================================================================{reset}
{white}        |{green}OPEN-SOURCE PROJECT | https://github.com/PadawanJB/publicos/blob/main/HNAP_Scan.py{white}|               {reset}
{white}        |{green}By PadawanJB                                                                      {white}|               {reset}
{white}        |{red}Não utilize dois parametros ao mesmo tempo, isto resultará em mal funcionamento   {white}|         {white}
{white}================================================================================================================{reset}
""".format(red=Fore.RED,yellow=Fore.YELLOW,green=Fore.GREEN,blue=Fore.BLUE,pink=Fore.MAGENTA,white=Fore.WHITE,reset=Style.RESET_ALL,bright=Style.BRIGHT))

######## Definindo listas ########

#port = ["66", "80", "81", "443", "445", "457", "1080", "1100", "1241", "1352", "1433", "1434", "1521", "1944", "2301", "3000", "3128", "3306", "4000", "4001", "4002", "4100", "5000", "5432", "5800", "5801", "5802", "6346", "6347", "7001", "7002", "8080", "8081", "8082", "8083", "8084", "8085", "8086", "8087", "8088", "8089", "8090", "8443", "8888", "30821"]
port = ["80", "443"]
httplist = []
hnaplist = []

#_#_#_#_ Definição de argumentos #_#_#_#_

parser = argparse.ArgumentParser(prog='HNAP_Scan', description='Efetua um scan HTTP, os hosts que obtiverem acesso HTTP são então adicionados em uma lista de acesso HNAP para que seja efetuado o teste do exploit.', exit_on_error=False)

ipnetworks = parser.add_argument_group('Redes de IP', 'Defina em qual faixa de IP privado fará os testes.')
execdef = parser.add_argument_group('Definições de execução', 'Defina parametros de execução opcionais.')

try:
        class VAction(argparse.Action):
                def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
                        super(VAction, self).__init__(option_strings, dest, nargs, const, default, type, choices, required, help, metavar)
                        self.values = 0
                def __call__(self, parser, args, values, option_string=None):
                        if values is None:
                                self.values += 1
                        else:
                                try:
                                        self.values = int(values)
                                except ValueErro:
                                        self.values = values.count('v')+1
                                setattr(args, self.dest, self.values)
except argparse.ArgumentError:
        print('Digite "-h" ou "--help" para verificar às opções disponives.')

ipnetworks.add_argument('-8', '--pri8', action='store_true', help='Use -8 para a faixa de IP privado 10.0.0.0/8.')
ipnetworks.add_argument('-10', '--cgnat', action='store_true', help='Use -10 para a faixa de IP privado 100.64.0.0/10.')
ipnetworks.add_argument('-12', '--pri12', action='store_true', help='Use -12 para a faixa de IP privado 172.16.0.0/12.')
ipnetworks.add_argument('-16', '--pri16', action='store_true', help='Use -16 para a faixa de IP privado 192.168.0.0/16.')
ipnetworks.add_argument('-t', '--teste', action='store_true', help='Efetua o teste em um IP especifico.')

helptext = """Níveis do verbose:
        0 = Não mostra nenhuma informação de log, somente barra de progresso.
        1 = Mostra logs de sucesso em ações e barra de progresso.
        2 = Mostra os logs de teste, sucesso e barra de progresso."""

execdef.add_argument('-v', '--verbose', action=VAction, const= 1, help=helptext)

args = parser.parse_args()
for c in [args.verbose]:
        verbose = args.verbose

if args.pri8 == True:
        arg1 = "-8"
        if os.path.exists("IPList8.txt"):
                pass
        else:
                for addr in IPv4Network('10.0.0.0/8'):
                        f = open("IPList8.txt", "a")
                        f.write(f"{addr}\r\n")
                f.close()
        IP8 = open('IPList8.txt')
elif args.cgnat == True:
        arg1 = "-10"
        if os.path.exists("IPList10.txt"):
                pass
        else:
                for addr in IPv4Network('100.64.0.0/10'):
                        f = open("IPList10.txt", "a")
                        f.write(f"{addr}\r\n")
                f.close()
        IP10 = open('IPList10.txt')
elif args.pri12 == True:
        arg1 = "-12"
        if os.path.exists("IPList12.txt"):
                pass
        else:
                for addr in IPv4Network('172.16.0.0/12'):
                        f = open("IPList12.txt", "a")
                        f.write(f"{addr}\r\n")
                f.close()
        IP12 = open('IPList12.txt')
elif args.pri16 == True:
        arg1 = "-16"
        if os.path.exists("IPList16.txt"):
                pass
        else:
                for addr in IPv4Network('192.168.0.0/16'):
                        f = open("IPList16.txt", "a")
                        f.write(f"{addr}\r\n")
                f.close()
        IP16 = open('IPList16.txt')
elif args.teste == True:
        arg1 = "-t"
        ipnetwork = survey.input("Digite o IP e a rede que deseja utilizar (Formato: 192.168.0.0/24): ")
        if os.path.exists("IPList.txt"):
                pass
        else:
                for addr in IPv4Network(ipnetwork):
                        f = open("IPList.txt", "a")
                        f.write(f"{addr}\r\n")
                f.close()
        IP1 = open('IPList.txt')
else:
        print('Digite "-h" ou "--help" para verificar às opções disponives.')
        exit()

######## Definindo quantidade de threads ########

threads = int(6)

######## Definindo variaveis ########

portnun = 0
ipnum = 0

if arg1 == "-8" or arg1 == "-10" or arg1== "-12" or arg1 == "-16" or arg1 == "-t":
        try:
                qntlinhas = open('IPList8.txt')
        except:
                pass
        try:
                qntlinhas = open('IPList10.txt')
        except:
                pass
        try:
                qntlinhas = open('IPList12.txt')
        except:
                pass
        try:
                qntlinhas = open('IPList16.txt')
        except:
                pass
        try:
                qntlinhas = open('IPList.txt')
        except:
                pass
        linhasqnt = qntlinhas.readlines()
        ipcar = len(linhasqnt)
        print(ipcar)

if arg1 == "-8" or arg1 == "-10" or arg1== "-12" or arg1 == "-16":
        portcar = len(port)
elif arg1 == "-t":
        portcar = len(port)

######## Definindo formato de log ########

log_format = '%(asctime)s:%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

######## Criando modulos ########

def iptocheck():
        if arg1 == "-8":
                for lineip in IP8:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-10":
                for lineip in IP10:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-16":
                for lineip in IP16:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-12":
                for lineip in IP12:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-t":
                for lineip in IP1:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

def testehttp():
        def funcao_thread(porttest):
                ip_to_check = iptocheck()
                if ip_to_check == None:
                        pass
                else:
                        if verbose > 1:
                                logging.info(f"Testanto {ip_to_check}.\r")
                        else:
                                pass
                        for lineport in range(len(port)):
                                porttest = port[lineport]
                                ipport_to_check = f"{ip_to_check}:{porttest}"
                                try:
                                        r = requests.get(f"{ipport_to_check}", timeout = 2)
                                except requests.ConnectionError:
                                        break
#                               print(r.status_code)
                                if (r.status_code == 200 or r.ststus_code == 301):
                                        logging.info(Fore.GREEN + f"Sucesso ao acessar {ipport_to_check}, status code: {r.status_code}\r")
                                        logging.info(Fore.GREEN + f"Adicionando {ipport_to_check}/ a lista de teste HNAP...\r")
                                        httplist.append(f"{ipport_to_check}")
                                else:
                                        continue
        if __name__ == "__main__":
                format = "%(asctime)s: %(message)s"
                logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
                threads = list()
                for nunthreads in range(15):
                        x = threading.Thread(target=funcao_thread, args=(nunthreads,))
                        threads.append(x)
                        x.start()
        for index, thread in enumerate(threads):
                thread.join()

def testehnap():
        execcurl1 = "curl -s -o /dev/null -w %{http_code} "
        execcurl2 = f"{iphttpslist}/HNAP1 > /dev/null 2>&1"
        execcurl = execcurl1 + execcurl2
        status_code =  os.system(execcurl)
        if(status_code == 0):
                hnaplist.append(f"{iphttpslist}, ")
                logging.info(f"IP {iphttpslist} adicionado a lista de acesso HNAP.\r")
        else:
                pass

def exploitnhap():
        pergunta1 = survey.confirm('Deseja baixar o "hnap0wn"? ', default = True)
        if pergunta1 == True:
                diretorio1 = survey.path('/home/', 'Informe o diretório que deseja instalar: ')
                os.system(f"mkdir {diretorio1}/hnap0wn")
                os.system(f"cd {diretorio1}/hnap0wn")
                os.system(f"wget -P {diretorio1}/hnap0wn https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/11101.tar.gz")
                os.system(f"sudo tar -xf {diretorio1}/hnap0wn/11101.tar.gz -C {diretorio1}hnap0wn/")
                logging.info(f"Download concluido com sucesso!!\r")
                print(" - Para mais informações de como utilizar o software acesse https://miloserdov.org/?p=5256.")
        elif pergunta1 == False:
                pass
        else:
                logging.info("Opção inválida.\r")
        pergunta2 = survey.confirm('Deseja salvar a lista de IPs que possuem a vulnerabilidade? ', default = False)
        if pergunta2 == True:
                f = open("HNAP_IP_List.txt", "x")
                f = open("HNAP_IP_List.txt", "a")
                f.write(f"{hnaplist}")
                f.close()
                logging.info(f'Lista salva em "HNAP_IP_List.txt"\r')
        elif pergunta2 == False:
                pass
        else:
                logging.info("Opção inválida.\r")

        pergunta3 = survey.confirm('Deseja salvar a lista de IPs que possuem o acesso HTTP? ', default = False)
        if pergunta3 == True:
                f = open("HTTP_IP_List.txt", "x")
                f = open("HTTP_IP_List.txt", "a")
                f.write(f"{httplist}")
                f.close()
                logging.info(f'Lista salva em "HTTP_IP_List.txt"\r')
        elif pergunta3 == False:
                pass

def limpartela():
        os.system("clear")
        banner()

def limpararq():
        if os.path.exists("IPList8.txt"):
                os.remove("IPList8.txt")
        elif os.path.exists("IPList10.txt"):
                os.remove("IPList10.txt")
        elif os.path.exists("IPList12.txt"):
                os.remove("IPList12.txt")
        elif os.path.exists("IPList16.txt"):
                os.remove("IPList16.txt")
        elif os.path.exists("IPList.txt"):
                os.remove("IPList.txt")
        else:
                pass

######## Inicio do código ########

limpartela()

with tqdm(total=ipcar, position=0, leave=True) as barra_progresso:
        if (ipnum/64770) <= 1:
                while(ipnum <= ipcar):
                        if(portnun <= portcar):
                                if verbose != 2:
                                        limpartela()
                                else:
                                        pass
                                barra_progresso.update(15)
                                ipnum = ipnum+15
                                testehttp()
                        elif(portnun >= portcar):
                                portnun=0
                                pass
                        else:
                                portnun=0
                                pass
                else:
                        pass
        elif ipcar/64770 == 1:
                pass
        else:
                print("Erro.")

for iphttpslist in tqdm(httplist):
        iphttpslist = str(iphttpslist)
        iphttpslist = iphttpslist.strip()
        testehnap()
        if verbose != 2:
                limpartela()
        else:
                pass
else:
        pass

exploitnhap()

limpararq()

print(f" - Que a Força esteja com você...")
