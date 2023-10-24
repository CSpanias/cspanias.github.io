---
title: RootMe CTF Write Up
date: 2023-10-20
categories: [CTF Write Up, THM]
tags: [gtfobins, suid, gobuster, nmap, webshell, apache]
img_path: /assets/rootme/
mermaid: true
---

![room_banner](room-banner.png)

## 1 Summary



## 2 Background Information

[The RootMe](https://tryhackme.com/room/rrootme) room is a fairly straightfoward room, great for beginners, as it provides "hints" on what to search for on each task. As a result, not really any specific background information is needed!

Let's dive right in 🏃!

## 3. CTF Process

### 3.1 Reconnaissance

This task asks us about **open ports**, **services**, and **service versions**. We can use `nmap` to find out all that:

    ```shell
    nmap -open -sC -sV -T4 MACHINE_IP
    ```

    ![Nmap Scan results](nmap-scan.png)

With just one command we are able to answer almost all task's 2 questions 🍻 !

The last question asks us to scan the web server using `gobuster` in order to find a hidden directory, so let's do just that:

    ```shell
    gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u MACHINE_IP
    ```

    ![Gobuster scan results](gobuster-scan.png)

And with that, we are ready to move on onto Task 3!

### 3.2 Getting a Shell

If we visit the subdirectory `/panel` that we just found via our browser, we see that it is in fact an upload page:

![Panel subdirectory](panel-dir.png)

1. Since the task asks us to get a shell, we can try using the popular [PentestMonkey's PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php). We can simpy copy and paste it on a file using `nano`, changing only the `IP` and `port` variables:

    ![revshell config](revshell.jpg)

2. When we try to upload our shell, the server makes it clear that `.php` extension files are not allowed:

    ![php-ext](php-ext.png)

    A simple way to bypass this server-side filtering is to change to extension to something else that would still work, such as `.php5`. This concept is explained thoroughly in the THM's [Upload Vulnerabilities](https://tryhackme.com/room/uploadvulns) room.

    When we try to upload `revshell.php5` the server now accepts it:

    ![php5-ext](php5-ext.png)

3. Next, we open a listener and the port we specified on our reverse shell, and upon visiting the URL hosting our revshell.php5, we receive our reverse shell. We can get our first 🚩 by searching for the `user.txt` file:

    ```shell
    find -name user.txt -type f 2>/dev/null
    ```

    ![revshell-user-txt](user-txt.jpg)

### 3.3 Privilege Escalation

The last task asks us to find a "weird" file with SUID permission and the `root.txt` file. Escalating privileges through SUID files is very common on CTFs, so our plan is as follows:
1. Search and find the "weird" SUID file.
2. Visit [GTFOBins](https://gtfobins.github.io/) to check how we can use it to perform privilege escalation.
3. Search and read for `root.txt`.

1. Let's search for SUID files:

    ```shell
    find / -perm -u=s -type f 2>/dev/null
    ```

    ![SUID Files](python-suid.png)

    From the list we get, **Python** definetely seems the most "weird".

2. If we search for [Python with the SUID flag highlighted](https://gtfobins.github.io/gtfobins/python/#suid) at GTFOBins, we get the following:

    ![GTFOBins Python](gtfobins-python-suid.png)

3. Following GTFOBins' instructions and searching for `root.txt`, we can snatch the final 🚩:

    ![Root Flag](root-txt.jpg)