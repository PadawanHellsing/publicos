#!/bin/bash

#O objetivo deste código é fazer um scan onde é verificado quais roteadores possuem usuário e senha padrão.

IP="192.168.100.1"
URL="http://$IP"
TOKEN=$(curl -sf $URL/asp/GetRandCount.asp)
curl -sf $URL/
| curl -sf $URL/resource/common/md5.js?20191022220012250237553184798
| curl -sf $URL/resource/common/RndSecurityFormat.js?20191022220012250237553184798
| curl -sf $URL/resource/common/safelogin.js?20191022220012250237553184798
| curl -sf $URL/resource/common/jquery.min.js?20191022220012250237553184798 > /dev/null

sleep 5
curl -sf -v -X POST -H "Host: $IP" -H "Content-Length: 110" -H "Cache-Control: max-age=0"\
-H "Upgrade-Insecure-Requests: 1" -H "Origin: $URL" -H "Content-Type: application/x-www-form-urlencoded"\
-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"\
-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9"\
-H "Referer: $URL/" -H "Accept-Encoding: gzip, deflate" -H "Accept-Language: en-US,en;q=0.9" -H "Connection: close"\
-b "Cookie=body:Language:english:id=-1" --data-binary "UserName=telecomadmin&PassWord=YWRtaW50ZWxlY29t&Language=english&x.X_HW_Token=$TOKEN" "$URL/login.cgi" > /dev/null
