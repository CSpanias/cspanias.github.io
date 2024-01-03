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
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = localhost
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = localhost
verify error:num=10:certificate has expired
notAfter=Dec 31 16:51:29 2023 GMT
verify return:1
depth=0 CN = localhost
notAfter=Dec 31 16:51:29 2023 GMT
verify return:1
---
Certificate chain
 0 s:CN = localhost
   i:CN = localhost
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA1
   v:NotBefore: Dec 31 16:50:29 2023 GMT; NotAfter: Dec 31 16:51:29 2023 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDCzCCAfOgAwIBAgIEd2zsFjANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDDAls
b2NhbGhvc3QwHhcNMjMxMjMxMTY1MDI5WhcNMjMxMjMxMTY1MTI5WjAUMRIwEAYD
VQQDDAlsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDa
I/3T3+5jb1P6JKLTAiKno5vP4XblDAMrz5DXYPPp2xMChk9qt/gJIk0DFqqBAaMT
NdeQAwbOE7p/vFUYr2VK/lRLD1hwPYvUWDcnaM54POA5DZWtsxkNmlf8TsV+CJbq
Wy/HF7wGxCIJTU85/BCAvjztaB6GiwNF1tK67gY3OMi17Y/OZcup5OlfsOc2Z1K8
JQTxUpLL+dKctD0MPm5wyRG3k7Er4nE+Ww+wQl+tvibxYdmI8ln5p7R302bFbMny
tYrEMwcMnXiZ/as2lC918s+mkMDF2N29vdc2z+yh8nxpbvB9Wnm8caWnz8Bgzlhm
Uf6Dr1X/OW9Sqr52CoafAgMBAAGjZTBjMBQGA1UdEQQNMAuCCWxvY2FsaG9zdDBL
BglghkgBhvhCAQ0EPhY8QXV0b21hdGljYWxseSBnZW5lcmF0ZWQgYnkgTmNhdC4g
U2VlIGh0dHBzOi8vbm1hcC5vcmcvbmNhdC8uMA0GCSqGSIb3DQEBBQUAA4IBAQAD
Axuf0o+lYLoAwbYBQ9u4TQGXVDP8THKIGvLA5YoQ66WTS+Yqz6UyU2KKWIXIJOPg
3m4pjssfW61KbE76ALqGNoXqX3/3zhhFEOxeKdu7oto54xeC9E6pLF+VRkOLBsER
vkVV04gIHvW6bJPJcqroW/hpkj8gFErOcKnV5Q+XWdjFs7mFNzMQWEViaU4Tv8Vb
VHvFd1H7QVO5jTqDeReKa1EX1TKhsFN5ZdeGFNW4lGMOMagretF0SggYQ/jXxTQq
ZlE48UQ2UjPmJ2Q93A7Zz9Q79SzdoxjAysD/z7r1V8cRM8XsUUt4EQsc/LcISu/5
shdDpgGChFBkzNY/2zYw
-----END CERTIFICATE-----
subject=CN = localhost
issuer=CN = localhost
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1339 bytes and written 373 bytes
Verification error: certificate has expired
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 10 (certificate has expired)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 3B86333C302F8578A6176621393A0747016984714B27D1A6A5FEDE2597D652D5
    Session-ID-ctx:
    Resumption PSK: 244515B670C10CA822DBF2F4060EDCB0CEE099447770D7A6E5DE75E8CFA2D75C61071DE462546EEC6CABAD3D7BE44DCC
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 35 fa 11 f4 72 e4 41 40-5c 24 4b 0a 01 db d5 57   5...r.A@\$K....W
    0010 - da c8 8d 16 25 05 b7 38-1a b2 17 31 a4 d2 6e f3   ....%..8...1..n.
    0020 - af be 8e 98 19 70 71 f0-15 ae 2d a1 73 ab cd 03   .....pq...-.s...
    0030 - ec 5c b7 06 a9 7e 86 8a-0d ae 74 33 a1 6c 5b 92   .\...~....t3.l[.
    0040 - 05 ba fe 65 be fb e7 91-eb a5 e6 f5 56 ed d3 1f   ...e........V...
    0050 - 22 20 0d 1d e1 3a a4 e2-04 5e 97 8b d8 6b c8 be   " ...:...^...k..
    0060 - c0 1c 1b 29 89 0a ff c6-2b 2f b1 ca d5 32 60 89   ...)....+/...2`.
    0070 - e6 50 02 8b 6c 7f 20 85-8a fc f9 7a 08 88 74 f0   .P..l. ....z..t.
    0080 - ab d7 7d b2 f1 36 61 47-aa d2 10 97 c2 3d 48 65   ..}..6aG.....=He
    0090 - 5c 3b a4 f7 0c 99 d2 57-73 24 8a 71 22 72 6f 99   \;.....Ws$.q"ro.
    00a0 - 69 f7 bf d9 ee c6 24 9b-44 2f e7 4f 88 df b9 85   i.....$.D/.O....
    00b0 - dc 64 91 c8 08 2e b4 5a-07 4b af 19 f2 45 a2 9a   .d.....Z.K...E..
    00c0 - c5 0e 74 1c 65 54 c1 ba-c3 70 c3 6b f5 f1 bf a5   ..t.eT...p.k....

    Start Time: 1704279091
    Timeout   : 7200 (sec)
    Verify return code: 10 (certificate has expired)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 83BF2A44BE2577608B8B5425F48D6F30CE1E84F2188616F6F8F5501A263B656F
    Session-ID-ctx:
    Resumption PSK: 9752FC0B4274A14E9BF9515B11E6107787089D5F7909E15BF0785A33814390BB54FC7DF33BBE8AE405933B5FDC9CA88A
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 35 fa 11 f4 72 e4 41 40-5c 24 4b 0a 01 db d5 57   5...r.A@\$K....W
    0010 - bb a0 fa 0a 70 eb 0e 18-cf 8c a4 11 87 d8 d4 e9   ....p...........
    0020 - 2f 43 15 19 4e 86 35 85-9f bf 32 ce 7e 64 b3 dc   /C..N.5...2.~d..
    0030 - 5a 4e 0f c3 5c b2 90 34-89 24 4c 13 c0 90 71 4c   ZN..\..4.$L...qL
    0040 - 9f 3a 4f 5a d5 85 26 81-ae 28 cf f9 3a 71 73 2f   .:OZ..&..(..:qs/
    0050 - e6 83 8b e0 7b 91 8a 51-e5 f2 0f 86 ce e5 d0 78   ....{..Q.......x
    0060 - 97 f7 cf a6 e1 22 5c 95-21 17 30 95 49 8d f8 b4   ....."\.!.0.I...
    0070 - da 6e 77 5a ad f6 0b c6-1c 60 b0 f5 da a2 6c 40   .nwZ.....`....l@
    0080 - 0c 18 50 33 d5 49 1b 1d-33 cc 13 5a 91 8b e6 5a   ..P3.I..3..Z...Z
    0090 - 0c 66 a9 3b 8d a5 79 d7-ea 14 a3 79 9d 50 11 23   .f.;..y....y.P.#
    00a0 - e3 40 d5 ec 6c e7 62 ac-19 78 63 cf 2c 21 e5 33   .@..l.b..xc.,!.3
    00b0 - 34 5f 65 f6 cb 26 b7 9c-a7 73 71 16 04 a8 88 9a   4_e..&...sq.....
    00c0 - 54 05 b4 e0 3e 56 7c 10-bd ee ed 10 5f d4 46 e9   T...>V|....._.F.

    Start Time: 1704279091
    Timeout   : 7200 (sec)
    Verify return code: 10 (certificate has expired)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
