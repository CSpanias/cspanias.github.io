---
title: Nmap
date: 2023-11-12
categories: [Other, Notes]
tags: [nmap, networking, firewall, icmp, tcp, ttl, enumeration, arp]
img_path: /assets/nmap/
---

## Introduction

**Live host discovery** is crucial as going directly into port scanning can **waste time** and **create unnecessary noise** if trying to scan offline systems.

![Host discovery cheatsheet](host_discovery_cheatsheet.png)
_[Commands](https://www.stationx.net/nmap-cheat-sheet/) related with Live Host Discovery_

## Host discovery

When no host discovery options are set, nmap follows the approaches shown below (in that order):

|User|Network|Method(s)|
|:-:|:-:|---|
|Privileged|LAN|ARP requests|
|Privileged|WAN|ICMP echo, TCP ACK (80), TCP SYN (443), ICMP timestamp|
|Unprivileged|WAN|TCP 3-way handshake via TPC SYN (80, 443)|

To confirm nmap's behaviour with and without the use of a privileged account, we can trying scanning a random IP address from the same subnet as ours:

![Using ifconfig command to find our IP address](ifconfig.jpg) 
_Using `ifconfig` to note down our IP address_

![Default host discovery scan with and without sudo](default_vs_sudo_scan.jpg) 
_Default Live Host Discovery scan with and without the use of a privilieged account_

When we execute the command without `sudo`, it skips both the ARP and ICMP scans, and goes straight for a full TCP scan. However, when we use `sudo` it performs an ARP scan as expected, since the target host is on the same subnet as us.

> If we gain an initial foothold with a low-privileged user on a target host and we try to enumerate the network from within using `nmap`, it will use a full TCP scan which will generate a lot of traffic and probably a system alert.
{: .prompt-danger }

### ARP scan

Requirements:
1. Privileged account.
2. Same subnet.

![Schematic diagram of an ARP request.](arp_scan.png)
_Schematic diagram of an ARP request_

### ICMP echo scan

Requirements:
1. Privileged account.

> If the target is on the same subnet, **an ARP request will precede the ICMP echo request**. We can disable ARP requests using `--disable-arp-ping`.
{: .prompt-info }

![Schematic diagram of an ICMP echo request.](nmap_icmp.png)
_Schematic diagram of an ICMP echo request_

New Windows versions as well as many firewalls block ICMP echo requests by default:

![Windows Defender Inbound rules.](firewall_rules.jpg)
_Windows Defender Inbound rules related to the ICMPIPv4 protocol_

![ICMP echo blocked.](firewall_icmp_blocked.jpg)
_ICMP echo requests not allowed_

![ICMP echo permitted.](firewall_icmp_permitted.jpg)
_ICMP echo requests permitted_

To see what happens in practice, we can scan a live host residing on a different subnet:

![Packet tracing during an ICMP echo request](icmp_echo_packet-trace.jpg)
_Packet tracing during an ICMP echo request_

![Reason that hosts is up on ICMP echo request](icmp_echo_reason.jpg)
_Reasoning of why nmap marked the host as alive after an ICMP echo request_

We see that nmap sent an ICMP echo request and it received an ICMP echo reply back, thus, it marked the host as online. If we try to replicate that for a host that is not up, nmap will send two ICMP echo requests before it gives up and mark the host as offline. The second is just making sure that nothing went wrong with the first one:

![Packet tracing of a dead host after an ICMP echo request](icmp_echo_packet-trace_host_down.jpg)
_Packet tracing of a dead host with an ICMP echo request_

> The TTL (time-to-live) value can helps us in identifying the target OS. The [default initial TTL value](https://www.systranbox.com/why-is-ttl-different-for-linux-and-windows-systems/) for **Linux/Unix** is **64**, and TTL value for **Windows** is **128**.
{: .prompt-tip }

![ttl value of 63 for Linux](ttl_linux.jpg)
_TTL value of 63 pointing towards a Linux OS_

![ttl value of 127 for Windows](ttl_windows.jpg)
_TTL value of 127 pointing towards a Windodws OS_

> As ICMP echo requests tend to be blocked, we can consider sending an **ICMP Timestamp** (`-PP`) or an **ICMP Address Mask** (`-PM`) request, and expect for a Timestamp or an Address Mask reply, respectively.
{: .prompt-tip }

### TCP scans

#### TCP full scan

> Unprivileged users can only scan using the full TCP 3-way handshake method.
{: .prompt-info }

![TCP 3-way handshake scan.](tcp_full.png)
_Schematic diagram of a full TCP 3-way handshake scan_

That's is how the process looks like:

![TCP 3-way handshake scan with packet trace.](tcp_full_scan_low_user.jpg)
_Packet tracing of a full TCP 3-way handshake scan_

![TCP 3-way handshake scan with reason.](tcp_full_scan_low_user_reason.jpg)
_Reasosing of a live host after a full TCP 3-way handshake scan_

#### TCP SYN scan

Requirements:
1. Privileged account.

> Privileged users don't need to complete the TCP 3-way handshake even if the port is open (TCP SYN scan), but unprivileged ones have no choice but wait for its completion (TCP full scan).
{: .prompt-info }

![TCP SYN scan diagram.](tcp_syn_ps.png)
_Schematic diagram of a TCP SYN scan_

![TCP SYN scan packet tracing.](tcp_syn_scan.jpg)
_Packet tracing of a TCP SYN scan_

#### TCP ACK

![TCP ACK scan diagram.](tcp_ack.png)
_Schematic diagram of a TCP ACK scan_

As we can see below, since the `reset` flag was received, nmap marked the host as alive:

![TCP ACK scan packet tracing.](tcp_ack_scan.jpg)
_Packet tracing of a TCP ACK scan_

![TCP ACK scan reasoning.](tcp_ack_scan_reason.jpg)
_Reasosing of a live host after a TCP ACK scan_

## Footnote

1. The majority of the material comes from [TryHackMe's Nmap](https://tryhackme.com/room/furthernmap) and [HackTheBox's Network Enumeration with Nmap](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap) modules.
2. The scan diagrams come exclusively from [TryHackMe's Nmap](https://tryhackme.com/room/furthernmap) module.