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

<!-- general overview of what this room is about -->

## Information Gathering

What we know beforehand:
1. Target's **IP address**.
2. Targets OS: **Linux**.
3. The room focus on **web app testing***.

Checklist:
- [x] 1 Port scanning
- [x] 2 Banner Grabbing

![nmap_scan](nmap-scan.png)
_List item 1_

![banner_grabbing](banner_grabbing.png)
_List item 2_{: .prompt-warning }

Next steps:
- [ ] Web enumeration
- [ ] SSH credentials

## Web enumeration

- [ ] 1 Check tools used
  + [ ] 1.1 Wappalyzer
  + [ ] 1.2 `whatweb`
- [ ] 2 View page source
  + [ ] 2.1 Enumerate `/nibbleblog` dir & search public exploits
    + [ ] 2.1.1 [CVE-2015-6967](https://nvd.nist.gov/vuln/detail/CVE-2015-6967)
    > works on < 4.0.5
    {: .prompt-warning }
    + [ ] 2.1.2 Metasploit module tested on 4.0.3
    > works on 4.0.3 & needs valid creds
    {: .prompt-warning }
- [ ] 3 Dir-busting
    + [ ] 3.1 Enumerate subdirectories


![wappalyzer](wappalyzer.png)
_List item 1.1_

![whatweb](whatweb.png)
_List item 1.2_

![page_source](web_server_page_source.png)
_List item 2_

> Add to checklist: Enumerate `/nibbleblog` dir & search public exploits. 
{: .prompt-warning }

![public_exploit](public_exploit.png)
_List item 2.1_

> [CVE-2015-6967](https://nvd.nist.gov/vuln/detail/CVE-2015-6967): _Unrestricted file upload vulnerability in the <u>My Image plugin</u> in Nibbleblog before 4.0.5 allows remote administrators to execute arbitrary code by uploading a file with an executable extension, then accessing it via a direct request to the file in content/private/plugins/my_image/image.php._
{: .prompt-info }

![msf_module](msf_exploit.png)
![msf_module_options](msf_exploit_options.png)
 _List item 2.1.2_

![gobuster_scan](gobuster-scan.png)
_List item 3_

![readme_subdir](nibbleblog_version.png)
_List item 3.1_