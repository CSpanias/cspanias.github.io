---
title: HTB - Broker
date: 2023-11-10
categories: [CTF Write Up, HTB]
tags: [nmap, default-credentials, activemq, cve-2023-46604, metasploit]
img_path: /assets/broker/
published: true
---

![room_banner](machine_banner.png)

## Overview

|:-:|:-:|
|Machine|[Broker](https://app.hackthebox.com/machines/578)|
|Rank|Easy|
|Time|-|
|Focus|Default creds, CVEs, activemq|

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

## 1. Initial Enumeration

What we know:
- Target IP: 10.10.11.243
- tun0: 10.10.14.11
- OS: Linux
- Web server focused

<figure>
    <img src="nmap-common.png"
    alt="Nmap port-scanning results" >
</figure>

> Confirm port services with banner grabbing:

<figure>
    <img src="banner_grabbing.png"
    alt="Banner grabbing with nc" >
</figure>

## 2. Web Server Enumeration

<figure>
    <img src="homepage.png"
    alt="Broker's homepage" >
</figure>

> `admin:admin` worked!

## 3. Initial Foothold

<figure>
    <img src="admin_panel.png"
    alt="Logged in as admin" >
</figure>

```wappalyzer
Nginx 1.18.0
C ?
Ubuntu
Reverse Proxies: Nginx 1.18.0
```

<figure>
    <img src="whatweb.png"
    alt="Whatweb report" >
</figure>

> Management tab reveals version:

<figure>
    <img src="activemq_version.png"
    alt="ACTIVEMQ's version" >
</figure>

> [CVE-2023-46604](https://nvd.nist.gov/vuln/detail/CVE-2023-46604)

<figure>
    <img src="cve.png"
    alt="CVE-2023-46604" >
</figure>

> There is a [msf module](https://www.rapid7.com/db/modules/exploit/multi/misc/apache_activemq_rce_cve_2023_46604/) for that. [AttackerDB](https://attackerkb.com/topics/IHsgZDE3tS/cve-2023-46604/rapid7-analysis)'s explanation.  
> [PoC](https://github.com/SaumyajeetDas/CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ).

<figure>
    <img src="broker_pwned.png"
    alt="Cozy machine pwned" >
</figure>