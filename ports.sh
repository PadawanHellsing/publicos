#!/bin/bash

echo "#######################################"
echo "######## Testa porta de origem ########"
echo "#######################################"
echo -n "IP alvo: "
read alvo

for top in 100
do
 echo "Testando as $top portas mais comuns"
 for porta in 53 80 443 22
 do
  # Executando scan com nmap
  echo "[+] Testando PORTA de ORIGEM $porta"
  portas_open1=$(sudo nmap -Pn -sS -D RND:20 --top-ports=$top -n --max-retries=0 -T5 --open $alvo | grep  "\/tcp")
  portas_open2=$(sudo nmap -Pn -sS -D RND:20 --top-ports=$top -g $porta -n --max-retries=0 -T5 --open $alvo | grep "\/tcp")
  echo " Total OPEN 1 = $portas_open1"
  echo " Total OPEN 2 = $portas_open2"
  echo "-----------------------------" 
#  echo "[?] Verificando se houve difernen  a entre as duas saidas acima."
 done
done

exit 0
