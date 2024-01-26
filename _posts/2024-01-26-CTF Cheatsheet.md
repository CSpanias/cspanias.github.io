---
title: CTF Cheatsheet
date: 2024-01-26
categories: [Cheatsheet, CTF]
tags: [cheatsheet, ctf, capturetheflag, reverse-shell, shell, rce, hash, script, python, john, hashcat, suid]
img_path: /assets/cheatsheet
published: true
image:
    path: cheatsheetCover.png
---

> _Image taken from [CTF-CheatSheet](https://github.com/Rajchowdhury420/CTF-CheatSheet)._

## Port scanning

```bash
# HailMary port-scanning
sudo incursore.sh --type All -H $IP
# TCP SYN common ports scanning
sudo nmap -sS -A -Pn --min-rate 10000 $IP
# TCP SYN all ports scanning
sudo nmap -sS -A -Pn --min-rate 10000 -p- $IP
```

## Vulnerability scanning

```bash
# start nessus on WSL2
sudo /opt/nessus/sbin/nessus-service
```

## Web server enumeration

```shell
# view page-source
# check site's structure with ZAP/Burp

# check for WAF
nmap -Pn -p 443 --script http-waf-detect,http-waf-fingerprint $IP
wafw00f https://$IP

# check tech used (similar to Wappalyzer)
whatweb https://$IP

# check for robots file
curl https://$IP/robots
curl https://$IP/robots.txt

# banner grabbing
curl -IL https://$IP/

# dir-busting and file search
ffuf -u http://$domain/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -recursion -e .aspx,.html,.php,.txt,.jsp -c -ac
gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .aspx,.html,.php,.txt,.jsp
dirsearch -u http://$IP
nikto -h http://$IP
feroxbuster -u $URL

# subdomain-busting
gobuster dns -d $IP -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt 
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://$IP -H "HOST: FUZZ.$domain" -ac -c 
# vhost-busting
gobuster vhost -u $URL -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt --append-domain
# with local DNS as a resolver
$ gobuster dns -d $domain -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r $IP:53

# parameter enum
$ ffuf -u http://internal.analysis.htb/users/list.php?FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -ac
```

## File enumeration

### Linux

```bash
# search for SUID files
$ find / -perm -4000 2>/dev/null
$ find / -perm -u=s 2>/dev/null
```

If machine has a web server, check for database configuration files:

```bash
# searching for configuration files
/var/www/html$ find . | grep config
# searching for database-related strings within the configuration file
/var/www/html$ grep database <filePath>
```

## FTP

```shell
# bounce attack
$ nmap -Pn -v -n -p80 -b <username>:<pass>@<IP> <target2scan>

# brute-force
$ medusa -u <username> -P <passList> -h <IP> -M ftp
$ hydra -l <username> -P <passList> ftp://<IP> -t 48
```

## SSH

```shell
# check SSH for vulns
$ python3 /opt/ssh-audit/ssh-audit.py $IP
# brute-force creds
$ hydra -L <userList> -P <passwordList> ssh://$IP
```

## Hash cracking

> [Hashcat-examples](https://hashcat.net/wiki/doku.php?id=example_hashes)

```bash
# using hashcat's autodetect mode ('--username' if hashes are in <name:hash> format)
$ hashcat <hashes> /usr/share/wordlists/rockyou.txt --username
# brute-force hashes using the mode found
$ hashcat -m 3200 hashes /usr/share/wordlists/rockyou.txt --username
# show cracked hashes
$ hashcat -m 3200 --username --show hashes
```

> [John hash formats](https://pentestmonkey.net/cheat-sheet/john-the-ripper-hash-formats)

```bash
# list formats
$ john --list=formats
# brute-force
john <hashes> --wordlist=/usr/share/wordlists/rockyou.txt
```

## Shell stabilization

```bash
# shell stabilization using script
$ which script
which script
/usr/bin/script
$ script -O /dev/null -q /bin/bash
script -O /dev/null -q /bin/bash
$ bash
bash
$ ^Z
[1]+  Stopped                 nc -lvnp 1337

┌──(kali㉿CSpanias)-[~]
└─$ stty raw -echo; fg
nc -lvnp 1337

www-data@50bca5e748b0:/var/www/html$
```

```bash
# shell stabilization with Python
$ python3 -c 'import.pty;pty.spawn("/bin/bash")'
$ ^Z
[1]+  Stopped                 nc -lvnp 1337
# background shell
┌──(kali㉿CSpanias)-[~]
└─$ stty raw -echo; fg
```

Get values for the `rows` and `cols` variables from our attack host:

```bash
# get attack host's shell rows and cols values
$ stty -a
speed 38400 baud; rows 51; columns 209; line = 0;
<SNIP>
```

Set the same values on target:

```bash
www-data@50bca5e748b0:/var/www/html$ stty rows 51 cols 209
www-data@50bca5e748b0:/var/www/html$ export TERM=xterm
```