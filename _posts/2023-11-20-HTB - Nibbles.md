---
title: HTB - Nibbles
date: 2023-11-20
categories: [CTF Write Up, HTB]
tags: []
img_path: /assets/nibbles/
---

![room_banner](nibbles_banner.png)

## Overview

[Nibbles](https://www.hackthebox.com/machines/nibbles) was the first **easy** HTB target that I pwned, and probably the majority of HTB users as well, as it was used as an example at the [Penetration Test](https://academy.hackthebox.com/path/preview/penetration-tester) job path.

> _Nibbles is a fairly simple machine, however with the inclusion of a login blacklist, it is a fair bit more challenging to find valid credentials. Luckily, a username can be enumerated and guessing the correct password does not take long for most._

## Information Gathering

What we know beforehand:
1. Target's **IP address**.
2. Targets OS: **Linux**.
3. The room focus on **web app testing**.

Checklist:
- [x] 1 Port scanning
- [x] 2 Banner Grabbing

1 Port scanning

<figure>
    <img src="nmap-scan.png" width="70%"
    alt="Nmap scan results" >
</figure>

2 Banner grabbing

<figure>
    <img src="banner_grabbing.png"
    alt="Banner grabbing with netcat" >
</figure>

Next steps:
- Web enumeration
- SSH credentials

## Web enumeration

Checklist:
- [x] 1 Check tools used
  + [x] 1.1 Wappalyzer
  + [x] 1.2 `whatweb`
- [x] 2 View page source
  + [x] 2.1 Enumerate `/nibbleblog` dir & search public exploits
    + [x] 2.1.1 [CVE-2015-6967](https://nvd.nist.gov/vuln/detail/CVE-2015-6967)
    > works on < 4.0.5
    {: .prompt-warning }
    + [ ] 2.1.2 Metasploit module tested on 4.0.3
    > works on 4.0.3 & needs valid creds --> `image.php` cleanup error
    {: .prompt-warning }
- [x] 3 Dir-busting
  + [x] 3.1 Enumerate subdirectories 
- [x] 4 Upload a [PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) directly on `My Image` plugin. 

1 Checking technologies used

<figure>
    <img src="wappalyzer.png" width="80%"
    alt="Wappalyzer technologies" >
</figure>

<figure>
    <img src="whatweb.png"
    alt="whatweb technologies" >
</figure>

2 Viewing page source

<figure>
    <img src="web_server_page_source.png" width="60%"
    alt="Homepage's page source" >
</figure>

> Add to checklist: Enumerate `/nibbleblog` dir & search public exploits. 
{: .prompt-warning }

2.1 Searching for public exploits

<figure>
    <img src="public_exploit.png" width="60%"
    alt="Nibbleblog public exploit" >
</figure>

> [CVE-2015-6967](https://nvd.nist.gov/vuln/detail/CVE-2015-6967): _Unrestricted file upload vulnerability in the <u>My Image plugin</u> in Nibbleblog before 4.0.5 allows remote administrators to execute arbitrary code by uploading a file with an executable extension, then accessing it via a direct request to the file in content/private/plugins/my_image/image.php._
{: .prompt-info }

2.1.2 Metasploit module

<figure>
    <img src="msf_exploit.png" width="75%"
    alt="Metasploit module options" >
</figure>

<figure>
    <img src="msf_exploit_options.png" width="85%"
    alt="Metasploit module options" >
</figure>

3 Dir-busting

<figure>
    <img src="gobuster-scan.png" width="80%"
    alt="Gobuster's scan results" >
</figure>

3.1 Enumerating subdirectories

<figure>
    <img src="nibbleblog_version.png" width="80%"
    alt="README subdirectory-Nibbleblog's version" >
</figure>

> Nibbleblog v4.0.3 --> Metasploit module, need to find creds.

<figure>
    <img src="users_xml.png" width="70%"
    alt="content subdirectory-users.xml file" >
</figure>

> Username, `admin`, obtained, still missing password for Logging in & Metasploit. After trying several passwords, `admin:nibbles` works.

2.1.2 Metasploit's module erroring

<figure>
    <img src="msf_manual_cleanup.png" width="70%"
    alt="Metasploit error message" >

</figure>

> MSF error: tried re-installing `My Image` plugin, and although `image.php` is not there, still same error.

4 Uplading a PHP reverse shell

<figure>
    <img src="my_img_plugin_config.png" width="85%"
    alt="My Image plugin configurations" >
</figure>

<figure>
    <img src="shell_upload.png" width="85%"
    alt="Shell upload" >
</figure>

<figure>
    <img src="revshell_success.png" width="85%"
    alt="Reverse shell obtained" >
</figure>

## Initial Foothold

Checklist:
- [x] 1 Stabilize shell
- [x] 2 Search for `user.txt`
- [x] 3 Check current user's privileges

1 Stabilize shell & 2 Search for `user.txt`

<figure>
    <img src="upgrading_shell_user_flag.jpg" width="50%"
    alt="Upgrading revese shell and getting user flag" >
</figure>

3 Checking current user's privs

<figure>
    <img src="sudo_l.png" width="70%"
    alt="Checking current user's privileges" >
</figure>

> `nibbles` can run `monitor.sh` as `root` with no pass. Exploit it to get a root shell.
{: .prompt-tip }

## Privilege Escalation

Checklist:
- [x] 1 Try to exploit `monitor.sh`
- [x] 2 Search for `root.txt`

1 `monitor.sh` exploitation

<figure>
    <img src="personal_zip.png" width="70%"
    alt="Personal_zip file" >
</figure>

<figure>
    <img src="script_perms.png" width="70%"
    alt="Checking script's permissions" >
</figure>

<figure>
    <img src="root_shell_code.png"
    alt="Adding root shell code" >
</figure>

2 Searching for `root.txt`

<figure>
    <img src="root_shell_root_txt.jpg" width="65%"
    alt="Getting root shell and root.txt" >
</figure>

<figure>
    <img src="nibbles.png" width="70%"
    alt="Nibbles machine pwnd" >
</figure>



