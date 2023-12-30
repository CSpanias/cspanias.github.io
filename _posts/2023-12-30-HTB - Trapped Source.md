---
title: HTB - Trapped Source
date: 2023-12-30
categories: [CTF, Web]
tags: [ctf, web, web-exploitation, htb, hack-the-box, trapped-source]
img_path: /assets/ctf/web/htb/trapped_source
published: true
---

![](room_banner.png)

## Overview

|:-:|:-:|
|Challenge|[Trapped Source](https://app.hackthebox.com/challenges/trapped-source)|
|Rank|Very easy|
|Category|Web|

> **Challenge description**: _Intergalactic Ministry of Spies tested Pandora's movement and intelligence abilities. She found herself locked in a room with no apparent means of escape. Her task was to unlock the door and make her way out. Can you help her in opening the door?_

1. The home page includes a keypad which takes 4 digits:

    ![](home.png){ .normal}


2. The name of the challenge, *Trapped Source*, suggests to view the page's source code. If we do, we can see the variable `correctPin` with its value set to `7551`:

    > If you get a pin with the number `0` in it, just restart the machine from HTB. I encountered this during my first attempt and waste much time trying stuff to manually input the `0` as I thought that inputting the `0` was the actual challenge! 

    ![](source.png){ .normal}

3. We can submit the flag and mark this challenge as solved, either manually typing its value or by a copy and paste via inspector:

    ![](flag.png){ .normal}

    ![](flag_inspector.png){ .normal}


    ![](machine_pwned.png){: width="60%" .normal}