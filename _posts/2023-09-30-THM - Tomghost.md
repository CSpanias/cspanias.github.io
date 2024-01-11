---
title: THM - Tomghost
date: 2023-09-30
categories: [CTF, Fullpwn]
tags: [thm, tryhackme, nmap, exploitdb, metasploit, hash, gpg, john, encryption, gtfobins, sudo, ajp]
img_path: /assets/thm/fullpwn/tomghost/
mermaid: true
image:
    path: tomghost_banner.png
---

## 1 Summary

<!-- Replace text-summary with graph* -->

- **Enumeration** with _nmap_, _Exploit-DB_
- **AJP Exploitation** with _Metasploit_
- **Horizotal PrivEsc via Decryption & Hash Cracking** with _GPG_, _john_
- **Vertical PrivEsc via SUDO** with _GTFOBins_

## 2 Background Information

[Tomghost's CTF room](https://tryhackme.com/room/tomghost)'s goal is to "_identify recent vulnerabilities to try exploit the system or read files that you should not have access to_". Let's first start with gaining an understanding what we are actually trying to do on this room.

As a beginner, I was using the terms **Apache** and **Apache Tomcat** interchangeably, but they are not really the same thing. According to this short [GeeksForGeeks article](https://www.geeksforgeeks.org/difference-between-apache-tomcat-server-and-apache-web-server/):

>_**Apache web server**_ is designed to create the web-servers and it can host one or more HTTP based web-servers, while _**Apache Tomcat**_ is a web container that allows the users to run Servlet and JAVA Server Pages that are based on the web-applications and it can also be used as the HTTP server. 

This room is focused on a vulnerability found in the _**Apache Tomcat**_ container, called **_Ghostcast_**.

![ghostscat banner](ghostcat_banner.png)

The **Ghostcat vulnerability** does essentially what the room's description says: if the _**Apache Jserv Protocol (AJP)**_ is exposed over the internet (usually on port 8009), it allows an attacker to **read sensitive files from the Tomcat directories**.

Based on the above information, we kind of know what we should expect:
1. Find the _**AJP protocol**_ exposed on port 8009.
2. Find an **existing exploit** to leverage, gain non-privileged access and snath our first 🚩.
3. Find a way to **escalate our privileges** to root and snatch our second 🚩.

## 3 CTF Process

### 3.1 Nmap port-scanning

Let's start enumerating our target with a **port-scanning** using `nmap`:
```bash
nmap <target-ip> -sV -T4 -oA nmap-scan -open
```
`<target-ip>` The target machine's IP.  
`-sV` Attempts to determine the version of the service running on port.  
`-T4` Aggressive (4) speeds scans; assumes you are on a reasonably fast and reliable network.  
`-oA <file-name>` Output in the three major formats at once.  
`-open` Show only open (or possibly open) ports.  

![Port-scanning results](nmap-scan.png)

As expected, the results include **port 8009** using the **_AJP protocol_** !

### 3.2 Exploit-DB & Metasploit

Searching [**_Exploit-db_**](https://www.exploit-db.com/) for an existing vulnerability related to "_apache tomcat ajp_", we find [**CVE-2020–1938**](https://www.exploit-db.com/exploits/49039), which conveniently let us know that it's included in **Metasploit**:
![CVE-2020–19383](exploit-db.png)

Launching **Metasploit** (using the  `msfconsole` command) and searching for **CVE-2020–1938**, confirms that there is an existing module which we can directly use as follows:

![The CVE-2020–1938 exploit on Metasploit](msf_exploit1.png)

As we can see using by using the `options` command, everything but `RHOSTS` is already good to go. We can pass our target's IP to `RHOSTS` by typing `set RHOSTS <target-ip>`. We can then use the `check` command to find out if our target is vulnerable, and then just `run` the exploit:

![Running the exploit](msf_exploit2_hidden.jpg)

By exploiting the Ghostcast vulnerability we were expecting to find and read sensitive files in the Tomcat directories. The exploit managed to successfully do that, providing us with a pair of credentials to use 👏.

### 3.3 Initial Foothold via SSH 

The nmap results (step 1) included an **SSH server**, which we can now utilise by try connecting using the obtained credentials:

![Connecting to the SSH server](ssh.png)

Success 🎉! We have now gained an **initial foothold** with a low-privileged user, as planned, and we should be able to find and (maybe) read our first 🚩. 
We know that we are searching for a file called `user.txt`, so let's just search for that:

![Capturing our first flag!](first_flag.jpg)

`/` Start searching from the root directory.  
`-iname user.txt` Search, ignoring casing, for a file called user.txt.  
`-type f` Search only for files.  
`2>/dev/null` Suppress any errors.  

### 3.4 GPG Encryption & Horizontal PrivEsc

The only thing left is to find the `root.txt` file which, as the name suggests, would require **escalating our privileges** to a root account.

When listing the files in our current user's home directory, two files appear: `credential.pgp` and `tryhackme.asc`:

![Files found in the current user's home directory](ssh_files.png)

These files are related to [**GPG**](https://www.redhat.com/sysadmin/encryption-decryption-gpg), a popular Linux security tool for encrypting files. The things we need to know for this task are the following:
1. `credential.pgp` is a binary GPG-encryted file which, based on its name, contains the root credentials we are searching for.  
2. `tryhackme.asc` contains a hashed password which might be needed for decrypting the above file.

We can transfer these files to our local machine using the `scp` command and try to directly decrypt the file:

![Transferring the files locally and attemp to decrypt the GPG file](scp%2Bdecrypt.png)

As we can see, the GPG file is encrypted with a **secret key**. If we are try to import `tryhackme.asc` as a key to GPG, a window pops up asking for a **passphrase**:

![GPG failed key import](gpg_failed_import.png)

We will use **John The Ripper** to crack the hash, and then provide it as passphrase to the pop up window. To do that, we first need to convert the hash file into a suitable format for john using `gpg2john`, and then pass that file to john:

![Cracking hashes with John](john_hash_hidden.jpg)

Now, we can use this passphrase when importing `tryhackme.asc` as a key to **GPG**, as well as when we are asked for it again, while decrypting `credentials.gpg`:

![ImportING a key and decrypting a GPG-encrypted file](gpg_decryption_hidden.jpg)

### 3.5 Sudo & Vertical PrivEsc
We have now obtained the credentials of another low-privileged user, what is called **horizontal privilege escalation**. We can try switching to that user and find out if there is anything that we can leverage that will allows us to gain a privileged account, that is, perform **vertical privilege escalation**.

By checking if there is any program that the user `merlin` could run as sudo, by typing `sudo -l`, we find out that the `zip` program is on that list:

![Checking for programs that our current user can use with sudo](suid_zip.png)

Visiting [**GTFOBins**](https://gtfobins.github.io/) and searching for `zip` we can find some interesting information:

![GTFOBins page for zip](gtfobins_zip.png)

By just following the instructions, we can get ourselves a **root shell** and **capture our final** 🚩🥂:

![Capturing our final flag 🥂!](final_flag.jpg)
