---
title: Dogcat CTF Write Up (2023)
date: 2023-10-03 10:00:00 +0100
categories: [CTF Walkthroughs] # up to 2 categories
tags: [thm, ctf] # TAG names should always be lowercase
img_path: /assets/dogcat/
---

Now that we managed to get an **initial foothold**, we should look for a way to **escalate our privileges**. We can check if the current user can run any program with SUDO:

![sudo_l](sudo_list.png)

It seems that we can run `env` with SUDO, and [**GTFOBins**](https://gtfobins.github.io/) is an excellent resource for searching what options might exist:

![gtfobins](gtfo_env.png)

Following GTFOBins's instructions, we can get ourselves a **root shell** and get our next 🚩:

![root_shell](root_shell_flag_3.png)

### 5. Container Escape

The room's description mentioned two things: **exploiting a PHP application via LFI**, which we did, and **break out of a docker container**, which we did not. We are missing our last 🚩, thus, we can safely assume that we are inside a container from which we must break out in order to get it. To confirm this, we can check our `hostname`. Under "normal" circumstances it would give us something like `dogcat` or the machine's IP address, but in this case we get a "weird" response:

![hostname_container](hostname.png)

To break out, we will need to find a way to launch a reverse shell from our current meterpreter shell (any [Inception](https://www.imdb.com/title/tt1375666/) fans here?). 

![inception](inception_banner.jpg)

In `/opt/backups` we can find a script called `backup.sh` which runs every minute with root privileges in order to generate the `backup.tar` file:

![opt_backups](backups_dir.png)

We can grab a [**bash reverse shell**](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) from PentestMonkey to replace the `backup.sh` contents, set up a listener on our machine, and wait for the script to run. We should receive our shell in under minute, and by listing the current directory's contents we can get our fourth and final 🚩:

![flag4](rce_flag4.png)
