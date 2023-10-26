---
title: Agent Sudo CTF Write Up
date: 2023-10-27
categories: [CTF Write Up, THM]
tags: [nmap, burpsuite, ssh, ftp, john, hydra, brute-force, dictionary-attack, steganography, binwalk, stegseek, john, encoding, base64, exploit-db, gtfobins, sudo, zip, compression]
img_path: /assets/agent-sudo/
mermaid: true
---

![room_banner](agent-sudo-banner.png)

## 1 Summary

flowchart TD
    A[Enumeration]
    B[ /agent_C_attention]:::red
    C[FTP Credentials]
    D[Steganography \nHash Cracking \nDecoding]
    E[SSH credentials]:::red

  A-- nmap \nBurp Suite --> B
  B-- hydra --oC
  C-- binwalk \njohn \nCyberchef \nstegseek--oD
  D-->E

## 2 Background Information

The [Agent Sudo](https://tryhackme.com/room/agentsudoctf) 

## 3. CTF Process

### 3.1 Enumerate

1. The first question of the room ask us how many open ports our target has, so let's try answering that using **nmap**:

    ![nmap-results](nmap-results.png)

    Breaking down the command:
    1. `nmap` **Launches Nmap**.
    2. `-sC` Enables Nmap's **default script scanning**. Nmap has a set of built-in scripts that can be used to perform various tasks, such as service discovery, vulnerability detection, and more. Using this option, Nmap will run these default scripts against the target hosts to gather **additional information about the services** and their potential vulnerabilities.
    3. `-sV` Performs **version detection on the target services**.
    4. `-open` Specifies that we want to **scan for open ports**.
    5. `-p-` Scans **all ports**, not just the most common ones.
    5. `-T4` Sets the **timing template** for the scan. Timing levels in Nmap range from 0 (paranoid) to 5 (insane), with 4 being a relatively aggressive and faster scanning speed.

    Our scan revealed the following services: an FTP, an SSH and a Web Server.

2. The second question is: "*How you redirect yourself to a secret page?*"

    This can be answered by simply visiting the web server via our browser:

    ![homepage](homepage.png)

3. The last question of this task wants us to find out the agent's name and provides the following hint:

    >You might face problem on using Firefox. Try 'user agent switcher' plugin with user agent: C

    The `User-Agent` is an HTTP header field that is part of the request sent by a client (such as a web browser or a mobile app) to a web server when making an HTTP request. It provides information about the user agent (i.e., the client software or device) that is making the request. The `User-Agent` header typically includes details about the client's operating system, software version, and sometimes other information like the device type.

    Its primary purpose is to help web servers and web applications determine how to respond to the client's request based on the client's capabilities. For example, a web server might use the `User-Agent` header to serve different versions of a website or web application to different types of clients (e.g., mobile devices vs. desktop computers).
    
    The author of the room suggests using a plugin for changing the `User-Agent` header, but we can also use **Burp Suite**. We need to first capture the HTTP request via **Proxy**, send the request to **Repeater**, modify the `User-Agent` header accordingly, send the modified request, and inspect the incoming HTTP response:

    ![Burp Proxy](http-request-proxy.jpg)

    ![user-agent-c](user-agent-c.jpg)

    The HTTP response reveals a new subdirectory, and upon visiting it on our browser, the agent's name is revealed!

    ![agent-c-location](agent-c-location.png)

    Onto task 2 🏃!

### 3.2 Hash Cracking and Brute-force

In this section we are expected to find and crack 4 passwords as well as find another's agent full name.

1. We need to first find the password for the **FTP** service. Since we already have a username, `chris`, we can try guessing it with **hydra**:

    ![hydra](hydra-ftp-password.jpg)

    The command is pretty straightforward:
    1. `-l chris` Lowercase `l` is used as we want to use just a **single static login username**, `chris`.
    2. `-P PASS_LIST` Uppercase `P` as we now want to pass a **list of passwords** against `chris`.
    3. `ftp://TAGET_IP` Definining what **service we want to attack**, in this case, `ftp`.

2. Next, we are asked about a **zip** file password, but we don't have any such file yet! Let's login into FTP, and see what we can find:

    ![ftp-mget](ftp-mget.png)

    There are 3 files there: `To_AgentJ.txt`, `cute-alien.jpg`, and `cutie.png` We can download them locally using `mget *`, as shown above. But, still, no zip file! Let's see what the content of `To_AgentJ.txt` is:

    ![txt-message](txt-message.png)

    We have 2 new pieces of information:
    1. There is another picture inside `J`'s directory.
    2. `J`'s login password is stored in the fake picture.

    Based on the above, and the fact that the next question is related to **steganography**, we probably have to check if these two photos are hiding something. Steganography is Greek for *hidden writing*, and is, in simple terms, the practice of hiding something inside of something else. We can use [**binwalk**](https://www.kali.org/tools/binwalk/), a tool for **searching images for embedded files** and executable code, to see if something is hidden inside the images:

    ![binwalk](binwalk.png)

    Apparently, the zip file is embedded in the `cutie.png` file! The question provides the hint: "*Mr.John*", suggesting to use **John The Ripper**, so let's try that. We need to first convert the file to a suitable format for **john**, and then just pass it over to him:

    ![zip2john](zip2john.jpg) 

3. The third question needs a **steg password**. We have extracted a text file before, so let's inspect its content:

    ![to-agentR](to-agentR-txt.png)

    From reading the sentence, we can infer that `QXJlYTUx` is a name which is currently encoded. The most straightfoward thing to do is to visit [CyberChef](https://gchq.github.io/CyberChef/) and let it do its magic:

    ![cyberchef](cyberchef.jpg)

4. Now we need to find another's agent full name. We haven't yet used the `cute-alien.jpg` picture, so let's check if there is something there, this time using [**stegseek**](https://github.com/RickdeJager/stegseek), a fast steghide cracker that is used to extract hidden data from files:

    ![stegseek-extraction](stegseek-extraction.jpg)

    We have enough information for answering both questions for this task 🍻 ! 

### 3.3 Capture the User Flag

1. We have a new pair of credentials, so let's use them right away:

    ![user-flag](user-flag.jpg)

    That was easy 🚩!

2. Next we are asked the name of the photo's incident. Along with the `user_flag.txt` file, there was also the `Alien_autospy.jpg` file. Let's get a copy that file to our machine using `scp`:

    ![scp](scp.png)

    ![alien-photo](alien-photo.png)

    The hint for this question mentions "Fox news", so we can use google and hack our way to the answer:

    ![google](google-incident-fox.png)

    ![roswell-alien-autopsy](roswell-alien-autopsy-fox.png)

### 3.4 Privilege Escalation

We reached the final task of this room 🎉, but this time there are no hints available 😩!

1. The first thing we always do when searching for a privilege escalation vector is checking if the current user has any SUDO privileges:

    ![sudo](sudo-l.png)

    It appears that we have **not root**, `!root`, access?! That's seems a bit strange, so let's ask Google about it:

    ![cve-root](cve-root.png)

    Apparently, according to [Exploit-DB](https://www.exploit-db.com/exploits/47502), there is a way to exploit this, which also help us to answer the first question. 

2. The above page contains details on how to use this exploit:

    ![sudo-exploit](sudo-exploit.png)

    Executing the above command results in us getting a root shell 🍾!

    ![root-exploit](root-exploit.png)

    Now, we can simply search for the root flag:

    ![root-flag](root-flag.jpg)

    And with that, both last questions can be answered 🚩! 
    
    Thanks Agent R. 🕵️‍♂️!