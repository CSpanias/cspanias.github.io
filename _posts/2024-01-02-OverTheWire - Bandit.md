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

```bash
$ ssh bandit11@bandit.labs.overthewire.org -p 2220

# decode ROT13
bandit11@bandit:~$ cat data.txt | tr '[a-zA-Z]' '[n-za-mN-ZA-M]'
The password is JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
```

## [Level 12 &rarr; 13](https://overthewire.org/wargames/bandit/bandit13.html)

> The password for the next level is stored in the file `data.txt`, which is a **hexdump** of a file that has been **repeatedly compressed**. For this level it may be useful to create a directory under `/tmp` in which you can work using `mkdir`. For example: `mkdir /tmp/myname123`. Then copy the datafile using `cp`, and rename it using `mv` (read the manpages!).

```bash
$ ssh bandit12@bandit.labs.overthewire.org -p 2220

# create a new directory within the tmp directory
bandit12@bandit:~$ mkdir /tmp/xhi4m
# copy the file into the newly-created directory
bandit12@bandit:~$ cp data.txt /tmp/xhi4m
# move within the newly-created directory
bandit12@bandit:~$ cd /tmp/xhi4m
# check the type of the file (based on its magic number)
bandit12@bandit:/tmp/xhi4m$ file data.txt
data.txt: ASCII text
```

