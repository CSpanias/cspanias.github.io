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

I have read numerous articles and seen many YouTube videos performing comparisons between THM and HTB, and everyone seemed to agree on the following: 

> THM is aimed at absolute beginners as it includes a lot of "handholding", while HTB is considered a platform for more advanced users. 

I think that is because HTB used to only have machines to "hack" with absolutely no guidance, but this is very much not the case now. 

HTB contains many different things nowadays: [Hacking Labs](https://www.hackthebox.com/hacker/hacking-labs), [Pro Hacking Labs](https://www.hackthebox.com/hacker/pro-labs), [Hacking Battlegrounds](https://www.hackthebox.com/hacker/hacking-battlegrounds), [CTFs](https://www.hackthebox.com/hacker/ctf), and also the [HTB Academy](https://academy.hackthebox.com/) which aims to teach everything, from fundamentals concepts and tools, such as **basic networking** and **how to use nmap**, to advanced concepts, like **how to attack an enterprise network** from start to finish and **how to document the whole process** while doing it.

I am now subscribed on both THM and HTB as a student, which comes below £20 per month for both, and my plan is to continue learning via THM until I, at least, achieve my goals, while perfroming my practical work on HTB. 

Having read the aforementioned comparisons, I was expecting to have a really hard time on starting out at HTB and I was ready to hit many roadblocks straight away. But it proved quite the opposite!

When I first logged in on the HTB platform, it suggested to me to go through its [**Starting Point**](https://app.hackthebox.com/starting-point), which as HTB puts it's: "*Hack The Box on rails*". I was so impressed by the **well thought out structure** and the **exceptionally well-written write ups**, that I decided to write a quick post about it, and, hopefully, let other people now about it.

## Tier 0

According to HTB, the goal of Tier 0 machines are to:

> *Cover the absolute **fundamentals of attacking a Box**. You'll learn **how to connect to the VPN**, perform **basic enumeration of ports and services**, and **interact with the services you find**. Each Box in this Tier is focused on a particular tool or service and contains only a single primary step.*

This Tier contains 8 rooms in total and the final task of each machine, is to find a single flag, the `flag.txt` file. Each machine includes a write-up that is similary structured, and, usually, contains three sections:
1. Introduction: General information as well as setting up the room's context.
2. Enumeration: How to use `nmap` for port scanning and to enumerate a specific service.
3. Foothold: How to interact with the service found.

You can find an overview of each room below:

| Room | Concept | Service | Tool(s) |
|:-----------------------------|:-----------------|
| Meow | Pwnbox/VPN, enumeration | telnet | `nmap` | 
| Fawn | ports, SSL/TLS | FTP | `nmap`, `ftp` |
| Dancing | SMB | SMB, NetBIOS | `nmap`, `smbclient` |
| Reedemer | | | |
| Explosion | | | |
| Preignition | | | |
| Mongod | | | |
| Synced | | | |


1. Meow 
    - How to use the Pwnbox/VPN.
    - What **enumeration** is and how to peform a basic `nmap` scan.
    - Information about `telnet` and common default credentials.
2. Fawn
    - Information about the **File Transfer Protocol**, `ftp`, including `anonymous` login.
    - General information about **ports** and the **SSL/TLS** protocol.
    - Introduction to `nmap` switches.
3. Dancing
    - Information about **Server Message Block (SMB)**.
    - SMB interaction with `smbclient`.
4. Reedemer
    - Information about the **Remote Dictionary Server (Redis)**.
    - Redis interaction via `redis-cli`.
5. Explosion
    - Infromation about the **Remote Desktop Protocol (RDP)**.
    - Information about **CLI-remote access tools**, such as **telnet** and **ssh**.
    - Infromation about **GUI-remote desktop tools**, such as **TeamViewer** and `xfreerdp`.
6. Preignition
    - Information about **WordPress**.
    - Information about web servers in general, and **nginx** in particular.
    - What **dir busting** is and how to use `gobuster`.
7. Mongod
    - Information about **MongoDB**.
    - Interacting with **MongoDB** with `mongodb`.
8. Synced
    - Information about the **rsync** protocol.

## Tier 1

Fundamental exploitation techniques, single primary exploitation step per machine, guided tasks, 1 flag

## Tier 2

Chain all steps together: enumeration, initial foothold, privilege escalation, 2 flags `user.txt` and `root.txt`

## Conclusion