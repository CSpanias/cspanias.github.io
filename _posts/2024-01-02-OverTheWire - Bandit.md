---
title: OverTheWire - Bandit
date: 2024-01-02
categories: [OverTheWire, Bandit]
tags: [overthewire, bandit, linux]
img_path: /assets/overthewire/bandit
published: true
---

The [Bandit](https://overthewire.org/wargames/bandit/) wargame is **aimed at absolute beginners**. It will teach the basics needed to be able to play other wargames. If you notice something essential is missing or have ideas for new levels, please let us know!

**Note for beginners**: First, if you know a command, but don’t know how to use it, try the **manual (man page)** by entering `man <command>`. For example, `man ls` to learn about the “ls” command. The “man” command also has a manual, try it! When using man, press `q` to quit (you can also use / and n and N to search). Second, if there is no man page, the command might be a shell built-in. In that case use the `help <X>` command, for example, `help cd`.

**Note for VMs**: You may fail to connect to overthewire.org via SSH with a “broken pipe error” when the network adapter for the VM is configured to use NAT mode. Adding the setting IPQoS throughput to `/etc/ssh/ssh_config` should resolve the issue. If this does not solve your issue, the only option then is to change the adapter to Bridged mode.

## [Level 0](https://overthewire.org/wargames/bandit/bandit0.html)

> The goal of this level is for you to log into the game using SSH. The host to which you need to connect is `bandit.labs.overthewire.org`, on port `2220`. The username is `bandit0` and the password is `bandit0`:

```shell
$ ssh bandit0@bandit.labs.overthewire.org -p 2220
bandit0@bandit:~$
```

## [Level 0 {% octicon arrow-right height:24 %} 1](https://overthewire.org/wargames/bandit/bandit0.html)
## [Level 0 --> 1](https://overthewire.org/wargames/bandit/bandit0.html)
## [Level 0 &rarr; -->]((https://overthewire.org/wargames/bandit/bandit0.html))

```shell
$ ssh bandit0@bandit.labs.overthewire.org -p 2220
bandit0@bandit:~$ cat readme
NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```

1. Level 0 --> 1
```shell
ssh bandit1@bandit.labs.overthewire.org -p 2220
# bandit1:NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```
The password for the next level is stored in a file called **readme** located in the home directory. Use this password to log into bandit1 using SSH:
```shell
cat readme
# NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```
2. Level 1 --> 2
```shell
ssh bandit1@bandit.labs.overthewire.org -p 2220
# bandit1:NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```
The password for the next level is stored in a file called **-** located in the home directory:
```shell
find / -iname - -type f 2>/dev/null
# /home/bandit1/-
cat /home/bandit1/-
# rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
# OR, "hide" the dash from the command
cat ./-
```

3. Level 2 --> 3
```shell
ssh bandit2@bandit.labs.overthewire.org -p 2220
# bandit2:rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
```
The password for the next level is stored in a file called **spaces in this filename** located in the home directory:
```shell
cat "/home/bandit2/spaces in this filename"
# aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
# OR
cat spaces\ in\ this\ filename
```

4. 3 --> 4
```shell
ssh bandit3@bandit.labs.overthewire.org -p 2220
# aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
```
The password for the next level is stored in a hidden file in the **inhere** directory:
```shell
ls -la
# inhere
cd .inhere
ls -la
# .hidden
cat .hidden
# 2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```

5. 4-->5
```shell
ssh bandit4@bandit.labs.overthewire.org -p 2220
# 2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```
The password for the next level is stored in the only human-readable file in the **inhere** directory. Tip: if your terminal is messed up, try the “reset” command:
```shell
cd inhere
file ./-file**
# ./-file00: data
# ./-file01: data
# ./-file07: ASCII text
cat ./-file07
# lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```

6. 5-->6
```shell
ssh bandit5@bandit.labs.overthewire.org -p 2220
# lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```
The password for the next level is stored in a file somewhere under the **inhere** directory and has all of the following properties:
- human-readable
- 1033 bytes in size
- not executable
```shell
ls -la maybehere* | grep 1033
# -rw-r-----  1 root bandit5 1033 Oct  5 06:19 .file2
find . -type f -size 1033c 2>/dev/null
# ./maybehere07/.file2
find . -type f -size 1033c 2>/dev/null | xargs file
# ./maybehere07/.file2: ASCII text, with very long lines (1000)
cat ./maybehere07/.file2
# P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```

7. 6-->7
```shell
ssh bandit6@bandit.labs.overthewire.org -p 2220
# P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```
The password for the next level is stored **somewhere on the server** and has all of the following properties:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size
```shell
find / -type f -size 33c 2>/dev/null | grep bandit7 | xargs ls -la
# -r-------- 1 bandit7 bandit7 33 Oct  5 06:19 /etc/bandit_pass/bandit7
# -rw-r----- 1 bandit7 bandit6 33 Oct  5 06:19 /var/lib/dpkg/info/bandit7.password
cat /var/lib/dpkg/info/bandit7.password
# z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```

8. 7-->8
```shell
ssh bandit7@bandit.labs.overthewire.org -p 2220
# z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```
The password for the next level is stored in the file **data.txt** next to the word **millionth**.
```shell
find / -type f -iname data.txt 2>/dev/null | grep bandit7 | xargs cat | grep "millionth"
# millionth TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```

9. 8-->9
```shell
ssh bandit8@bandit.labs.overthewire.org -p 2220
# TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```
The password for the next level is stored in the file **data.txt** and is the only line of text that occurs only once.
```shell
find / -type f -iname data.txt 2>/dev/null | grep bandit8
# /home/bandit8/data.txt
cat /home/bandit8/data.txt | sort | uniq -u
# EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```

10. 9-->10
```shell
ssh bandit9@bandit.labs.overthewire.org -p 2220
# EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```
The password for the next level is stored in the file **data.txt** in one of the few human-readable strings, preceded by several ‘=’ characters.
```shell
cd /home/bandit9
ls
# data.txt
xxd data.txt | grep "====*"
# 00000460: 785d 543d 3d3d 3d3d 3d3d 3d3d 3d20 7468  x]T========== th
# 000014a0: a1a7 4f5b 970e b936 fe5e 4653 bf3d 3d3d  ..O[...6.^FS.===
# 000014b0: 3d3d 3d3d 3d3d 3d20 7061 7373 776f 7264  ======= password
# 00001b40: c8ff 3d3d 3d3d 3d3d 3d3d 3d3d 2069 73ba  ..========== is.
# 00003f40: 3d3d 3d3d 3d3d 3d3d 2047 3777 384c 4969  ======== G7w8LIi
# ======== G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
```

11. 10-->11
```shell
ssh bandit10@bandit.labs.overthewire.org -p 2220
# G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
```
The password for the next level is stored in the file **data.txt**, which contains base64 encoded data.
```shell
base64 -d data.txt
# The password is 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
```

12. 11-->12
```shell
ssh bandit11@bandit.labs.overthewire.org -p 2220
# 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
```
The password for the next level is stored in the file **data.txt**, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

Reading: [Rot13 on Wikipedia](https://en.wikipedia.org/wiki/Rot13)