Correct!
JQttfApK4SeyHwDlI9SXGR50qclOAil1
```

## [Level 16 &rarr; 17](https://overthewire.org/wargames/bandit/bandit17.html)

> The credentials for the next level can be retrieved by submitting the password of the current level to a port on `localhost` in the range `31000` to `32000`. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

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

# use nmap to scan the ports found above to check which one uses SSL
bandit16@bandit:~$ nmap localhost -sV -p 31518, 31790 -T4
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-03 11:37 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00010s latency).

PORT      STATE SERVICE  VERSION
31518/tcp open  ssl/echo

Nmap scan report for 31790 (0.0.124.46)
Host is up (0.00019s latency).

PORT      STATE  SERVICE VERSION
31518/tcp closed unknown

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 2 IP addresses (2 hosts up) scanned in 52.93 seconds

# connecting on port 31790
bandit16@bandit:~$ openssl s_client -connect localhost:31790
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = localhost
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = localhost
verify error:num=10:certificate has expired
notAfter=Dec 31 16:51:30 2023 GMT
verify return:1
depth=0 CN = localhost
notAfter=Dec 31 16:51:30 2023 GMT
verify return:1
---
Certificate chain
 0 s:CN = localhost
   i:CN = localhost
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA1
   v:NotBefore: Dec 31 16:50:30 2023 GMT; NotAfter: Dec 31 16:51:30 2023 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDCzCCAfOgAwIBAgIESXSR6jANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDDAls
b2NhbGhvc3QwHhcNMjMxMjMxMTY1MDMwWhcNMjMxMjMxMTY1MTMwWjAUMRIwEAYD
VQQDDAlsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDf
zwpJ6DLZ0kO/ln7nmNz0hMpvNOT2Fhn/BxEFWpFUxlb/0/QWhPC5JSfMlxhM7H3H
pvDOzN1aG21I55wXB2OCtWK7EPjSY3Kb2woA4L4No80acYINoiEiR7U1qG5rNE+T
okH4d7xvQa8I45NG5JTm4yIdpbjP6SP9z/W8eYWHkuceF3zirkCixtvObJG0+cJK
qEWD/FrVQ9E+qmFrOEGlXTzcK3M5XAkdAwg84yDmOTEF76b69o5j+g5bm+X6w1m0
LRpxr0XSDBpHJ6Fgb4gKc3MmHxF8Qbhig6kJB77r5uYJgKLo2nebzsYUIdhAVCj0
bLzKZY9F2QjZ6BowxES5AgMBAAGjZTBjMBQGA1UdEQQNMAuCCWxvY2FsaG9zdDBL
BglghkgBhvhCAQ0EPhY8QXV0b21hdGljYWxseSBnZW5lcmF0ZWQgYnkgTmNhdC4g
U2VlIGh0dHBzOi8vbm1hcC5vcmcvbmNhdC8uMA0GCSqGSIb3DQEBBQUAA4IBAQC7
k7wv/qUszdJGE92/QZuUaDYd16yhHQX7fnqL9i7op/C+zsLljj5srXb9qGyhwn0o
s0YBL5vVFpXU7Q6GX2n9eUvaHIT/iXCUTq4/RmjGJ9n165zN8JVRe5gzvDNmkpuu
cAyFT3f4yCZmZK8EQcAmINwzCUGwiKccrUNxA3bf6kafc59qhgg5+IrqY4D5XjLr
b4yOXzIK1qTMWR9utI5fpmwjAkrAW4EWZAEr8N/Ww7dyqiN4cO8HJgCWXEbGK4eP
1dOGKqZGy7vtqlfqYqu5V794GxvEqgh2UQDxJfqA65SYjn7TJsORjwisiCpvod/U
eVdny9PstWp8PUe7GFQJ
-----END CERTIFICATE-----
subject=CN = localhost
issuer=CN = localhost
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1339 bytes and written 373 bytes
Verification error: certificate has expired
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 10 (certificate has expired)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 6474427E7761D5C5DF814B16498F70D464320D43B99F13E2ECBB37A99FA2FD4D
    Session-ID-ctx:
    Resumption PSK: 7F6A839E58576DCDEA901882BBEFEB04ADBA8230552EDFE2C8EAA8C6CA2971903872FE6E796477CE76B62C48120981AA
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 2d 36 88 37 92 9e 74 f5-2c d7 85 e8 62 8b 89 87   -6.7..t.,...b...
    0010 - 60 d1 35 62 f1 30 4a 1a-63 11 a1 f5 14 3d ce 5e   `.5b.0J.c....=.^
    0020 - a8 a5 88 15 0a 1d cb ee-27 86 00 ad 69 cf 4f 16   ........'...i.O.
    0030 - 5d 22 73 df ab 50 0a b3-3c 56 41 f2 b1 8f 13 9a   ]"s..P..<VA.....
    0040 - 34 4b 41 0d 64 72 59 0a-fb e2 b8 1f 5e ef 98 81   4KA.drY.....^...
    0050 - e9 14 fc 3c 1c 13 5e 32-ee 39 e7 59 2b 80 5b 89   ...<..^2.9.Y+.[.
    0060 - c6 86 33 6b b0 14 77 ca-68 27 18 ee 53 99 6b 74   ..3k..w.h'..S.kt
    0070 - 70 96 a8 dc 38 d0 cf c7-86 9b e9 af a9 d0 6b ab   p...8.........k.
    0080 - fd 5e 50 72 53 0b d0 99-3d cb 17 35 8c 85 59 2d   .^PrS...=..5..Y-
    0090 - 08 97 e6 5e 5a d4 c2 d1-80 ca a8 c6 1f e1 1f 10   ...^Z...........
    00a0 - c1 72 10 b1 ea 12 b3 2d-68 94 ae a0 b2 94 3b 1c   .r.....-h.....;.
    00b0 - af f1 e7 76 f0 08 a7 73-bd 6a 33 3d 0c 1f f3 9e   ...v...s.j3=....
    00c0 - 60 1d ee dd fd b2 37 65-54 20 c5 a2 50 84 37 c9   `.....7eT ..P.7.

    Start Time: 1704281686
    Timeout   : 7200 (sec)
    Verify return code: 10 (certificate has expired)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 6098570B673D4550A391465206111B4763E716B57E46E596621C74044780BBFA
    Session-ID-ctx:
    Resumption PSK: 64ECC786DFE93C5147C4357D9221289A4825737C9E084047C57CBB92828E460C3422BDC7BCF5C101FF8E7C0585658257
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 2d 36 88 37 92 9e 74 f5-2c d7 85 e8 62 8b 89 87   -6.7..t.,...b...
    0010 - 83 7c 4d 3e 44 c6 ea 75-f5 db 65 c7 85 b5 ce 16   .|M>D..u..e.....
    0020 - e8 84 f5 a4 98 fa 2b b6-e2 1c e2 a7 37 cd 95 ab   ......+.....7...
    0030 - 0c 84 b4 97 7f bf 3f 56-55 72 24 4e 2a 1c ce ba   ......?VUr$N*...
    0040 - e4 c5 55 c6 27 5c 2a 82-bc c1 cf 95 12 38 47 05   ..U.'\*......8G.
    0050 - 9f 8c 4d 39 ea 54 23 25-ed 89 5c 4e 8c a2 1d ca   ..M9.T#%..\N....
    0060 - c7 0a b0 ba ea 50 ed 88-1c 85 41 d1 4e f5 ab db   .....P....A.N...
    0070 - b2 c0 16 fe cb 50 d1 bc-b1 7f 25 b6 0b 1b c8 b8   .....P....%.....
    0080 - 8d d9 35 d0 48 89 dc 1e-05 85 1c f0 e4 67 83 f4   ..5.H........g..
    0090 - bf 35 bd a1 69 44 f1 04-42 18 ce 8a 1c db ac 62   .5..iD..B......b
    00a0 - 07 af 7f 6f f7 1b 7b 36-1d bd 8c ac e3 fb 3b fb   ...o..{6......;.
    00b0 - 10 18 a8 28 b2 aa 36 7b-75 76 1c 5b 66 bf cf 98   ...(..6{uv.[f...
    00c0 - 0f bf 8f 16 9d 22 8d 1e-ec a2 22 d5 7c c1 8f 1d   ....."....".|...

    Start Time: 1704281687
    Timeout   : 7200 (sec)
    Verify return code: 10 (certificate has expired)
    Extended master secret: no
    Max Early Data: 0
---
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


