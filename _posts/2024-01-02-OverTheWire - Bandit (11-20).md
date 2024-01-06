---
title: OverTheWire - Bandit (11-20)
date: 2024-01-02
categories: [OverTheWire, Bandit]
tags: [overthewire, bandit, linux]
img_path: /assets/overthewire/bandit
published: true
---

---

[Levels 0-10](https://cspanias.github.io/posts/OverTheWire-Bandit-(0-10)/)

---

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

---

[Levels 21-33](https://cspanias.github.io/posts/OverTheWire-Bandit-(21-33)/)

---