#!/bin/bash
if [ $1 == "" ]
then
  echo "HTTP Parsing HTML"
  echo "$0 DOMAIN"
  echo "Exemplo: $0 google.com"
else
wget $1 2> /dev/null
echo ======================================================================================
echo "                     Resolvendo URLs em: $1"
echo ======================================================================================
grep href index.html | cut -d "/" -f 3 | grep "\." | cut -d '"' -f 1 | grep -v "<l" > $1.txt
echo [+] Concluido: Salvando os resultados em: $1.txt
echo
echo ======================================================================================
echo "    Line                       IP                              ADDRESS"
echo ======================================================================================
line=0
for url in $(cat $1.txt);
do
line=$((line+1))
host $url | grep "has address" | cut -d " " -f 4 > listaip.txt;
for ip in $(cat listaip.txt);
do echo "    $line                    $ip                       $url";done
done
rm index.html
rm listaip.txt
rm $1.txt
fi
