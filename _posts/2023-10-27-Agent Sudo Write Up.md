---
title: Agent Sudo CTF Write Up
date: 2023-10-27
categories: [CTF Write Up, THM]
tags: [nmap, burpsuite, ssh, ftp, john, hydra, brute-force, dictionary-attack, steganography, binwalk, stegseek, john, encoding, base64, exploit-db, gtfobins, sudo, \!root, zip, compression]
img_path: /assets/agent-sudo/
mermaid: true
---

![room_banner](agent-sudo-banner.png)

## 1 Summary



## 2 Background Information

The [Agent Sudo](https://tryhackme.com/room/agentsudoctf) 

## 3. CTF Process

### 3.1 Enumerate

1. The first question of the room is asking us how many open ports are on our target, so let's try answering that using **nmap**:

    ![nmap-results](nmap-results.png)

    Breaking down the command:
    1. `nmap` **Launches Nmap**.
    2. `-sC` Enables Nmap's **default script scanning**. Nmap has a set of built-in scripts that can be used to perform various tasks, such as service discovery, vulnerability detection, and more. Using this option, Nmap will run these default scripts against the target hosts to gather **additional information about the services** and their potential vulnerabilities.
    3. `-sV` Performs **version detection on the target services**.
    4. `-open` Specifies that we want to **scan for open ports**.
    5. `-p-` Scans all ports, not just the most common ones.
    5. `-T4` Sets the **timing template** for the scan. Timing levels in Nmap range from 0 (paranoid) to 5 (insane), with 4 being a relatively aggressive and faster scanning speed.

    ![Nmap Scan results](nmap-scan.png)

    Our scan revealed three services:
    1. FTP
    2. SSH
    3. Web Server

2. The second question is: "*How you redirect yourself to a secret page?*"

    That can be answered by visiting the web server via our browser:

    ![homepage](homepage.png)

3. The last question of this task wants to find out the agent's name and has the following hint:

    >You might face problem on using Firefox. Try 'user agent switcher' plugin with user agent: C

    Instead of using the plugin, we can use **Burp Suite** instead: we need to first capture the HTTP request via **Proxy**, send the request to **Repeater**, modify the **User-Agent** accordingly, and inspect the incoming HTTP response:

    ![Burp Proxy](http-request-proxy.jpg)

    ![user-agent-c](user-agent-c.jpg)

    The HTTP response revealed a new subdirectory, and upon visiting it on our browser, the agent's name is revealed:

    ![agent-c-location](agent-c-location.png)

Onto task 2 🏃!

### 3.2 Hash Cracking and Brute-force

In this section we are expected to find and crack four passwords as well as find another's agent full name.

1. We need to first find the password for the **FTP** service. Since we already have a username, `chris`, and we know already that he has a weak password, we can try guessing it with **hydra**:

    ![hydra][hydra-fpt-password.jpg]

2. Next, we are asked about a **zip** file password, but we don't have any such file yet! Let's login into FTP, and see what we can find:

    ![ftp-mget](ftp-mget.png)

    There are three files there: `To_AgentJ.txt`, `cute-alien.jpg`, and `cutie.png` which we can download locally using `mget *`, as shown above. So, still, no zip file! Let's see what the contant of `To_AgentJ.txt` is:

    ![txt-message](txt-message.png)

    We have two pieces of information:
    1. There is another picture inside our, i.e., `J`, directory.
    2. `J`'s login password is stored in the fake picture.

    Based on the above as well as that next question is related to steganography, we can see these two "fake" photos are hiding something. We can do that with `binwalk`:

    ![binwalk](binwalk.png)

    Apparently, the zip file was embedded in the `cutie.png` file! The *Mr.John* hint provides, points in using `john`, so let's try that. We need to first convert the file to a suitable format for `john` and then just pass it over:

    ![zip2john](zip2john.jpg) 

3. The third questions need a steg password. We have extracted a text file before, so let's inspect its content:

    ![to-agentR](to-agentR-txt.png)

    From reading the sentence, we can infer that `QXJlYTUx` is a name which is currently encoded. The most straightfoward thing to do is to visit [CyberChef](https://gchq.github.io/CyberChef/) and let it works its magic:

    ![cyberchef](cyberchef.jpg)

    There are other ways to find this such as directly trying decoding with `base64`:

    ![base64-decoding](base64-d-area51.jpg)

    Or use `stegseek`:

    ![stegseek-passphrase](stegseek.jpg)

4. Now we need to find





### 3.3 Capture the User Flag

### 3.4 Privilege Escalation

