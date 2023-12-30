---
title: HTB - Starting Point Review 
date: 2023-11-19
categories: [Other, Review]
tags: [penetration-testing, starting-point, hackthebox, htb-academy, ctf, capture-the-flag, ethical-hacking, review]
img_path: /assets/htb-startingpoint/
mermaid: true
---

## TryHackMe vs. HackTheBox

For the past few months, I was intensively studying and practicing almost exclusively through the [Try Hack Me](https://tryhackme.com) (THM) platform. Within 3 months I completed, almost, 7 out of 9 learning paths that I had set as a goal, worked my way through numerous CTF rooms, and I was sitting at the top 2% rank.

![THM profile](thm_profile.png)

My initial plan was to "pause" my THM journey, as I wanted to enroll and start studying for the [Practical Junior Penetration Tester (PJPT)](https://certifications.tcm-sec.com/pjpt/) cert, but after exploring HTB's structure, I found it so intriguing, that I opted to go for the [Certified Penetration Testing Specialist (CPTS)](https://academy.hackthebox.com/preview/certifications/htb-certified-penetration-testing-specialist) instead. 

I have read numerous articles and seen many YouTube videos comparing THM and HTB, and everyone seemed to agree that **THM is aimed at absolute beginners** , while **HTB is considered a more advanced platform**. And I quickly understood why when I read the following while working through HTB's Penetration Testing job path:

> _Hack The Box was **initially created to give technical professionals a safe place to practice** and develop hacking skills and was not ideally suited for beginners starting their IT/Security journeys. Hack The Box began as **solely a competitive CTF platform** with a mix of machines and challenges, each awarding varying amounts of points depending on the difficulty, to be solved from a "black box" approach, with **no walkthrough, guidance, or even hints**._

Luckily for beginners, like myself, HTB is presently a lot more than the above description. It now consists of various elements, such as: [Hacking Labs](https://www.hackthebox.com/hacker/hacking-labs), [Pro Hacking Labs](https://www.hackthebox.com/hacker/pro-labs), [Hacking Battlegrounds](https://www.hackthebox.com/hacker/hacking-battlegrounds), [CTFs](https://www.hackthebox.com/hacker/ctf), and the [HTB Academy](https://academy.hackthebox.com/). The latter aims to teach everything, from fundamental concepts and tools, such as **basic networking** and **how to use nmap**, to advanced concepts, like **how to attack an enterprise network** from start to finish and **how to document the whole process** while doing it.

![htb products](htb-products.png){: width="70%"}

My HTB journey is now under way and, hopefully, I will soon be writing another post for my experience on completing the [Penetration Test job path](https://academy.hackthebox.com/path/preview/penetration-tester) as well as for the CPTS exam itself.

> You can find the rationale behind why one can't sit directly for the CPTS without having completed the associated job path on [this](https://youtu.be/noieqyKdMQg?t=1165) amazing discussion between [John Hammond](https://johnhammond.llc/) and [Dimitrios Bougioukas](https://www.linkedin.com/in/dbougioukas/), HTB's Academy Director.
{: .prompt-info }

When I first logged in on the HTB platform, it suggested to me to go through the [Starting Point](https://app.hackthebox.com/starting-point):

![htb-starting-point](htb-starting-point.jpg)

> _**Starting Point** is **Hack The Box on rails**. It's a **linear series of Boxes tailored to absolute beginners** and features very easy exploit paths to not only introduce you to our platform but also **break the ice into the realm of penetration testing**. Using the Starting Point, you can **get a feel for how Hack The Box works**, how to connect and interact with Boxes, and **pave a basic foundation for your hacking skills to build off of**._

I just completed all 3 tiers of the Starting Point, and I was so impressed by the **well thought out structure** and the **exceptionally well-written walkthroughs**, that I decided to write a quick post and, hopefully, let more people know about it!

My goal is to provide a very brief overview of each tier and highlight the differences among them.

## The Key is a Strong Foundation - Tier 0

According to HTB, the goal of this tier is to:

> *Cover the absolute **fundamentals of attacking a Box**. You'll learn **how to connect to the VPN**, perform **basic enumeration of ports and services**, and **interact with the services you find**. Each Box in this Tier is focused on a particular tool or service and contains only a single primary step.*


Tier 0 contained 8 rooms in total and the final task of each machine was to find a single flag, the `flag.txt` file. Each machine included a walkthrough that was similary structured, and, usually, consisted of three sections:
1. **Introduction**: General information for setting up the room's context.
2. **Enumeration**: How to use `nmap` for port scanning and how to perform service-specific enumeration.
3. **Foothold**: How to interact with the service found.

![Tier 0 walkthrough](tier0-walkthrough.jpg)

An overview of each room is presented below:

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

This tier does just what it says: emphasizes **basic enumeration using** `nmap`, which starts from just a basic scan and ends up using various options, such as `-sC`, `-sV`, `-p-` and `--min-rate`, and **service-specific interaction**. 

The **walkthroughs here are relatively short**, from 4 to 12 pages, so it does not dive deep in any of the concepts mentioned, but gives just enough information so someone can understand what is happening on each room.

## You Need to Walk Before You Can Run - Tier 1

Moving on to tier 1, the difficulty started to ramp up and some rooms seemed a bit more challenging than expected, given the fact that are rated as **very easy**:

> _...things are kicked up a notch and a bit more complexity is introduced. Tier 1 focuses on **fundamental exploitation techniques**. While **the depth of the material in this Tier is increased** over the previous, these **Boxes** still feature a single primary exploitation step._

This tier included 10 rooms in total and the final task was the same as before, i.e., finding `flag.txt`. The walkthroughs were similarly structured, but they increased in complexity and size, ranging from 8 up to 19 pages.

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

A lot of more concepts were introduced, the depth of each walkthough was increased, and the number of tools used per machine grew from just 1-2 to 2-6. 

As I have already mentioned, **the quality of the walkthroughs is top-notch**. Personally, I always took my time with each machine, and progressed slowly until I was confident that I understoond what I was doing on each step. More than once, in particular when I encountered a concept for the first time, I went over a machine multiple times. 

For example, for the Funnel room:
1. The first time, I worked along the walkthrough, making detailed notes on the side. I completed the machine, but I was still having a hard time understanding how **remote and dynamic port forwarding** worked.
2. I took a step back, read some more articles, such as [this](https://iximiuz.com/en/posts/ssh-tunnels/) excellent visual guide to SSH Tunnels and [this](https://www.youtube.com/watch?v=N8f5zv9UUMI) video tutorial, until I got some clarity. At the same time, I expanded and refined my notes.
3. Armed with a better understanding, I restarted Funnel and went over and practiced the parts that were not very clear at first, in this case, both **dynamic and local port forwarding**.

![funnel-room](funnel-room.png)

> Most walkthroughs include links to HTB academy modules that are relevant to the room. Funnel was one of the few that did not, but after a quick search on the HTB Academy I found the [Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/module/details/158) module, which they might forgot to link to the machine.
{: .prompt-info }

## Tier 2

Tier 2 included 7 rooms, the walkthroughs grew a bit more, ranging from 14 up to 23 pages, and, of course, the difficulty increased further.

> _This is the final Tier, and the **most complex**. The Boxes in Tier 2 are **full-fledged, and chain multiple steps together**. You'll need to enumerate, gain an initial foothold, and escalate your privileges to reach root/system. Unlike in the previous Tiers, these Boxes have **two flags**, `user.txt` and `root.txt`._

Here is an overview of the tier 2 machines:

| Room | Concept | Service | Tool(s) |
|:-----------------------------|:-----------------|
| Archetype | xp_cmdshell, automated enumeration | SMB, ms-sql-s | `nmap`, `smbclient`, `mssqlclient.py`, `nc`, winPEAS, `psexec.py` | 
| Oopsie | Web crawling, cookie tampering, information disclosure, webshell, dir busting, shell stabilization, suid | HTTP | `nmap`, Burp Suite, `gobuster`, `find`, `grep` |
| Vaccine | Password-protected files, hashes, SQLi, cookie stealing, RCE | FTP, HTTP | `nmap`, `zip2john`, `john`, crackstation, `sqlmap`, cookie-editor, GTFOBins |
| Unified | Log4J, UniFi, OS Command Injection, RCE, hashes | HTTP, MongoDB | `nmap`, Burp Suite, `tcpdump`, rogue-jndi, `nc`, `mongo` |
| Included | UDP, LFI, RCE, containers | TFTP, HTTP |  `nmap`, `curl`, `tfpt`, `lxc`, HackTricks  |
| Markup | XXE, SSH keys, Windows permissions, RCE | HTTP, SSH |  `nmap`, Burp Suite, HackTricks, WinPEAS |
| Base | Dir-busting, swap files, PHP functions, RCE, URL encoding | HTTP, SSH |  `nmap`, `gobuster`, Burp Suite, GTFOBins |

When I entered this level, I had already started studying through the [Penetration Tester](https://academy.hackthebox.com/path/preview/penetration-tester) job path for the CPTS, so I took a slighly different approach than the previous tiers:
1. I spawned the machine and just noted down the IP address; I didn't look at any of the room questions. 
2. I tried to enumerate it to the best of my abilities and went as far as I could.
2. If I couldn't make any progress for about 30-45 minutes, I then looked at the questions, which, more often than not, they worked like hints. 
3. If after looking the questions I was still stuck, I then read the walkthrough until I got myself unstuck.
4. Then, I started working alone again, and in case I got stuck again, I repeated the process until I solved the box.

As a result, it took me, on average, **2.5 hours to solve a (very easy!!!) box**. While working through this tier, I also implemented [Tyler Ramsbey](https://www.youtube.com/@TylerRamsbey)'s advice and started making a to-do list for each port/service I found, to made sure that I was not forgetting to check anything and, most importantly, to have a plan beforehand and not spend too long on a potential rabithole. 

For example, if the machine has an HTTP(S) server, I know beforehand what I want to do. Obviously, this list serves as a starting point, and it expands with info and tasks as I am working through the machine. I found handy to also have the commands right below as it makes the process far more efficient:

![Web Enumeration Checklist](web_enum_checklist.png)

> The **to-do list** methodology helped me tremendously in progressing through each box and developing the **intuition of having an attack plan ready as soon as I saw a service**. In addition, as I did it while working through a machine, it helped me a lot with generating **documentation** which was a big bonus.
{: .prompt-info }

## Conclusion

As a conclusion, having spend some time on both THM and HTB, I can't say that it is a matter of which is best, but rather which suits someone's goals best. I wanted to sit for an entry-level certification while having the chance to practice on CTFs, and HTB ticks both boxes. Having said that, I will almost certainly rejoin THM once I get the CPTS, and I will try to be active in both platforms. 

The only unpleasant surprise I encountered so far on HTB is that the walkthroughs for the retired machines do not seem to be on the same level as those written for Starting Point's machines. To be fair, I have just done two boxes, [Nibbles](https://app.hackthebox.com/machines/121) and [Broker](https://app.hackthebox.com/machines/578), so I will have a better opinion when I have a bigger sample.

One reason for that might be that there is an extensive video-walkthrough from [IppSec](https://www.youtube.com/@ippsec) on every box as well as a shorter written walkthrough from [0xdf](https://0xdf.gitlab.io/), so I shouldn't really complain, should I???

![Starting Point badges](starting_point_badges.png)