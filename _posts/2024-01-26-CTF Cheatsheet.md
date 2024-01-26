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

Hailmary scan
```bash
sudo incursore.sh --type All -H $IP
```
TCP SYN common ports scanning
```bash
sudo nmap -sS -A -Pn --min-rate 10000 $IP
```
TCP SYN all ports scanning
```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- $IP
```

## Vulnerability scanning

Start nessus on WSL2
```bash
sudo /opt/nessus/sbin/nessus-service
```

## Web server enumeration

Check for WAF
```shell
nmap -Pn -p 443 --script http-waf-detect,http-waf-fingerprint $IP
```
```bash
wafw00f https://$IP
```

Check for tech used (similar to Wappalyzer)
```bash
whatweb https://$IP
```

Check for robots file
```bash
curl https://$IP/robots
```
```bash
curl https://$IP/robots.txt
```

Banner grabbing
```bash
curl -IL https://$IP/
```

Dir-busting and file search
```bash
ffuf -u http://$domain/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -recursion -e .aspx,.html,.php,.txt,.jsp -c -ac
```
```bash
gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .aspx,.html,.php,.txt,.jsp
```
```bash
dirsearch -u http://$IP
```
```bash
nikto -h http://$IP
```
```bash
feroxbuster -u $URL
```

Subdomain-busting
```bash
gobuster dns -d $IP -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```
```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://$IP -H "HOST: FUZZ.$domain" -ac -c
```

Vhost-busting
```bash
gobuster vhost -u $URL -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt --append-domain
```
With local DNS as a resolver
```bash
gobuster dns -d $domain -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r $IP:53
```

Parameter enum
```bash
ffuf -u http://internal.analysis.htb/users/list.php?FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -ac
```

## Kernel vulns

kernel's version
```bash
uname -a
```

## File enumeration

### Linux

SUIDS
```bash
find / -perm -4000 2>/dev/null
```
```bash
find / -perm -u=s 2>/dev/null
```

If web server --> check for database config files:

```bash
/var/www/html$ find . | grep config
```

Searching for db-related strings within config file
```bash
/var/www/html$ grep database <filePath>
```

## FTP

Bounce attack
```shell
nmap -Pn -v -n -p80 -b <username>:<pass>@<IP> <target2scan>
```

Brute-force
```bash
medusa -u <username> -P <passList> -h <IP> -M ftp
```
```bash
hydra -l <username> -P <passList> ftp://<IP> -t 48
```

## SSH

Check for SSH vulns
```shell
python3 /opt/ssh-audit/ssh-audit.py $IP
```

Brute-force creds
```bash
hydra -L <userList> -P <passwordList> ssh://$IP
```

## Hash cracking

> [Hashcat-examples](https://hashcat.net/wiki/doku.php?id=example_hashes)

Autodetect mode ('--username' if hashes are in <name:hash> format)
```bash
hashcat <hashes> /usr/share/wordlists/rockyou.txt --username
```

Brute-force hashes using the mode found above
```bash
hashcat -m 3200 hashes /usr/share/wordlists/rockyou.txt --username
```

Show cracked hashes:
```bash
hashcat -m 3200 --username --show hashes
```

> [John hash formats](https://pentestmonkey.net/cheat-sheet/john-the-ripper-hash-formats)

List formats
```bash
john --list=formats
```

Brute-force
```bash
john <hashes> --wordlist=/usr/share/wordlists/rockyou.txt
```

## Shell stabilization

Using `script`
```bash
script -O /dev/null -q /bin/bash
```
```bash
bash
```

Using Python
```bash
python3 -c 'import.pty;pty.spawn("/bin/bash")'
```

Config shell
```bash
^Z
[1]+  Stopped                 nc -lvnp 1337
```
```bash
stty raw -echo; fg
```

Get values for the `rows` and `cols` variables from our attack host
```bash
stty -a
```

Set values on target

```bash
www-data@50bca5e748b0:/var/www/html$ stty rows 51 cols 209
```

Export TERM
```bash
www-data@50bca5e748b0:/var/www/html$ export TERM=xterm
```