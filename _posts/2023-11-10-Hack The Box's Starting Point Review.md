---
title: Hack The Box's Starting Point Review 
date: 2023-11-10
categories: [Review, HTB]
tags: [nmap, telnet, ftp, smb, redis, apache, rdp, dir-busting, mongodb, rsync]
img_path: /assets/htb-startingpoint/
mermaid: true
---

## Introduction

For the past few months, I was intensively studying and practicing almost exclusively through the [Try Hack Me](https://tryhackme.com) (THM) platform. I have completed 6 out of 9 learning paths that I have set as a target - I am currently working on [Red Teaming](https://tryhackme.com/paths) - as well as worked my way through numerous CTF rooms. 

I realised that I was spending far too much time on just one resource, so I recently decide to also joined the [HTB](https://app.hackthebox.com/home) platform. 

![THM and HTB profiles](site-profiles.png)

I have read numerous articles and seen many YouTube videos performing comparisons between THM and HTB, and everyone seemed to agree on the following: 

> **THM is aimed at absolute beginners** , while **HTB is considered a more advanced platform**. 

I think that is because HTB used to only have machines to "hack" with absolutely no guidance, but this is very much not the case now. 

HTB contains many different things nowadays: [Hacking Labs](https://www.hackthebox.com/hacker/hacking-labs), [Pro Hacking Labs](https://www.hackthebox.com/hacker/pro-labs), [Hacking Battlegrounds](https://www.hackthebox.com/hacker/hacking-battlegrounds), [CTFs](https://www.hackthebox.com/hacker/ctf), and also the [HTB Academy](https://academy.hackthebox.com/) which aims to teach everything, from fundamentals concepts and tools, such as **basic networking** and **how to use nmap**, to advanced concepts, like **how to attack an enterprise network** from start to finish and **how to document the whole process** while doing it.

![htb products](htb-products.png){: width="70%"}

I now have a montly student subscription for both THM and HTB, which costs £12 and £10, respectively, and my plan is to continue learning via THM until I, at least, achieve my goals, while perfroming my practical work on HTB. 

Having read the aforementioned comparisons, I was expecting to have a really hard time on starting out at HTB and I was ready to hit many roadblocks straight away. But it proved quite the opposite!

When I first logged in on the HTB platform, it suggested to me to go through its [**Starting Point**](https://app.hackthebox.com/starting-point), which according to HTB: 

> _**Starting Point** is **Hack The Box on rails**. It's a **linear series of Boxes tailored to absolute beginners** and features very easy exploit paths to not only introduce you to our platform but also **break the ice into the realm of penetration testing**. Using the Starting Point, you can **get a feel for how Hack The Box works**, how to connect and interact with Boxes, and **pave a basic foundation for your hacking skills to build off of**._

I was so impressed by the **well thought out structure** and the **exceptionally well-written walkthroughs**, that I decided to write a quick post about it, and, hopefully, let other people now about it.

![htb-starting-point](htb-starting-point.jpg)

## Tier 0

According to HTB, the goal of this level is to:

> *Cover the absolute **fundamentals of attacking a Box**. You'll learn **how to connect to the VPN**, perform **basic enumeration of ports and services**, and **interact with the services you find**. Each Box in this Tier is focused on a particular tool or service and contains only a single primary step.*

![tier0](tier-0-completed.png)

This tier contains 8 rooms in total and the final task of each machine is to find a single flag, the `flag.txt` file. Each machine includes a walkthrough that is similary structured, and, usually, contains three sections:
1. **Introduction**: General information for setting up the room's context.
2. **Enumeration**: How to use `nmap` for port scanning and how to perform service-specific enumeration.
3. **Foothold**: How to interact with the service found.

![Tier 0 walkthrough](tier0-walkthrough.jpg)

You can find an overview of each room below:

| Room | Concept | Service | Tool(s) |
|:-----------------------------|:-----------------|
| Meow | Pwnbox/VPN, enumeration | telnet | `nmap` | 
| Fawn | ports, SSL/TLS | FTP | `nmap`, `ftp` |
| Dancing | SMB, OSI model | smb | `nmap`, `smbclient` |
| Reedemer | Key-value in-memory NoSQL databases | Redis | `nmap`, `redis-cli` |
| Explosion | Remote access tools | RDP |  `nmap`, `xfreerdp` |
| Preignition | Web servers, dir busting | HTTP |  `nmap`, `gobuster`|
| Mongod | Document-oriented NoSQL databases | mongodb |  `nmap`, `mongodb` |
| Synced | File transfer services | rsync |  `nmap`, `rsync` |

As you can see, this tier does just what it says: emphasizes **basic enumeration using** `nmap`, which starts from just a basic scan and ends up using various options, such as `-sC`, `-sV`, `-p-` and `--min-rate`, and **service-specific interaction**. 

The **walkthroughs here are relatively short**, from 4 to 12 pages, so it does not dive deep in any of the concepts mentioned, but gives just enough information to start with.

## Tier 1

Moving on to tier 1:

> ...things are kicked up a notch and a bit more complexity is introduced. Tier 1 focuses on **fundamental exploitation techniques**. While **the depth of the material in this Tier is increased** over the previous, these **Boxes** still feature a single primary exploitation step.

![tier1](tier-1-completed.png)

This tier contains 10 rooms in total and the final task is the same as before, i.e., finding `flag.txt`. The walkthroughs are similarly structured, but they increase in complexity and size, from 8 up to 19 pages.

Here is an overview of the rooms included on this level:

| Room | Concept | Service | Tool(s) |
|:-----------------------------|:-----------------|
| Appointment | SQLi | HTTP | `nmap`, `gobuster`, SQL | 
| Sequel | MariaDB | mysql | `nmap`, `mysql` |
| Crocodile | Chaining together attack vectors, dir busting  | FTP, HTTP | `nmap`, `ftp`, Wappalyzer, `gobuster` |
| Responder | Name-Based Virtual Hosting, LFI, RFI, path traversal, NTLM, hash cracking | HTTP, WinRM | `nmap`, Responder, `john`, `evil-winrm` |
| Three | AWS S3 buckets, subdomains, virtual-host routing, dir busting, webshells | SSH, HTTP |  `nmap`, Wappalyzer, `gobuster`, `awscli`, `nc`, `curl` |
| Ignition | Name-Based Virtual Hosting, DNS, dir busting  | HTTP |  `nmap`, `curl`, `gobuster` |
| Bike | Node.js, XSS, template engines, SSTI, URL encoding | HTTP, SSH |  `nmap`, Wappalyzer, Burp Suite |
| Funnel | Port forwarding, SOCKS5, password spraying, interal network enumeration | SSH, FTP, postgresql |  `nmap`, `hydra`, `ss`, `psql`, `proxychains` |
| Pennyworth | Jenkins, groovy scripts, RCE | HTTP |  `nmap`, `nc` |
| Tactics | Firewalls, Impacket | SMB |  `nmap`, `smbclient`, `psexec.py` |

As you can see, a lot of more concepts are introduced, the depth of each walkthough increases, and the number of tools used per machine grows from just 1-2 to 2-6. 

As I have already mentioned, the quality of the walkthroughs is top-notch. Personally, I am always taking my time with each machine, so I can make sure that I understand what I am doing on each step. It is not uncommon, in particular when I encounter concepts for the first time, to go over a machine many times. 

For instance, for the Funnel room:
1. The first time, I worked along the walkthrough, making detailed notes on the side. I completed the machine, but the concepts of **remote and dynamic port forwarding** were not entirely clear on my head.
2. Took a step back, read some more articles, such as [this](https://iximiuz.com/en/posts/ssh-tunnels/) excellent visual guide to SSH Tunnels, until I got clarity. At the same time, I refined my notes.
3. Armed with a better understanding, I restarted Funnel and went over the parts that was not very clear at first, in this case, getting the flag with **dynamic port forwarding** instead of **local port forwarding**.

Most walkthroughs include links to HTB academy modules that are relevant to the room. Funnel was one of the few that did not, but after I manually searched I found the [Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/module/details/158) module, which they might forget to link. Unfortunately, I do not currently have an HTB Academy subscription or enough cubes to unlock its content, but I am pretty confident that its quality would be great!

![](tunneling-module.png)


## Tier 2

> This is the final **Tier**, and the most complex. The **Boxes** in **Tier 2** are full-fledged, and chain multiple steps together. You'll need to enumerate, gain an initial foothold, and escalate your privileges to reach root/system. Unlike in the previous **Tiers**, these **Boxes** have two flags, **`user.txt`** and **`root.txt`**.

| Room | Concept | Service | Tool(s) |
|:-----------------------------|:-----------------|
| Archetype | Reverse shell, privilege escalation, automated enumeration | SMB, ms-sql-s | `nmap`, `smbclient`, `mssqlclient.py`, `nc`, winPEAS, `psexec.py` | 
| Oopsie | Web crawling, cookie tampering, information disclosure, webshell, dir busting, shell stabilization, suid | HTTP | `nmap`, Burp Suite, `gobuster`, `find`, `grep` |
| Vaccine |   |  | `nmap` |
| Unified |  |  | `nmap` |
| Included |  |  |  `nmap` |
| Markup |  |  |  `nmap`|
| Base |  |  |  `nmap` |


## Conclusion