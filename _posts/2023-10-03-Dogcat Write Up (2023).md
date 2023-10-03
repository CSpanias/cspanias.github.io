---
title: Dogcat CTF Write Up (2023)
date: 2023-10-03 10:00:00 +0100
categories: [CTF Walkthroughs] # up to 2 categories
tags: [thm, ctf] # TAG names should always be lowercase
img_path: /assets/dogcat/
---
![dogcat banner](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/dogcatbanner.png)

# Summary

- **Enumeration** with _nmap_
- **LFI exploitation** and **Directory Traversal** with _Burp Suite (Proxy, Repeater)_, _Metasploit_
- **Vertical PrivEsc via SUDO** with _GTFOBins_
- **Container Escape** via _Scheduled Scripts_

# Background Information

[Dogcat](https://tryhackme.com/room/dogcat) is considered a **medium difficulty** room, and I couldn't agree more with that. Thus far, I have only worked on **easy difficulty** rooms, and this was sure a level above that. I seriously struggled getting an **intial foothold** and I felt lost while searching for the fourth 🚩! 

Based on the room's description, the goal is to **exploit a PHP application via LFI** and **break out of a docker container**. Although I have completed the THM's LFI module, I encountered the concepts of **Log Poisoning** and **Container Escape** for the first time, and as a result, I spent some time reading and learning about them.

I would suggest to anyone unfamiliar with the aforementioned concepts, to go through the following resources before attempting this room:

1. The Burp Suite [Basics](https://tryhackme.com/room/burpsuitebasics) and [Repeater](https://tryhackme.com/room/burpsuiterepeater) modules from _TryHackMe_.
2. The [Local File Inclusion](https://tryhackme.com/room/fileinc) module from _TryHackMe_.
3. An excellent article/lab about [Apache Log Poisoning](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/?ref=fr33s0ul.tech) from _Hacking Articles_.

# CTF Process

## 1. Port-scanning with nmap

Let's start by **port-scanning** our target with `nmap`:
```bash
nmap <target-ip> -sV -T4 -oA nmap-scan -open
```
`<target-ip>` The target machine's IP.  
`-sV` Attempts to determine the version of the service running on port.  
`-T4` Aggressive (4) speeds scans; assumes you are on a reasonably fast and reliable network.  
`-oA <file-name>` Output in the three major formats at once.  
`-open` Show only open (or possibly open) ports.

The results include an **Apache Web Server** and an **SSH server**:

![nmap_scan](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/nmap-scan.png)

## 2. Directory Traversal with Burp Suite's Repeater

Upon visiting the web server we come across a page where we can select and view various images of cats and dogs:

<img src="https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/homepage.png" 
     width="500" 
     height="300" />

If we notice the address bar on our browser, it becomes like this when selecting:
- A dog: http://10.10.123.178/?view=dog
- A cat: http://10.10.123.178/?view=cat

This is where some background knowledge on LFI will come handy. The last part of the aforementioned URLs, e.g. `?view=dog`, are called **parameters**. These can be manipulated and exploited, given that the web app lacks proper **input validation**.

<img src="https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/url_parts.png" 
  width="500"
  height="200"
  />

We can attempt a **Directory Traversal attack** by manipulating the URL's parameters for finding files located outside the web app's root directory. **Burp Suite's Repeater** is the perfect tool for this kind of attack, as it is mostly based on trial and error.

If we use **Burp Suite's Proxy** to capture an HTTP request while choosing to see a dog, and then send it to **Repeater**, it looks like this:

![intruder_request](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/proxy2intruder.png)

On the first line, we can see the URL's parameter `?view=` assigned the value `dog`. The dog image we get as a response is located somewhere inside the Apache's directory, such as `/var/www/html/photos/dogs/5.jpg`. As the name suggests, the **dot-dot-slash attack**, a more fun name for the Directory Traversal attack, is based on using the `../` to eventually get out of the Apache's root directory and try accessing other files, such as `/etc/passwd`. 

So let's try that, by replacing the `dog` value with `/../../etc/passwd`:

![intruder_error1](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/intruder_error1.png)

We get back the message "_Sorry, only dogs or cats allowed._". So let's keep the word `dog` instead of replacing the whole string:

![intruder_error2](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/intruder_error2_path.png)

Now, we are getting a Warning that includes Apache's homepage directory `/var/www/html/index.html`. Using this info, we know that we need at least 3 `../` to get out of that:
1. With the first `../` will be moving from `/var/www/html/` to `/var/www/`.
2. With the second `../` will be moving from `/var/www/` to `/var/`.
3. With the third `../` will be moving from `/var` to `/`. 

We will probably need more than three `../` as the photo will be one or two subdirectories deeper than `/var/www/html/`, such as `/var/www/html/media/dogs/1.jpg`.

We can also see that the app is adding the `.php` extension to our values:

![php_ext](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/php_ext.png)

We can get around this by using a [**NULL BYTE**](https://www.thehacker.recipes/web/inputs/null-byte-injection) at the end of our string, such as `%00` or `&`, tricking the web application into ignoring whatever comes after it, in this case the `.php` extension. After some trial and error, it seems that we need six `../` to successfully get out of the Apache's root directory:

![dot_dot_slash_attack](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/intruder_passwd.png)

## 3. Log Poisoning with Burp Suite's Repeater and Metasploit

Instead of accessing `/etc/passwd`, we can try accessing **Apache's log file** and try to poison it. The default location of the log file is `/var/log/apache2/access.log`, so let's try that:

![log_file](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/intruder_logfile.png)

We can use the `User-Agent` part of the request, by replacing the agent part, `(X11; Ubuntu; Linux x86_64; rv:109.0)`, with PHP code that will accept commands, such as `<?php system($_GET['c']); ?>`:

![log-poisoning](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/user_agent1.png)

If we now add `&c=` to our URL, we can pass any command of our choosing, such as `ps`, and see the output included in the HTTP response:

![ps](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/log_ps.png)

We can exploit this type of vulnerability with **Metasploit's web devivery script** as follows:

![metasploit_webdelivery](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/metasploit_payload1.png)

`LHOST <IP>` Your machine's IP address.  
`SRVPORT <PORT>` An available port to start an HTTP server to host the payload file.  
`PAYLOAD php/meterpreter/reverse_tcp` Specifying that we need a PHP reverse shell.  
`TARGET 1` Choosing PHP for our target machine ([more info](https://www.imdb.com/title/tt1375666/)).  

As instructed by Metasploit, we must run the generated command  as our command in the URL, and a meterpreter session will open on our shell:

![meterpreter_session](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/meterpreter_shell.png)

We can find our first 🚩 by listing the directory files:

![first_flag](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/first_flag.jpg)

We can also find our second 🚩 by just searching for a file that includes `flag2` in its name:

![second_flag](https://github.com/CSpanias/pentesting.io/blob/main/thm/dogcat/media/flag2.png)

## 4. PrivEsc with SUDO and GTFOBins

Now that we managed to get an **initial foothold**, we should look for a way to **escalate our privileges**. We can check if the current user can run any program with SUDO:

![sudo_l](sudo_list.png)

It seems that we can run `env` with SUDO, and [**GTFOBins**](https://gtfobins.github.io/) is an excellent resource for searching what options might exist:

![gtfobins](gtfo_env.png)

Following GTFOBins's instructions, we can get ourselves a **root shell** and get our next 🚩:

![root_shell](root_shell_flag_3.png)

## 5. Container Escape

The room's description mentioned two things: **exploiting a PHP application via LFI**, which we did, and **break out of a docker container**, which we did not. We are missing our last 🚩, thus, we can safely assume that we are inside a container from which we must break out in order to get it. To confirm this, we can check our `hostname`. Under "normal" circumstances it would give us something like `dogcat` or the machine's IP address, but in this case we get a "weird" response:

![hostname_container](hostname.png)

To break out, we will need to find a way to launch a reverse shell from our current meterpreter shell (any [Inception](https://www.imdb.com/title/tt1375666/) fans here?). 

![inception](inception_banner.jpg)

In `/opt/backups` we can find a script called `backup.sh` which runs every minute with root privileges in order to generate the `backup.tar` file:

![opt_backups](backups_dir.png)

We can grab a [**bash reverse shell**](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) from PentestMonkey to replace the `backup.sh` contents, set up a listener on our machine, and wait for the script to run. We should receive our shell in under minute, and by listing the current directory's contents we can get our fourth and final 🚩:

![flag4](rce_flag4.png)
