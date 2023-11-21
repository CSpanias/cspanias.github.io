---
title: HTB - Keeper
date: 2023-11-21
categories: [CTF Write Up, HTB]
tags: []
img_path: /assets/keeper/
published: true
---

![room_banner](keeper_banner.png)

## Overview

|:-:|:-:|
|Machine|[Keeper](https://app.hackthebox.com/machines/556)
|Rank|Easy|
|Time|3h19m|
|Focus|Default credentials, [CVE-2023-32784](https://nvd.nist.gov/vuln/detail/CVE-2023-32784)

## Information Gathering

```shell
# live host discovery
sudo nmap -PA -sn $IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2023-11-21 16:26 GMT
Nmap scan report for 10.10.11.227
Host is up (0.024s latency).
Nmap done: 1 IP address (1 host up) scanned in 1.26 seconds
```

```shell
# scanning common ports
sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 $IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2023-11-21 16:29 GMT
Nmap scan report for 10.10.11.227
Host is up (0.025s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 35:39:d4:39:40:4b:1f:61:86:dd:7c:37:bb:4b:98:9e (ECDSA)
|_  256 1a:e9:72:be:8b:b1:05:d5:ef:fe:dd:80:d8:ef:c0:66 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.18.0 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94SVN%E=4%D=11/21%OT=22%CT=1%CU=32880%PV=Y%DS=2%DC=I%G=Y%TM=655
OS:CDAF8%P=x86_64-pc-linux-gnu)SEQ(SP=FC%GCD=1%ISR=105%TI=Z%CI=Z%II=I%TS=A)
OS:SEQ(SP=FC%GCD=1%ISR=106%TI=Z%CI=Z%II=I%TS=A)OPS(O1=M53CST11NW7%O2=M53CST
OS:11NW7%O3=M53CNNT11NW7%O4=M53CST11NW7%O5=M53CST11NW7%O6=M53CST11)WIN(W1=F
OS:E88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)ECN(R=Y%DF=Y%T=40%W=FAF0%O=M
OS:53CNNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T
OS:4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+
OS:%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y
OS:%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%
OS:RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.75 seconds
```

## Web Enumeration

```shell
whatweb http://10.10.11.227
http://10.10.11.227 [200 OK] Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], IP[10.10.11.227], nginx[1.18.0]
```

```shell
curl http://10.10.11.227
<html>
  <body>
    <a href="http://tickets.keeper.htb/rt/">To raise an IT support ticket, please visit tickets.keeper.htb/rt/</a>
  </body>
</html>
```

> Add `tickets.keeper.htb` to `/etc/hosts`.

<figure>
    <img src="hosts_file.png"
    alt="/etc/hosts file" >
</figure>

<figure>
    <img src="wappalyzer.png"
    alt="Wappalyzer report" >
</figure>

```shell
# banner grabbing
curl -IL http://$IP/
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 21 Nov 2023 16:42:35 GMT
Content-Type: text/html
Content-Length: 149
Last-Modified: Wed, 24 May 2023 14:04:44 GMT
Connection: keep-alive
ETag: "646e197c-95"
Accept-Ranges: bytes
```

<figure>
    <img src="tickets_home.png"
    alt="Tickets.keeper.htb homepage - Login form" >
</figure>

> RT 4.4.4 (out-of-date), latest 5.0.5, [release notes](https://docs.bestpractical.com/release-notes/rt/5.0.5) include 3 CVEs.

<figure>
    <img src="default_creds_google.png"
    alt="Googling default credentials for Request tracker" >
</figure>

<figure>
    <img src="rt_logged_in.png"
    alt="Logged in with default credentials" >
</figure>

<figure>
    <img src="user_details.png"
    alt="Enumeration users on the website" >
</figure>

## Initial Foothold

