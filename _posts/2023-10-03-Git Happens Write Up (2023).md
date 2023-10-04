---
title: Git Happens CTF Write Up (2023)
date: 2023-10-03 10:00:00 +0100
categories: [CTF Write Up, THM] # up to 2 categories
tags: [nmap, nikto, git, gittools] # TAG names should always be lowercase
img_path: /assets/git_happens/
mermaid: true
---

![room_banner](git_happens_banner.png)

# Summary

*Replace text-summary with graph*

- **Enumeration** with _nmap_
- **Subdirectory Enumeration** with _Nikto_
- **Git Repository Manipulation** with _GitTools_

# Background Information

The [Git Happens room](https://tryhackme.com/room/githappens), as the name suggests, focuses on **Git**. Thus, some basic knowledege about **Git**, as well as some **familiarity with Git's functionality**, would greatly help in solving this challenge. 

Some quick and great resources to read through and practice the main concepts are:
1. [Git Tutorial](https://www.w3schools.com/git/default.asp?remote=github) from w3schools.
2. [Introduction to GitHub](https://github.com/skills/introduction-to-github#introduction-to-github) from GitHub's [official documentation](https://github.com/git-guides#getting-started-with-git).

In brief, **Git** is the most popular **version control system** today, which can be thought as a **timeline management utility**. The core building blocks of a Git project are its **commits**, which are essentially snapshots along the project's timeline. 

As [GitHub's documentation](https://github.com/git-guides/git-commit) perfectly explains: 

>*Over time, commits should tell a story of the history of your repository and how it came to be the way that it currently is*.

Keep this last line in mind, as it's extremely relevant to this room!

# CTF Process

## 1. Port-scanning with nmap

As usual, let's start with an **nmap port-scanning**:
```shell
nmap -sV -T4 -open <taget-ip>
````
`-sV` Attempts to determine the version of the service running on port.  
`-T4` Aggressive (4) speeds scans; assumes you are on a reasonably fast and reliable network.    
`-open` Show only open (or possibly open) ports.   
`<target-ip>` The target machine's IP. 

![nmap_scan](nmap-scan.jpg)

Not much there, just an **nginx web server** on port 80. Vising the site via our browser, we see a login page:

![homepage](homepage.png)

## 2. Subdirectory enumeration with Nikto

We can use various tools for searching subdirectories, such as **gobuster** and **Nikto**, but let's go with Nikto this time:

![nikto_scan](nikto_scan.jpg)

It looks like Nikto found a **public-facing git repository**: `/.git` ! 

![git_dir](git_dir.png)

## 3. Git Repositories and GitTools

We can download the whole repository on our machine using [**GitTools**](https://github.com/internetwache/GitTools). We just need to:
1. Go to the desired directory and clone **GitTools** with `git clone https://github.com/internetwache/GitTools`.
2. Use the `gitdumber.sh` script passing the target repository and the destination directory that we want to clone it in: `gitdumber.sh http://<target-ip>/.git <dest-dir>`.

![gittools](git_clone.jpg)

By moving within the directory, in this case `git`, we can interact as it was our own. For instance, we can see its logs using `git log`:

![git_log](git_log.png)

We are interested mostly on the **commits** included within the log, and in particularly the earlier ones, when the site was on its initial stages. We can achieve this by [chaining commands](https://www.diskinternals.com/linux-reader/bash-chain-commands/#:~:text=Chaining%20usually%20means%20binding%20things,by%20simply%20introducing%20an%20operator.) using the pipe operator `|`, which passes a command's output as the following command's input.

![command_chaining](git_commits_file.jpg)
1. `git log | grep commit` Read logs and show only the lines which include the word "_commit_".
2. `git log | grep commit | cut -d " " -f2` Separate each line using space as the delimiter, and keep only the second field.
3. `git log | grep commit | cut -d " " -f2 | xargs` Converts input from standard input into arguments to a command.
4. `git log | grep commit | cut -d " " -f2 | xargs | cut -d " " -f1 | git show` Separate arguments using space as the delimiter, keep only the first field, and show the corresponding commit.
5. `git log | grep commig | cut -d " " -f2 | xargs git show > commits` Use the arguments generated as an input to `git show`, and write them to the `commits` file. 

Finally, we can use `subl commits` to open the file we just created with the **sublime editor**, and search for the word "_password_" by pressing `CTRL+F`. We can see a discussion regarding the password's security all the way from its creation in plaintext format.

![log_message.png](log_message.png)
![log_message1.png](log_message1.png)
![log_message2.jpg](log_message2.jpg)

The plaintext password is our first and only 🚩 🥂 !
