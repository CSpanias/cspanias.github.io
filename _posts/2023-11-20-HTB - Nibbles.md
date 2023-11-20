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

![nmap_scan](nmap-scan.png)
_List item 1_

![banner_grabbing](banner_grabbing.png)
_List item 2_{: .prompt-warning }

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


![wappalyzer](wappalyzer.png)
_List item 1.1_

![whatweb](whatweb.png)
_List item 1.2_

![page_source](web_server_page_source.png){: width="50%"}
_List item 2_

> Add to checklist: Enumerate `/nibbleblog` dir & search public exploits. 
{: .prompt-warning }

![public_exploit](public_exploit.png){: width="60%"}
_List item 2.1_

> [CVE-2015-6967](https://nvd.nist.gov/vuln/detail/CVE-2015-6967): _Unrestricted file upload vulnerability in the <u>My Image plugin</u> in Nibbleblog before 4.0.5 allows remote administrators to execute arbitrary code by uploading a file with an executable extension, then accessing it via a direct request to the file in content/private/plugins/my_image/image.php._
{: .prompt-info }

![msf_module](msf_exploit.png)
![msf_module_options](msf_exploit_options.png)
 _List item 2.1.2_

![gobuster_scan](gobuster-scan.png){: width="60%"}
_List item 3_

![readme_subdir](nibbleblog_version.png)
_List item 3.1_

> Nibbleblog v4.0.3 --> Metasploit module, need to find creds.

![users_xml_file](users_xml.png)
_List item 3.1_

> Username, `admin` obtained, still missing password for Logging in & Metasploit. After trying several passwords, `admin:nibbles` works.

![msf_error](msf_manual_cleanup.png)

> MSF error: tried re-installing `My Image` plugin, and although `image.php` is not there, still same error.

![My_image_plugin_config](my_img_plugin_config.png)
_List item 4_

![shell_upload](shell_upload.png)
_List item 4_

![revshell_success](revshell_success.png)
_List item 4_

## Initial Foothold

Checklist:
- [x] 1 Stabilize shell
- [x] 2 Search for `user.txt`
- [x] 3 Check current user's privileges

![upgrading_shell_user_flag](upgrading_shell_user_flag.jpg)
_List item 1 & 2_

![sudo_l](sudo_l.png)
_List item 3_

## Privilege Escalation

Checklist:
- [x] 1 Try to exploit `monitor.sh`
- [x] 2 Search for `root.txt`

![personal_zip](personal_zip.png)
_List item 1_

> `nibbles` can run `monitor.sh` as `root` with no pass. Exploit it to get a root shell.
{: .prompt-tip }

![script_perms](script_perms.png)
_List item 1_

![root_shell_code](root_shell_code.png)
_List item 1_

![root_shell_root_txt](root_shell_root_txt.jpg)
_List item 2_

![nibbles_pwnd](nibbles.png)