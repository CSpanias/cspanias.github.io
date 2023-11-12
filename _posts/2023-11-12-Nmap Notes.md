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

When no host discovery options are set, nmap follows the approaches below (in that order):

|User|Network|Method(s)|
|:-:|:-:|---|
|Privileged|LAN|ARP requests|
|Privileged|WAN|ICMP echo, TCP ACK (80), TCP SYN (443), ICMP timestamp|
|Unprivileged|WAN|TCP 3-way handshake via TPC SYN (80, 443)|

To confirm nmap's behaviour with and without the use of a privileged account, we can trying scan a random IP address from the same subnet as ours:

![Using ifconfig command to find our IP address.](ifconfig.jpg)

![Default host discovery scan with and without sudo.](default_vs_sudo_scan.jpg)

When we execute the command without `sudo`, it skips both the ARP and ICMP scans, and goes straight for a full TCP scan. However, when we use `sudo` it performs an ARP scan as expected, since the target host is on the same subnet as us.

> If we gain an initial foothold with a low-privileged user on a target host and we try to enumerate the network from within using `nmap`, it will use a full TCP scan which will generate a lot of traffic and probably a system alert.

### ARP scan

Requirements:
1. We have a privileged account.
2. We are on the same subnet.

Process:
1. Nmap sends an ARP request.
2. It expects an ARP reply back if the host is online.

![Schematic diagram of an ARP request.](arp_scan.png)

### ICMP echo scan

Requirements:
1. We have a privileged account.
2. We are on a different subnet.

> If the target is on the same subnet, an ARP request will precede the ICMP echo request. We can disable ARP requests using `--disable-arp-ping`.

Process:
1. Nmap sends an ICMP echo request.
2. It expects an ICMP echo reply back if the host is online.

![Schematic diagram of an ICMP echo request.](nmap_icmp.png)

> New Windows versions as well as many firewalls block ICMP echo requests by default.

To see what happens in practice, we can scan a live host residing on a different subnet and add the `--packet-trace` and `--reason` flags:

![Packet tracing during an ICMP echo request](icmp_echo_packet-trace.jpg)

![Reason that hosts is up on ICMP echo request](icmp_echo_reason.jpg)

We see that nmap sent an ICMP echo request and it received an ICMP echo reply back, thus, it marked the host as online.

If we try to replicate that for a host that is not up, nmap will send two ICMP echo requests before it gives up and mark the host as offline. The second is just making sure that nothing went wrong with the first one:

![Reason that hosts is up on ICMP echo request](icmp_echo_packet-trace_host_down.jpg)

---------------
An interesting thing to note is the time-to-live variable, `ttl`. Its value can helps us enumerate the target OS: smaller numbers, such as `63`, indicate Linux, while bigger ones, like `127`, indicate Windows.

<!-- Why? What about macOS? -->

![ttl value of 63 for Linux](ttl_linux.jpg)

![ttl value of 127 for Windows](ttl_windows.jpg)

> As ICMP Echo requests tend to be blocked, we can consider sending an ICMP Timestamp (`-PP`) or an ICMP Address Mask (`-PM`) request, and expect for a Timestamp or an Address Mask reply, respectively.

### TCP scans

#### TCP full scan

> Unprivileged users can only scan using the full TCP 3-way handshake method.

Process:
1. Nmap sends a SYN packet.
2. If the host is alive, it will reply with a SYN/ACK packet.
3. Nmap will send an ACK packet.

![TCP 3-way handshake scan.](tcp_full.png)

That's is how the process looks like:

![TCP 3-way handshake scan with packet trace.](tcp_full_scan_low_user.jpg)

![TCP 3-way handshake scan with reason.](tcp_full_scan_low_user_reason.jpg)

#### TCP SYN scan

Requirements:
1. We have a privileged account.
2. We are on a different subnet.

Process:
1. Nmap sents a SYN packet.
2. If host is alive, it will replay with a SYN/ACK packet.
3. Nmap will close the communication by sending a RST packet.

> The process looks the same with a TCP full scan, with the difference that here the communication is closed, and not hanged up.

<!-- what's the real differece? -->

#### TCP ACK

Process:
1. Nmap sends with the ACK flag set.
2. If the host is up, it will reply with a RST packet.

As we can see below, since the `reset` flag was received, nmap marked the host as up:

![TCP ACK scan packet tracing.](tcp_ack_scan.jpg)

![TCP ACK scan reasoning.](tcp_ack_scan_reason.jpg)