We know that the file is a [**hexdump**](https://intentionalprivacy.files.wordpress.com/2019/02/hexdumpprimer.pdf). These can be used to figure out the file type based on the **file signature**, aka [**magic number**](https://en.wikipedia.org/wiki/List_of_file_signatures). This file's magic number is `We can start by renaming the file, checking its magic number and then reverting the hexdump:

```bash
# renaming the file
bandit12@bandit:/tmp/xhi4m$ mv hexdump hexdump_data
# checking the file's magic number (first 4 characters)
bandit12@bandit:/tmp/xhi4m$ head -1 data.txt
00000000: 1f8b 0808 6855 1e65 0203 6461 7461 322e  ....hU.e..data2.
# reverting the hexdump
bandit12@bandit:/tmp/xhi4m$ xxd -r hexdump_data compressed_data
# displaying the first line of the file
bandit12@bandit:/tmp/xhi4m$ head -1 compressed_data
�h44�z��A����@=�h4hh�⸮⸮⸮��hd����������������9���1����������;,�
�����2�3d*58�~  �S�ZP^��luY��Br$�FP!%�s��h�?�)[=�h��O(B��2A���)�tZc��:�pã)�A�ˈ�0���΅A�yjeϢx,�(����z�E�+"�2�/�-��e"���^����t�j���$�d�@�dJơ'7\���$��m1c��#>�aԽ�EV��F��OCӐc@M�C���]��Y2^h8���D=��~      O�I��NDpF�+�|b#Jv�#�J��d�LފW$�Û�͖y�`
                              �\&       ��[�@*w�M�0θ��nr��C��`e$b�
                                                                  ~�{���
                                                                        ��`�<����a��?e:T���e�T4±b����)
```

Based on the file's magic number (`1f8b`) and the [wiki list](https://en.wikipedia.org/wiki/List_of_file_signatures) we know that it's a `gzip` file. Therefore, we can add the proper extension (`.gz`) and decompress it:

> Renaming the file with the proper extension is necessary only for `gzip`.

```bash
# check the type of the file (based on its magic number)
bandit12@bandit:/tmp/xhi4m$ file compressed_data
compressed_data: gzip compressed data, was "data2.bin", last modified: Thu Oct  5 06:19:20 2023, max compression, from Unix, original size modulo 2^32 573
# add the proper extension
bandit12@bandit:/tmp/xhi4m$ mv compressed_data compressed_data.gz
# decompress the file
bandit12@bandit:/tmp/xhi4m$ gzip -d compressed_data.gz
# list the directory contents
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data  hexdump_data
```

This generated a file named `compressed_data` so we can repeat the process as many times as necessary until we get the password:
1. Identify the type of the file.
2. Act accordingly.

```bash
# check the type of the file (based on its magic number)
bandit12@bandit:/tmp/xhi4m$ file compressed_data
compressed_data: bzip2 compressed data, block size = 900k
# add the proper extension
bandit12@bandit:/tmp/xhi4m$ mv compressed_data compressed_data.bz2
# decompress the file
bandit12@bandit:/tmp/xhi4m$ bzip2 -d compressed_data.bz2
# list the directory contents
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data  hexdump_data

# repeat the process for decompressing the gzipped file
bandit12@bandit:/tmp/xhi4m$ file compressed_data
compressed_data: gzip compressed data, was "data4.bin", last modified: Thu Oct  5 06:19:20 2023, max compression, from Unix, original size modulo 2^32 20480
bandit12@bandit:/tmp/xhi4m$ mv compressed_data compressed_data.gz
bandit12@bandit:/tmp/xhi4m$ gzip -d compressed_data.gz
# list the directory contents
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data  hexdump_data

# repeat the process for extracting the tar archive file
bandit12@bandit:/tmp/xhi4m$ file compressed_data
compressed_data: POSIX tar archive (GNU)
bandit12@bandit:/tmp/xhi4m$ mv compressed_data compressed_data.tar
bandit12@bandit:/tmp/xhi4m$ tar -xf compressed_data.tar
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data.tar  data5.bin  hexdump_data

# repeat the process for extracting the tar archive file
bandit12@bandit:/tmp/xhi4m$ file data5.bin
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/xhi4m$ tar -xf data5.bin
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data.tar  data5.bin  data6.bin  hexdump_data

# repeat the process for decompressing the bzipped2 file
bandit12@bandit:/tmp/xhi4m$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/xhi4m$ bzip2 -d data6.bin
# bzip2: Can't guess original name for data6.bin -- using data6.bin.out
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data.tar  data5.bin  data6.bin.out  hexdump_data

# repeat the process for extracting the tar archive file
bandit12@bandit:/tmp/xhi4m$ file data6.bin.out
data6.bin.out: POSIX tar archive (GNU)
bandit12@bandit:/tmp/xhi4m$ tar -xf data6.bin.out
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data.tar  data5.bin  data6.bin.out  data8.bin  hexdump_data

# repeat the process for decompressing the gzipped file
bandit12@bandit:/tmp/xhi4m$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Thu Oct  5 06:19:20 2023, max compression, from Unix, original size modulo 2^32 49
bandit12@bandit:/tmp/xhi4m$ mv data8.gz data8.bin.gz
bandit12@bandit:/tmp/xhi4m$ gzip -d data8.bin.gz
bandit12@bandit:/tmp/xhi4m$ ls
compressed_data.tar  data5.bin  data6.bin.out  data8.bin  hexdump_data

bandit12@bandit:/tmp/xhi4m$ file data8.bin
data8.bin: ASCII text
bandit12@bandit:/tmp/xhi4m$ cat data8.bin
The password is wbWdlBxEir4CaE8LaPhauuOo6pwRmrDw
```

## [Level 13 &rarr; 14](https://overthewire.org/wargames/bandit/bandit14.html)

> The password for the next level is stored in `/etc/bandit_pass/bandit14` and can only be read by user `bandit14`. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. 

> Note: `localhost` is a hostname that refers to the machine you are working on.

```bash
$ ssh bandit13@bandit.labs.overthewire.org -p 2220

bandit13@bandit:~$ ls
sshkey.private
bandit13@bandit:~$ cat sshkey.private
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtCnEucB9DvN2HZkupc/h6hTKUYLqXuyLD8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----
```

We have to create a file, copy paste the key on our local machine, and then use it to connect to the next level:

```bash
# create a file called 'id_rsa'
$ sudo nano id_rsa
# display the file contents
$ cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtCnEucB9DvN2HZkupc/h6hTKUYLqXuyLD8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----

# use the key to connect to the next level
$ ssh bandit14@bandit.labs.overthewire.org -p 2220 -i id_rsa
bandit14@bandit:~$
```

## [Level 14 &rarr; 15](https://overthewire.org/wargames/bandit/bandit15.html)

> The password for the next level can be retrieved by submitting the password of the current level to port `30000` on localhost.

```bash
$ ssh bandit14@bandit.labs.overthewire.org -p 2220 -i id_rsa

# read the password (location mentioned on the previous level)
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
# submit the data on the required socket
bandit14@bandit:~$ nc localhost 30000
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
Correct!
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
```

## [Level 15 &rarr; 16](https://overthewire.org/wargames/bandit/bandit16.html)

> The password for the next level can be retrieved by submitting the password of the current level to port `30001` on `localhost` using SSL encryption.

> Helpful note: Getting `HEARTBEATING` and `Read R BLOCK`? Use `-ign_eof` and read the `CONNECTED COMMANDS` section in the manpage. Next to `R` and `Q`, the `B` command also works in this version of that command…

```bash
$ ssh bandit15@bandit.labs.overthewire.org -p 2220

bandit15@bandit:~$ openssl s_client -connect localhost:30001

<SNIP>

read R BLOCK
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
Correct!
JQttfApK4SeyHwDlI9SXGR50qclOAil1
```

## [Level 16 &rarr; 17](https://overthewire.org/wargames/bandit/bandit17.html)

> The credentials for the next level can be retrieved by submitting the password of the current level to a port on `localhost` in the range `31000` to `32000`. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

We can use `netstat` to check which ports are currenly listening:

```bash
$ ssh bandit16@bandit.labs.overthewire.org -p 2220

# check what ports are listening
bandit16@bandit:~$ netstat -nlt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
netstat: no support for `AF INET (tcp)' on this system.
tcp6       0      0 :::31518                :::*                    LISTEN
tcp6       0      0 :::2220                 :::*                    LISTEN
tcp6       0      0 :::2232                 :::*                    LISTEN
tcp6       0      0 :::2230                 :::*                    LISTEN
tcp6       0      0 :::2231                 :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
tcp6       0      0 :::31790                :::*                    LISTEN
tcp6       0      0 :::30001                :::*                    LISTEN
tcp6       0      0 :::30002                :::*                    LISTEN
```

We found just two ports within the required range: `31518` and `31790`. We can use `nmap` with the version scan option (`-sV`) to check which one uses SSL, and then submit the flag to it:

```bash
# use nmap to scan the ports found above to check which one uses SSL
bandit16@bandit:~$ nmap localhost -sV -p 31518,31790 -T4

PORT      STATE SERVICE     VERSION
31518/tcp open  ssl/echo
31790/tcp open  ssl/unknown
```

We can see that both use SSL but the port `31518` will just echo back whatever will pass to it. So we will use port `31790`:

```bash
# connecting on port 31790
bandit16@bandit:~$ openssl s_client -connect localhost:31790

<SNIP>

read R BLOCK
JQttfApK4SeyHwDlI9SXGR50qclOAil1
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

closed
```

## [Level 17 &rarr; 18](https://overthewire.org/wargames/bandit/bandit18.html)

> There are 2 files in the `home` directory: `passwords.old` and `passwords.new`. The password for the next level is in `passwords.new` and is the only line that has been changed between `passwords.old` and `passwords.new`.

> NOTE: if you have solved this level and see `Byebye!` when trying to log into `bandit18`, this is related to the next level, `bandit19`.

```bash
# connect to SSH using the key found in the previous level
$ ssh bandit17@bandit.labs.overthewire.org -p 2220 -i id_rsa

# display the differences of the two files
bandit17@bandit:~$ diff passwords.old passwords.new
42c42
< p6ggwdNHncnmCNxuAt0KtKVq185ZU7AW
---
> hga5tuuCLF6fFzUpnagiMN8ssu9LFrdg
```

## [Level 18 &rarr; 19](https://overthewire.org/wargames/bandit/bandit19.html)

> The password for the next level is stored in a file `readme` in the `home` directory. Unfortunately, someone has modified `.bashrc` to log you out when you log in with SSH.

We can pass command to an SSH server without logging in to it:

```bash
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme

bandit18@bandit.labs.overthewire.org's password:
awhqfNnAbc1naukrpqDYcF95h7HoMTrC
```

We can also spawn a terminal and read the file that way:

```bash
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 /bin/bash

bandit18@bandit.labs.overthewire.org's password:
cat readme
awhqfNnAbc1naukrpqDYcF95h7HoMTrC
```

## [Level 19 &rarr; 20](https://overthewire.org/wargames/bandit/bandit20.html)

> To gain access to the next level, you should use the `setuid` binary in the `home` directory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (`/etc/bandit_pass`), after you have used the `setuid` binary.

```bash
$ ssh bandit19@bandit.labs.overthewire.org -p 2220
# list directory's files
bandit19@bandit:~$ ls
bandit20-do
# check the file's type
bandit19@bandit:~$ file bandit20-do
bandit20-do: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=037b97b430734c79085a8720c90070e346ca378e, for GNU/Linux 3.2.0, not stripped
# execute binary
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
# check file's permissions
bandit19@bandit:~$ ls -l bandit20-do
-rwsr-x--- 1 bandit20 bandit19 14876 Oct  5 06:19 bandit20-do
# list directory's files
bandit19@bandit:~$ ls /etc/bandit_pass
bandit0  bandit10  bandit12  bandit14  bandit16  bandit18  bandit2   bandit21  bandit23  bandit25  bandit27  bandit29  bandit30  bandit32  bandit4  bandit6  bandit8
bandit1  bandit11  bandit13  bandit15  bandit17  bandit19  bandit20  bandit22  bandit24  bandit26  bandit28  bandit3   bandit31  bandit33  bandit5  bandit7  bandit9
# check file's permissions
bandit19@bandit:~$ ls -l /etc/bandit_pass/bandit20
-r-------- 1 bandit20 bandit20 33 Oct  5 06:19 /etc/bandit_pass/bandit20
```

1. We have a binary file (`bandit20-do`) which is used to run a command as the user `bandit20`.
2. We can execute this file because it belongs to the `bandit19` group which has execute permissions (`x`). 
3. The `bandit20` password file can only be read by the user `bandit20`.

As a result, we have to use the binary and pass the command to read the file as `bandit20`:

```bash
# read the file as the user 'bandit20'
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
VxCazJaVykI6W36BkBU0mJTCM8rR95XT
```

## [Level 20 &rarr; 21](https://overthewire.org/wargames/bandit/bandit21.html)

> There is a `setuid` binary in the `home` directory that does the following: it makes a connection to `localhost` on the port you specify as a command-line argument. It then reads a line of text from the connection and compares it to the password in the previous level (`bandit20`). If the password is correct, it will transmit the password for the next level (`bandit21`).

> NOTE: Try connecting to your own network daemon to see if it works as you think.

```bash
$ ssh bandit20@bandit.labs.overthewire.org -p 2220
```

We can create a **onetime server**, a server that sends one message and then disconnects, using `nc -lp` and then pass it a message with the combination of the `echo` command and the pipe (`|`) operator. We can background this operation using `&` at the end so we can continue to use our terminal instead of opening a new one:

```bash
bandit20@bandit:~$ echo -n 'VxCazJaVykI6W36BkBU0mJTCM8rR95XT' | nc -lp 1337 &
[1] 3062056
```

Now we need to run the binary using the same port as our server (`1337`) so it can connect to it, receive the password inputted through `echo`, and sends us back the new one:

```bash
bandit20@bandit:~$ ./suconnect 1337 VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Read: VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Password matches, sending next password
NvEJF7oVjkddltPSrdKEFOllh9V1IBcq
[1]+  Done                    echo -n 'VxCazJaVykI6W36BkBU0mJTCM8rR95XT' | nc -lp 1337
```

## [Level 21 &rarr; 22](https://overthewire.org/wargames/bandit/bandit22.html)

> A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

```bash
$ ssh bandit21@bandit.labs.overthewire.org -p 2220

# list directory files
bandit21@bandit:~$ ls /etc/cron.d
cronjob_bandit15_root  cronjob_bandit22  cronjob_bandit24       e2scrub_all  sysstat
cronjob_bandit17_root  cronjob_bandit23  cronjob_bandit25_root  otw-tmp-dir

# display the file content
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null

# display the file content
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

The above bash script modifies the permissions (`chmod 644`) of the `/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv` file and then copies the next level's password to that file. The `644` permissions correspond to the owner of the file (`bandit22`) having read (`r`) and write (`w`) permissions and the group and others having read permissions only. As a result, everyone can read it. 

```bash
# check file's permissions
bandit21@bandit:/etc/cron.d$ ls -l /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
-rw-r--r-- 1 bandit22 bandit22 33 Jan  3 20:22 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv

bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff
```

## [Level 22 &rarr; 23](https://overthewire.org/wargames/bandit/bandit23.html)

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

> NOTE: Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.

```bash
$ ssh bandit22@bandit.labs.overthewire.org -p 2220

bandit22@bandit:~$ ls -l /etc/cron.d
total 36
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit15_root
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit17_root
-rw-r--r-- 1 root root 120 Oct  5 06:19 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct  5 06:19 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct  5 06:19 cronjob_bandit24
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit25_root
-rw-r--r-- 1 root root 201 Jan  8  2022 e2scrub_all
-rwx------ 1 root root  52 Oct  5 06:20 otw-tmp-dir
-rw-r--r-- 1 root root 396 Feb  2  2021 sysstat

bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null

bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

Let's break down what this bash script does:
1. `myname=$(whoami)` The `whoami` commands outputs the current user and since this is written by `bandit23`, the `myname` variable will be assigned that name.
2. `mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)` The first part just outputs 'I am user bandit23', the second part hashes that string using the MD5 hashing algorithm, and then third part splits the output using space as the delimiter and picks the first field. The latter is then assigned to the variable `mytarget`.
3. Then goes on to echo the following string: "Copying passwordfile /etc/bandit_pass/bandit23 to /tmp/<mytarget>".
4. Finally, it copies the password from `/etc/bandit_pass/bandit23` the a file under the `/tmp/` directory with the `mytarget`'s value as its name.

An example of what's happening:

```bash
# hashing the string using MD5
bandit22@bandit:~$ echo I am user bandit23 | md5sum
8ca319486bfbbc3663ea0fbe81326349  -

# selecting the first field of the output
bandit22@bandit:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
```

So the password should be stored in the following file `/tmp/8ca319486bfbbc3663ea0fbe81326349`.

```bash
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G
```

## [Level 23 &rarr; 24](https://overthewire.org/wargames/bandit/bandit24.html)

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

> NOTE: This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!

> NOTE 2: Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…

```bash
$ ssh bandit23@bandit.labs.overthewire.org -p 2220

bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null

bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```

Let's break down what the above bash script does:

The `myname` variable is assigned the output of the command `whoami` typed by the user `bandin24`. 

```bash
bandit23@bandit:~$ whoami
bandit23
```

Then iterates through all files within the `/var/spool/bandit24/foo` directory, ignores the current (`.`) and previous (`..`) directories, and then checks who is the owner of the file.  

```bash
bandit23@bandit:/tmp$ stat --format "%U" test.txt
bandit23
```

  > [`stat` command in Linux](https://linuxize.com/post/stat-command-in-linux/).

Finally, if the owner is the user `bandint23`, it executes the script. If the scripts runs for more than 60 seconds, then it will be forcefully terminated. Finally, it deletes the script.

As a result, we have to create a script that reads `bandit24`'s password, move it to the `/var/spool/bandit24/foo/` directory, and wait for it to execute. According to the output of `/etc/cron.d/cronjob_bandit24`, it executes every minute, so it should be executed within maximum of 1 minute.

```bash
# create a new director within /tmp
bandit23@bandit:~$ mkdir /tmp/lvl_23/
# move to the newly-created dir
bandit23@bandit:~$ cd /tmp/lvl_23
# create the required script
bandit23@bandit:/tmp/lvl_23$ nano bandit23.sh
# display the script's content
bandit23@bandit:/tmp/lvl_23$ cat bandit23.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/lvl_23/lvl_24_pass
# create the file that the password will be written to
bandit23@bandit:/tmp/lvl_23$ touch lvl_24_pass
# give appropriate permissions to the script, directory, and password file
bandit23@bandit:/tmp/lvl_23$ chmod +rx bandit23.sh
bandit23@bandit:/tmp/lvl_23$ chmod 777 /tmp/lvl_23
bandit23@bandit:/tmp/lvl_23$ chmod 777 lvl_24_pass
# check files' permissions
bandit23@bandit:/tmp/lvl_23$ ls -la
total 408
drwxrwxrwx    2 bandit23 bandit23   4096 Jan  4 17:18 .
drwxrwx-wt 3062 root     root     405504 Jan  4 17:19 ..
-rwxrwxr-x    1 bandit23 bandit23     67 Jan  4 17:17 bandit23.sh
-rwxrwxrwx    1 bandit23 bandit23      0 Jan  4 17:18 lvl_24_pass
# copy the script to the appropriate directory
bandit23@bandit:/tmp/bandit23_dir$ cp bandit23.sh /var/spool/bandit24/foo/
# wait for a minute and check if the file has changed
bandit23@bandit:/tmp/lvl_23$ cat lvl_24_pass
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar
```

## [Level 24 &rarr; 25](https://overthewire.org/wargames/bandit/bandit25.html)

> A daemon is listening on port `30002` and will give you the password for `bandit25` if given the password for `bandit24` and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called **brute-forcing**. You do not need to create new connections each time.

```bash
$ ssh bandit24@bandit.labs.overthewire.org -p 2220
```

We can connect to the listening port using `nc`:

```bash
bandit24@bandit:/tmp/lvl_24$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
# input the correct flag and a random 4-digit pincode
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar 0000
Wrong! Please enter the correct pincode. Try again.
```

Now we can create a brute-forcing script to get all the possible combinations. We can loop through all possible 4-digit combinations (`for i in {0000..9999}`), add each pin to the flag separated by a space (`echo "$password $i"`), and then append each sequence to a file (`>> pin_combinations.txt`). 

Passing the file as it is, i.e., with the 10000 resulting combinations, makes the connection to timeout, so we have to split it into 2 separate files (`split -l 5000 pin_combinations.txt pin_`). We can then pass each file to the daemon listening (`nc localhost 30002 < pin_aa > results_A` & `nc localhost 30002 < pin_ab >> results_A`), and search for a unique row in the final output (`sort results_A | uniq -u`):

```bash
bandit24@bandit:/tmp/lvl_24$ nano bruteForce.sh
bandit24@bandit:/tmp/lvl_23$ cat bruteForce.sh
#!/bin/bash

# set a variable with the previous level flag
password="VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar"
# confirm the password
echo "The password is: $password."

echo "Creating the pin combination file..."
# iterate through all combinations of a 4-digit password
for i in {0000..9999}
do
        # append the password plus the pin combination separated by a space to a file
        echo "$password $i" >> pin_combinations.txt
done
echo "Done."

echo "Splitting the file into two..."
# split the file into 2 separate files
split -l 5000 pin_combinations.txt pin_
echo "Done."

echo "Brute-force starting...passing the first file..."
# pass the first file and write the results
nc localhost 30002 < pin_aa > results_A
echo "Done."

echo "Brute-force continues...passing the second file..."
# pass the second file and write the results
nc localhost 30002 < pin_ab >> results_A
echo "Done."

echo "Searching for the flag..."
# search for the flag
sort results_A | uniq -u
echo "Flag found!"
```

Now all we have to do, is execute our script:

```bash
# execute the script
bandit24@bandit:/tmp/lvl_23$ ./bruteForce.sh
The password is: VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar.
Creating the pin combination file...
Done.
Splitting the file into two...
Done.
Brute-force starting...passing the first file...
Done.
Brute-force continues...passing the second file...
Done.
Searching for the flag...

Correct!
Exiting.
The password of user bandit25 is p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d
Timeout. Exiting.
Flag found!
```

## [Level 25 &rarr; 26](https://overthewire.org/wargames/bandit/bandit26.html)

> Logging in to `bandit26` from `bandit25` should be fairly easy… The shell for user `bandit26` is not `/bin/bash`, but something else. Find out what it is, how it works and how to break out of it.

```bash
$ ssh bandit25@bandit.labs.overthewire.org -p 2220

# list directory's files
bandit25@bandit:~$ ls
bandit26.sshkey
# display file's content
bandit25@bandit:~$ cat bandit26.sshkey
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0ECgYEA1crBUAR1gSkM+5mGjjoFLJKrFP+IhUHFh25qGI4Dcxxh1f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
```

First, since there is a private key lying around, let's copy and paste it to our machine since we will use to log in to the next level:

```bash
# check file's content
$ head -5 id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
# assign the appropriate permissions to the file
$ sudo chmod 400 id_rsa
# check file's permissions
$ ls -l id_rsa
-r-------- 1 root root 1679 Jan  5 06:56 id_rsa
```

Then going back to our SSH connection, we can check which shell is assigned to each user by checking the `/etc/passwd` file:

```bash
# check users' assigned shells
bandit25@bandit:~$ cat /etc/passwd | grep 'bandit25\|bandit26'
bandit25:x:11025:11025:bandit level 25:/home/bandit25:/bin/bash
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
# check file's content
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

For the user `bandit26` a script called `showtext` is assigned as a shell, which opens the `text.txt` file using `more`. [`more`](https://linux.die.net/man/1/more) is used to view large text files, displaying one screen at a time. Its **interactive mode** only works when the file's content is too large to fully be displayed in the current terminal window and it is based on the `vi` text editor.

As this level's instructions say, we must find a way to break out of `more`. From playing many fullpwn CTFs and constantly using [GTFOBins](https://gtfobins.github.io/gtfobins/vi/#shell), we know that commands can be passed to `vi` and it can be used to break out from restricted environments by spawing an interactive system shell:

![](gtfobins_vi.png){: .normal}

As a result, we can try limiting our terminal's display for `more`'s interactive mode to work, and then spawn a shell through `vi` (using option (b)):

![](level_25_to_26.png){: .normal}

```bash
# connect as bandit26 to SSH
$ sudo ssh bandit26@bandit.labs.overthewire.org -i id_rsa -p 2220
```

After logging in we are in `vi`'s command mode:

![](more_login.png){: .normal}

Now, we can press `v` to go into `vi` and follow GTFOBins instructions:

```bash
# set the user's shell to /bin/bash
:set shell=/bin/bash
# drop into the above-defined shell
:shell
bandit26@bandit:~$
```

Now, we can just read the password of `bandit26` and proceed to the next level:

```bash
bandit26@bandit:~$ cat /etc/bandit_pass/bandit26
c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1
```

## [Level 26 &rarr; 27](https://overthewire.org/wargames/bandit/bandit27.html)

> Good job getting a shell! Now hurry and grab the password for `bandit27`!

To get the password for `bandit27`, we have to login using the solution of the previous level. Once we reach the point that we have dropped on a shell we can see what's within the user's home directory:

```bash
# list directory's files
bandit26@bandit:~$ ls
bandit27-do  text.txt
# use the provided binary to read next level's password
bandit26@bandit:~$ ./bandit27-do
Run a command as another user.
  Example: ./bandit27-do id
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS
```

## [Level 27 &rarr; 28](https://overthewire.org/wargames/bandit/bandit28.html)

> There is a git repository at `ssh://bandit27-git@localhost/home/bandit27-git/repo` via the port `2220`. The password for the user `bandit27-git` is the same as for the user `bandit27`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit27@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp
bandit27@bandit:~$ mkdir /tmp/lvl_27
# move the the /tmp directory
bandit27@bandit:~$ cd /tmp/lvl27
# clone the git repo
bandit27@bandit:/tmp/lvl_27$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit27/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
# list directory's contents
bandit27@bandit:/tmp/lvl_27$ ls
repo
bandit27@bandit:/tmp/lvl_27$ cd repo
bandit27@bandit:/tmp/lvl_27/repo$ ls
README
bandit27@bandit:/tmp/lvl_27/repo$ cat README
The password to the next level is: AVanL161y9rsbcJIsFHuw35rjaOM19nR
```

## [Level 28 &rarr; 29](https://overthewire.org/wargames/bandit/bandit29.html)

> There is a git repository at `ssh://bandit28-git@localhost/home/bandit28-git/repo` via the port `2220`. The password for the user `bandit28-git` is the same as for the user `bandit28`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit28@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit28@bandit:~$ mkdir /tmp/lvl_28 && cd /tmp/lvl_28
# clone the repo
bandit28@bandit:/tmp/lvl_28$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit28/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password:
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
# display file's content
bandit28@bandit:/tmp/lvl_28$ cat repo/README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
```

We can interact with this repository as it was ours and we can use all `git` commands on it. We can see the logs as follows:

```bash
# check the git's logs
bandit28@bandit:/tmp/lvl_28/repo$ git log
commit 14f754b3ba6531a2b89df6ccae6446e8969a41f3 (HEAD -> master, origin/master, origin/HEAD)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    fix info leak

commit f08b9cc63fa1a4602fb065257633c2dae6e5651b
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    add missing data

commit a645bcc508c63f081234911d2f631f87cf469258
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    initial commit of README.md
```

From the above output we notice the following:
1. The first commit was the creation of the `README.md` file.
2. The second one has as comment "*add missing data*" so this is when `Morla` probably wrote the credentials.
3. The thild and last commit has as comment "*fix info leak*" which is problably when the plaintext password was changed to its current form, i.e., `xxxxxxxxxx`.

So we can find the second commit and get the plaintext password:

```bash
# show the defined commit
bandit28@bandit:/tmp/lvl_28/repo$ git show f08b9cc63fa1a4602fb065257633c2dae6e5651b
commit f08b9cc63fa1a4602fb065257633c2dae6e5651b
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    add missing data

diff --git a/README.md b/README.md
index 7ba2d2f..b302105 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials

 - username: bandit29
-- password: <TBD>
+- password: tQKvmcwNYcFS6vmPHIUSI3ShmsrQZK8S
```

## [Level 29 &rarr; 30](https://overthewire.org/wargames/bandit/bandit30.html)

> There is a git repository at `ssh://bandit29-git@localhost/home/bandit29-git/repo` via the port `2220`. The password for the user `bandit29-git` is the same as for the user `bandit29`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit29@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit29@bandit:~$ mkdir /tmp/lvl_29 && cd /tmp/lvl_29
# clone the repo
bandit29@bandit:/tmp/lvl_29$ git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit29/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
# display the file's contents
bandit29@bandit:/tmp/lvl_29$ cat repo/README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>
```

We can repeat the process of the previous level to see what we can find:

```bash
# check logs
bandit29@bandit:/tmp/lvl_29$ cd repo && git log
commit 4364630b3b27c92aff7b36de7bb6ed2d30b60f88 (HEAD -> master, origin/master, origin/HEAD)
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:43 2023 +0000

    fix username

commit fca34ddb7d1ff1f78df36538252aea650b0b040d
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:43 2023 +0000

    initial commit of README.md
```

After checking both logs, it does not seem that they include anything of interest. The `README.md` file mentioned "*no password in production!*" which suggests that there might be more than one branch, a development one and a production one. We can list all branches as follows:

```bash
# list branches
bandit29@bandit:/tmp/lvl_29/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

There is indeed a development branch (`dev`), so we can switch to it and check what's in there:

```bash
# switch to the dev branch
bandit29@bandit:/tmp/lvl_29/repo$ git checkout dev
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
Switched to a new branch 'dev'
# check directory's contents
bandit29@bandit:/tmp/lvl_29/repo$ ls -la
total 20
drwxrwxr-x 4 bandit29 bandit29 4096 Jan  5 09:35 .
drwxrwxr-x 3 bandit29 bandit29 4096 Jan  5 09:27 ..
drwxrwxr-x 2 bandit29 bandit29 4096 Jan  5 09:35 code
drwxrwxr-x 8 bandit29 bandit29 4096 Jan  5 09:35 .git
-rw-rw-r-- 1 bandit29 bandit29  134 Jan  5 09:35 README.md
# display file's contents
bandit29@bandit:/tmp/lvl_29/repo$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: xbhV3HpNGlTIdnjUrdAlPzc2L6y9EOnS
```

## [Level 30 &rarr; 31](https://overthewire.org/wargames/bandit/bandit31.html)

> There is a git repository at `ssh://bandit30-git@localhost/home/bandit30-git/repo` via the port `2220`. The password for the user `bandit30-git` is the same as for the user `bandit30`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit30@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit29@bandit:~$ mkdir /tmp/lvl_30 && cd /tmp/lvl_30
# clone the repo
bandit29@bandit:/tmp/lvl_29$ git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit29/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
# display the file's contents
bandit30@bandit:/tmp/lvl_30$ cat repo/README.md
just an epmty file... muahaha
```

Like most VCSs, Git has the ability to **tag** specific points in a repository’s history as being important. Typically, people use this functionality to mark release points (v1.0, v2.0 and so on).

> [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)

```bash
# check the current tags
bandit30@bandit:/tmp/lvl_30/repo$ git tag
secret
# show the tag's content
bandit30@bandit:/tmp/lvl_30/repo$ git show secret
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt
```

## [Level 31 &rarr; 32](https://overthewire.org/wargames/bandit/bandit32.html)

> There is a git repository at `ssh://bandit31-git@localhost/home/bandit31-git/repo` via the port `2220`. The password for the user `bandit31-git` is the same as for the user `bandit31`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit31@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit31@bandit:~$ mkdir /tmp/lvl_31 && cd /tmp/lvl_31
# clone the repo
bandit31@bandit:/tmp/lvl_31$ git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
# display file's content
bandit31@bandit:/tmp/lvl_31$ cat repo/README.md
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

According to the `README.md` file, we will need to create a file meetings the required specifications and then push it to the repo. 

```bash
# create the file
bandit31@bandit:/tmp/lvl_31/repo$ echo "May I come in?" > key.txt
# check that the file is created
bandit31@bandit:/tmp/lvl_31/repo$ ls -la
total 24
drwxrwxr-x 3 bandit31 bandit31 4096 Jan  6 21:35 .
drwxrwxr-x 3 bandit31 bandit31 4096 Jan  6 21:33 ..
drwxrwxr-x 8 bandit31 bandit31 4096 Jan  6 21:38 .git
-rw-rw-r-- 1 bandit31 bandit31    6 Jan  6 21:33 .gitignore
-rw-rw-r-- 1 bandit31 bandit31   15 Jan  6 21:35 key.txt
-rw-rw-r-- 1 bandit31 bandit31  147 Jan  6 21:33 README.md
# display file's content
bandit31@bandit:/tmp/lvl_31/repo$ cat key.txt
May I come in?
```

The sequence for pushing a file to a Git repo is:
1. Record changes to the repo via [`git commit`](https://git-scm.com/docs/git-commit).
2. Update remote refs along with associated object via [`git push`](https://git-scm.com/docs/git-push).

Before doing that, we can see that there is a [`.gitignore`](https://git-scm.com/docs/gitignore) file in our directory:

```bash
# display file's content
bandit31@bandit:/tmp/lvl_31/repo$ cat .gitignore
*.txt
```

`.gitignore` specifies intentionally untracked files to ignore. In this case, it ignores all `.txt` files (`*.txt`). So trying to go over the above 2-step sequence won't work in this case.

To add the file anyway we can use [`git add`](https://git-scm.com/docs/git-add), which add file contents to the index, before using `git commit`:

```bash
# add file contents to the index
bandit31@bandit:/tmp/lvl_31/repo$ git add -f key.txt
# record the changes to the repo
bandit31@bandit:/tmp/lvl_31/repo$ git commit -a
Unable to create directory /home/bandit31/.local/share/nano/: No such file or directory
It is required for saving/loading search history or cursor positions.

[master 625a650] A random message!
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
# update remote refs
bandit31@bandit:/tmp/lvl_31/repo$ git push
<SNIP>
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 327 bytes | 327.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: rmCBvG56y58BXzv98yZGdO7ATVL5dW8y
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo'
```

## [Level 32 &rarr; 33](https://overthewire.org/wargames/bandit/bandit33.html)

> After all this git stuff its time for another escape. Good luck!

```bash
$ ssh bandit32@bandit.labs.overthewire.org -p 2220
WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: Permission denied
```

It seems that everything we type is automatically converted to uppercase! All the Linux commands are lowercase, so we can't really pass any command. But we can use [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/) which, by convention, have uppercase names.

More specifically, there is the [`$0`](https://linuxhandbook.com/bash-dollar-0/) special variable which can be used in two ways:
1. To find the logged-in shell.
2. To print the name of the script that is being executed.

We are interested in the first use!

```bash
# drop into the logged-in shell
>> $0
# read the password
$ cat /etc/bandit_pass/bandit33
odHo63fHiFqcWWJG9rLiLDtPm45KzUKy
```

## [Level 32 &rarr; 33](https://overthewire.org/wargames/bandit/bandit33.html)

> At this moment, level 34 does not exist yet.

```bash
$ ssh bandit33@bandit.labs.overthewire.org -p 2220

# list directory's files
bandit33@bandit:~$ ls
README.txt
# display file's content
bandit33@bandit:~$ cat README.txt
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game. However, we are constantly working
on new levels and will most likely expand this game with more levels soon.
Keep an eye out for an announcement on our usual communication channels!
In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
```