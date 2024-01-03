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

## [Level 0 &rarr; 1](https://overthewire.org/wargames/bandit/bandit1.html)

> The password for the next level is stored in a file called `readme` located in the `home` directory. Use this password to log into `bandit1` using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

```shell
$ ssh bandit0@bandit.labs.overthewire.org -p 2220

bandit0@bandit:~$ ls
readme

bandit0@bandit:~$ cat readme
NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```

## [Level 1 &rarr; 2](https://overthewire.org/wargames/bandit/bandit2.html)

> The password for the next level is stored in a file called `-` located in the home directory.

```shell
$ ssh bandit1@bandit.labs.overthewire.org -p 2220

# use absolute path
bandit1@bandit:~$ cat /home/bandit1/-
rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi

# OR, "hide" the dash from the command
bandit1@bandit:~$ cat ./-
rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
```

## [Level 2 &rarr; 3](https://overthewire.org/wargames/bandit/bandit3.html)

> The password for the next level is stored in a file called `spaces in this filename` located in the home directory.

```shell
$ ssh bandit2@bandit.labs.overthewire.org -p 2220

bandit2@bandit:~$ cat "spaces in this filename"
aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG

# or use backslashes
bandit2@bandit:~$ cat spaces\ in\ this\ filename
aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
```

## [Level 3 &rarr; 4](https://overthewire.org/wargames/bandit/bandit4.html)

> The password for the next level is stored in a hidden file in the `inhere` directory.

```shell
$ ssh bandit3@bandit.labs.overthewire.org -p 2220

bandit3@bandit:~$ ls -la inhere/
total 12
drwxr-xr-x 2 root    root    4096 Oct  5 06:19 .
drwxr-xr-x 3 root    root    4096 Oct  5 06:19 ..
-rw-r----- 1 bandit4 bandit3   33 Oct  5 06:19 .hidden

bandit3@bandit:~$ cat inhere/.hidden
2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```

## [Level 4 &rarr; 5](https://overthewire.org/wargames/bandit/bandit5.html)

> The password for the next level is stored in the only human-readable file in the `inhere` directory. Tip: if your terminal is messed up, try the `reset` command.

```shell
$ ssh bandit4@bandit.labs.overthewire.org -p 2220

bandit4@bandit:~$ ls -la inhere/
total 48
drwxr-xr-x 2 root    root    4096 Oct  5 06:19 .
drwxr-xr-x 3 root    root    4096 Oct  5 06:19 ..
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file00
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file01
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file02
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file03
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file04
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file05
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file06
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file07
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file08
-rw-r----- 1 bandit5 bandit4   33 Oct  5 06:19 -file09

# using bash scripting
bandit4@bandit:~$ for file in inhere/*; do cat "$file";echo \n; done

# check content first
bandit4@bandit:~$ file inhere/*
inhere/-file00: data
inhere/-file01: data
inhere/-file02: data
inhere/-file03: data
inhere/-file04: data
inhere/-file05: data
inhere/-file06: data
inhere/-file07: ASCII text
inhere/-file08: data
inhere/-file09: data

bandit4@bandit:~$ cat inhere/-file07
lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```

## [Level 5 &rarr; 6](https://overthewire.org/wargames/bandit/bandit6.html)

> The password for the next level is stored in a file somewhere under the `inhere` directory and has all of the following properties: human-readable, 1033 bytes in size, not executable.

```shell
$ ssh bandit5@bandit.labs.overthewire.org -p 2220

bandit5@bandit:~$ ls inhere/
maybehere00  maybehere03  maybehere06  maybehere09  maybehere12  maybehere15  maybehere18
maybehere01  maybehere04  maybehere07  maybehere10  maybehere13  maybehere16  maybehere19
maybehere02  maybehere05  maybehere08  maybehere11  maybehere14  maybehere17

# using grep based on size
bandit5@bandit:~$ ls -la inhere/maybehere*/ | grep 1033
-rw-r-----  1 root bandit5 1033 Oct  5 06:19 .file2

# using find base on size
bandit5@bandit:~$ find -size 1033c 2>/dev/null
./inhere/maybehere07/.file2

# using find's output as argument for file 
bandit5@bandit:~$ find -size 1033c 2>/dev/null | xargs file
./inhere/maybehere07/.file2: ASCII text, with very long lines (1000)

bandit5@bandit:~$ cat inhere/maybehere07/.file2
P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```

## [Level 6 &rarr; 7](https://overthewire.org/wargames/bandit/bandit7.html)

> The password for the next level is stored somewhere on the server and has all of the following properties: owned by user `bandit7`, owned by group `bandit6`, `33` bytes in size.

```shell
$ ssh bandit6@bandit.labs.overthewire.org -p 2220

bandit6@bandit:/$ find / -type f -size 33c -user bandit7 -group bandit6 2>/dev/null
/var/lib/dpkg/info/bandit7.password

bandit6@bandit:/$ cat /var/lib/dpkg/info/bandit7.password
z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```

## [Level 7 &rarr; 8](https://overthewire.org/wargames/bandit/bandit8.html)

> The password for the next level is stored in the file `data.txt` next to the word `millionth`.

```shell
$ ssh bandit7@bandit.labs.overthewire.org -p 2220

bandit7@bandit:~$ ls
data.txt

bandit7@bandit:~$ cat data.txt | grep millionth
millionth       TESKZC0XvTetK0S9xNwm25STk5iWrBvP

# or in a one-liner
bandit7@bandit:~$ ls | xargs cat | grep millionth
millionth       TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```

## [Level 8 &rarr; 9](https://overthewire.org/wargames/bandit/bandit9.html)

> The password for the next level is stored in the file `data.txt` and is the only line of text that occurs only once.

```shell
$ ssh bandit8@bandit.labs.overthewire.org -p 2220

bandit8@bandit:~$ sort data.txt | uniq -u
EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```

## [Level 9 &rarr; 10](https://overthewire.org/wargames/bandit/bandit10.html)

> The password for the next level is stored in the file `data.txt` in one of the few human-readable strings, preceded by several `=` characters.

```shell
$ ssh bandit9@bandit.labs.overthewire.org -p 2220

bandit9@bandit:~$ strings data.txt | grep ==
x]T========== theG)"
========== passwordk^
========== is
========== G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
```

## [Level 10 &rarr; 11](https://overthewire.org/wargames/bandit/bandit11.html)

> The password for the next level is stored in the file `data.txt`, which contains `base64` encoded data.

```shell
$ ssh bandit10@bandit.labs.overthewire.org -p 2220

bandit10@bandit:~$ base64 -d data.txt
The password is 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
```

## [Level 11 &rarr; 12](https://overthewire.org/wargames/bandit/bandit12.html)

> The password for the next level is stored in the file `data.txt`, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

```console
$ ssh bandit11@bandit.labs.overthewire.org -p 2220

# decode ROT13
bandit11@bandit:~$ cat data.txt | tr '[a-zA-Z]' '[n-za-mN-ZA-M]'
The password is JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
```

## [Level 12 &rarr; 13](https://overthewire.org/wargames/bandit/bandit13.html)

> The password for the next level is stored in the file `data.txt`, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under `/tmp` in which you can work using `mkdir`. For example: `mkdir /tmp/myname123`. Then copy the datafile using `cp`, and rename it using `mv` (read the manpages!).

```shell
$ ssh bandit12@bandit.labs.overthewire.org -p 2220


```