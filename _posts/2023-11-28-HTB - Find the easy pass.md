---
title: HTB - Find the easy pass
date: 2023-11-28
categories: [CTF, Reverse Engineering]
tags: [reverse-enginnering, exe, binary, windows, xxd, subl, ghidra, ollydbg]
img_path: /assets/find-the-easy-pass/
published: true
---

![](chall_banner.png)

## Overview

|:-:|:-:|
|Challenge|[Find the easy pass](https://app.hackthebox.com/challenges/5)|
|Rank|Easy|
|Time|45min|
|Category|Reverse Engineering|

## Quick solve

```shell
# download the required zip file
ls
'Find The Easy Pass.zip'

# unzip the file with the given password
unzip Find\ The\ Easy\ Pass.zip
Archive:  Find The Easy Pass.zip
[Find The Easy Pass.zip] EasyPass.exe password:
  inflating: EasyPass.exe

ls
 EasyPass.exe  'Find The Easy Pass.zip'
# check file type
file EasyPass.exe
EasyPass.exe: PE32 executable (GUI) Intel 80386, for MS Windows, 8 sections

# create a hex dump and write it to a file
xxd EasyPass.exe > bin_code
# read file with sublime
subl bin_code
```

> Search for "password" in Sublime.

<figure>
    <img src="subl_password_search.jpg"
    alt="Searching for the string 'password' in Sublime" >
</figure>

> Since 'fortan!' gave 'Wrong Password!', I tried 'fortran!' which is a [general-purpose programming language](https://en.wikipedia.org/wiki/Fortran) and it worked!

## Proper solution

> Taken from [haxez](https://haxez.org/2021/09/hack-the-box-reversing-find-the-easy-pass-has-been-pwned/).

```shell
# check file permissions
ls -l
total 2280
-rw-r--r-- 1 kali kali  402432 Jul  3  2017  EasyPass.exe
-rwxrwxrwx 1 kali kali  210291 Nov 28 14:02 'Find The Easy Pass.zip'

# give execute permissions to .exe
sudo chmod +x EasyPass.exe

# check again to confirm that .exe has execute permissions
ls -l
total 2280
-rwxr-xr-x 1 kali kali  402432 Jul  3  2017  EasyPass.exe
-rwxrwxrwx 1 kali kali  210291 Nov 28 14:02 'Find The Easy Pass.zip'

# run the program
./EasyPass.exe
```

<figure>
    <img src="pass_prompt.png"
    alt="Program launched" >
</figure>

```shell
# launch ghidra
ghidra
```

> [Ghidra](https://ghidra-sre.org/) is a reverse engineering tool, aka a disassembly tool, that was developed by the NSA and released in 2019 ([Ghidra quickstart & tutorial: Solving a simple crackme](https://www.youtube.com/watch?v=fTGTnrgjuGA)).

Search for the string 'password':

<figure>
    <img src="search_strings.png"
    alt="String search" >
</figure>

<figure>
    <img src="search_password_string.png"
    alt="'Password' string search" >
</figure>

Click on 'Wrong Password' (memory reference: `00454200`) and check References from main app:

<figure>
    <img src="ref_check.png"
    alt="Checking references" >
</figure>

<figure>
    <img src="wrong_pass_refs.png"
    alt="Memory location's references" >
</figure>

Repeat above step (memory ref: `00454144`) and click on the Function Graph icon (top bar):

<figure>
    <img src="function_graph.jpg"
    alt="Function Graph" >
</figure>

The above represents an `if` statement and the green arrow indicates that the function executed the second box (`00454144`). The last function call was `FUN_00404628`. Click on the function and check back on the main window (mem ref: `00454131`):

<figure>
    <img src="function_mem_ref.png"
    alt="Function's memory reference" >
</figure>

Double-click the function to reveal its logic. It takes 2 parameters, `param_1` and `param_2`, and then compares them. So we can 'safely' assume that one of them would be the correct one:

<figure>
    <img src="function_logic.jpg"
    alt="Function's logic" >
</figure>

We need to find out what is stored inside these parameters. Open `.exe` with `ollydgb`, find function's mem ref and toggle a breakpoint:

<figure>
    <img src="toggle_breakpoint.png"
    alt="Toggle breakpoint" >
</figure>

Now click the Play button on top and check the registers on the right-hand side:

<figure>
    <img src="registers.jpg"
    alt="Toggle breakpoint" >
</figure>

<figure>
    <img src="chall_pwned.png"
    alt="Challenge pwned" >
</figure>