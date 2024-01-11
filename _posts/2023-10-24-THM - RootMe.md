---
title: THM - RootMe
date: 2023-10-24
categories: [CTF, Fullpwn]
tags: [thm, tryhackme, gtfobins, suid, gobuster, nmap, webshell, apache]
img_path: /assets/thm/fullpwn/rootme/
mermaid: true
image:
    path: room-banner.png
---

## 1 Summary

[![](https://mermaid.ink/img/pako:eNptkU1OwzAQRq9imU0qtZC1F0iU8CeBqBpYNSyceJxadexobANR04uwYc3tOAJOW6BIeGX5ffrmabymlRVAGZXavlRLjp7czgtD4jlbXJjQAHKvrHlijJU6wA5NF3kohUKovMWOkZOWG9B_M-dJModnQAckX4LWpChMcIDH_tWTz_e3j9Eo5hHELp4lCVrr_6F7GzKZnPam4e1QVNsyOA_YT_dCkdp-BsaD83fWrKAjs-sZGQy-BXbJsmu5c8rUJLpEvYlTAohUOrbF1_58b78dlz_eZG6Yd_VweT9VxvXZgAenSseaDCSJjsR5tCtgRzJND0iNAOaHpfKQDXv6RamkYxpX3XAl4l-st0OoX0IDBWXxKjiuClqYTczx4G3emYoyjwHGNLSCe8gUr5E3lEmuHWy-AFrKoPc?type=png)](https://mermaid.live/edit#pako:eNptkU1OwzAQRq9imU0qtZC1F0iU8CeBqBpYNSyceJxadexobANR04uwYc3tOAJOW6BIeGX5ffrmabymlRVAGZXavlRLjp7czgtD4jlbXJjQAHKvrHlijJU6wA5NF3kohUKovMWOkZOWG9B_M-dJModnQAckX4LWpChMcIDH_tWTz_e3j9Eo5hHELp4lCVrr_6F7GzKZnPam4e1QVNsyOA_YT_dCkdp-BsaD83fWrKAjs-sZGQy-BXbJsmu5c8rUJLpEvYlTAohUOrbF1_58b78dlz_eZG6Yd_VweT9VxvXZgAenSseaDCSJjsR5tCtgRzJND0iNAOaHpfKQDXv6RamkYxpX3XAl4l-st0OoX0IDBWXxKjiuClqYTczx4G3emYoyjwHGNLSCe8gUr5E3lEmuHWy-AFrKoPc)

## 2 Background Information

[The RootMe](https://tryhackme.com/room/rrootme) room is fairly straigthfoward, great for beginners, as it provides "hints" on what to search for on each task. As a result, not really any specific background information is needed!

Let's dive right in 🏃!

## 3. CTF Process

### 3.1 Reconnaissance

This task asks us about **open ports**, **services**, and **service versions**. We can use `nmap` to find out all this information:

```shell
nmap -open -sC -sV -T4 MACHINE_IP
```

Breaking down the command:
1. `nmap` **Launches Nmap**.
2. `-open` Specifies that we want to **scan for open ports**.
3. `-sC` Enables Nmap's **default script scanning**. Nmap has a set of built-in scripts that can be used to perform various tasks, such as service discovery, vulnerability detection, and more. Using this option, Nmap will run these default scripts against the target hosts to gather **additional information about the services** and their potential vulnerabilities.
4. `-sV` Performs **version detection on the target services**.
5. `-T4` Sets the **timing template** for the scan. Timing levels in Nmap range from 0 (paranoid) to 5 (insane), with 4 being a relatively aggressive and faster scanning speed.

![Nmap Scan results](nmap-scan.png)

With just one command we are able to answer almost all task's 2 questions 🍻 !

The last question tells us to scan the web server with `gobuster`, so let's do just that:

```shell
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u MACHINE_IP
```

This is fairly straightforward scan:
1. `gobuster` **Executes Gobuster**.
2. `dir` Specifies that we want to perform **directory brute-forcing**.
3. `-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt` **Specifies the wordlist** file that Gobuster should use for its brute-force attack. The `directory-list-2.3-medium.txt` file is a commonly used wordlist for web directory and file enumeration.
4. `-u MACHINE_IP` Defines the target URL or IP address on which we want to perform the directory/file brute-forcing.

![Gobuster scan results](gobuster-scan.png)

The scan results reveals the `/panel` directory, and with that, we are ready to move on onto Task 3!

### 3.2 Getting a Shell

If we visit the subdirectory `/panel` via our browser, we see that it is an upload page:

![Panel subdirectory](panel-dir.png)

1. Since the task asks us to get a shell, we can try using the popular [PentestMonkey's PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php). We can simpy copy and paste it on a file using `nano`, changing only the `IP` and `port` variables:

    ![revshell config](revshell.jpg)

2. When we try to upload our shell, the server makes it clear that `.php` extension files are not allowed:

    ![php-ext](php-ext.png){: width="60%"}

    A simple way to bypass this **server-side filtering** is to change to extension to something else that would still work, such as `.php5`. This concept is explained thoroughly in the THM's [Upload Vulnerabilities](https://tryhackme.com/room/uploadvulns) room.

    When we try to upload `revshell.php5` the server now accepts it:

    ![php5-ext](php5-ext.png){: width="60%"}

3. Next, we open a listener at the port we specified before, and upon visiting the URL hosting our script, `http://MACHINE-IP/revshell.php5`, we should receive our reverse shell. We can get our first 🚩 by searching for the `user.txt` file:

    ```shell
    find -name user.txt -type f 2>/dev/null
    ```

    The above command does the following:
    1.  `find` This utility is used for **searching files and directories** in a specified directory structure.
    2. `/` This is the starting point for the search. In our case, it represents the root directory of the file system, `/`, meaning that find will search the entire file system.
    3. `-name user.txt` Specifies the **name of the file** we want to search for.
    4. `-type f` Restricts the search to **regular files only**, as opposed to directories, symbolic links, or other types of files.
    5. `2>/dev/null` This is a **redirection operation** that suppresses standard error (*stderr*) output by directing it to the null device (`/dev/null`). This ensures that any error messages or warnings generated during the search are discarded and not displayed in the terminal.

    ![revshell-user-txt](user-txt.jpg)

### 3.3 Privilege Escalation

The last task asks us to find a "weird" file with the SUID permission set as well as the `root.txt` file. Escalating privileges through SUID files is very common on CTFs, so our plan is as follows:
    1. Search and find the "weird" SUID file.
    2. Visit [GTFOBins](https://gtfobins.github.io/) to check how we can use it to perform privilege escalation.
    3. Search for `root.txt`.

1. Let's search for SUID files:

    ```shell
    find / -perm -u=s -type f 2>/dev/null
    ```

    This is almost identical as the previous `find` command, but we are now searching for SUID files instead of a specific file as before. As a result, we replaced `-iname user.txt` with `-perm -u=s`. The latter specifies the **permission pattern** to search for. In this case, it's looking for files with the setuid permission, where `-u=s` indicates files where the setuid bit is set. The `u` stands for the user's permissions (owner), and `s` indicates that the setuid bit is set.

    ![SUID Files](python-suid.png)

    From the resulting list, there is only one obvious culprit: `/usr/bin/python`.

2. If we search for ["python" with the SUID flag highlighted](https://gtfobins.github.io/gtfobins/python/#suid) at GTFOBins, we get the following:

    ![GTFOBins Python](gtfobins-python-suid.png)

3. Following GTFOBins' instructions and searching for `root.txt`, we can snatch the final 🚩:

    ![Root Flag](root-txt.jpg)