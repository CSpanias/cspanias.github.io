---
title: Nmap Notes
date: 2023-11-12
categories: [Notes, Enumeration]
tags: [nmap]
img_path: /assets/nmap/
---

## Introduction

<!-- material and picks taken from THM and HTB -->

## Host discovery

When no host discovery options are set, nmap follows the approaches shown below (in that order):

|User|Network|Method(s)|
|:-:|:-:|---|
|Privileged|LAN|ARP requests|
|Privileged|WAN|ICMP echo, TCP ACK (80), TCP SYN (443), ICMP timestamp|
|Unprivileged|WAN|TCP 3-way handshake via TPC SYN (80, 443)|

To confirm nmap's behaviour with and without the use of a privileged account, we can trying scanning a random IP address from the same subnet as ours:

![Using ifconfig command to find our IP address.](ifconfig.jpg){: width="70%"}

![Default host discovery scan with and without sudo.](default_vs_sudo_scan.jpg){: width="70%"}

When we execute the command without `sudo`, it skips both the ARP and ICMP scans, and goes straight for a full TCP scan. However, when we use `sudo` it performs an ARP scan as expected, since the target host is on the same subnet as us.

> If we gain an initial foothold with a low-privileged user on a target host and we try to enumerate the network from within using `nmap`, it will use a full TCP scan which will generate a lot of traffic and probably a system alert.

### ARP scan

Requirements:
1. Privileged account.
2. Same subnet.

![Schematic diagram of an ARP request.](arp_scan.png){: width="60%"}

### ICMP echo scan

Requirements:
1. Privileged account.

> If the target is on the same subnet, **an ARP request will precede the ICMP echo request**. We can disable ARP requests using `--disable-arp-ping`.

![Schematic diagram of an ICMP echo request.](nmap_icmp.png){: width="60%"}

New Windows versions as well as many firewalls block ICMP echo requests by default:

![Windows Defenders Inbound rules.](firewall_rules.jpg)

![ICMP echo blocked.](firewall_icmp_blocked.jpg)

![ICMP echo permitted.](firewall_icmp_permitted.jpg)

To see what happens in practice, we can scan a live host residing on a different subnet and add the `--packet-trace` and `--reason` flags:

![Packet tracing during an ICMP echo request](icmp_echo_packet-trace.jpg)

![Reason that hosts is up on ICMP echo request](icmp_echo_reason.jpg){: width="70%"}

We see that nmap sent an ICMP echo request and it received an ICMP echo reply back, thus, it marked the host as online. If we try to replicate that for a host that is not up, nmap will send two ICMP echo requests before it gives up and mark the host as offline. The second is just making sure that nothing went wrong with the first one:

![Reason that hosts is up on ICMP echo request](icmp_echo_packet-trace_host_down.jpg)

<!-- Can we highlight this part? -->
An interesting thing to note is that we can identify which OS our target use by looking at its **time-to-live** value, (`ttl`). The [default initial TTL value](https://www.systranbox.com/why-is-ttl-different-for-linux-and-windows-systems/) for **Linux/Unix** is **64**, and TTL value for **Windows** is **128**.

![ttl value of 63 for Linux](ttl_linux.jpg){: width="70%"}

![ttl value of 127 for Windows](ttl_windows.jpg){: width="70%"}

> As ICMP echo requests tend to be blocked, we can consider sending an **ICMP Timestamp** (`-PP`) or an **ICMP Address Mask** (`-PM`) request, and expect for a Timestamp or an Address Mask reply, respectively.

### TCP scans

#### TCP full scan

> Unprivileged users can only scan using the full TCP 3-way handshake method.

![TCP 3-way handshake scan.](tcp_full.png){: width="70%"}

That's is how the process looks like:

![TCP 3-way handshake scan with packet trace.](tcp_full_scan_low_user.jpg){: width="70%"}

![TCP 3-way handshake scan with reason.](tcp_full_scan_low_user_reason.jpg){: width="60%"}

#### TCP SYN scan

Requirements:
1. Privileged account.

> Privileged users don't need to complete the TCP 3-way handshake even if the port is open (TCP SYN scan), but unprivileged ones have no choice but wait for its completion (TCP full scan).

![TCP SYN scan diagram.](tcp_syn_ps.png){: width="70%"}

![TCP SYN scan packet tracing.](tcp_syn_scan.jpg)

#### TCP ACK

![TCP ACK scan diagram.](tcp_ack.png){: width="70%"}

As we can see below, since the `reset` flag was received, nmap marked the host as alive:

![TCP ACK scan packet tracing.](tcp_ack_scan.jpg)

![TCP ACK scan reasoning.](tcp_ack_scan_reason.jpg){: width="60%"}