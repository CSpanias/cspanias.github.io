---
title: PicoCTF - Login
date: 2024-01-08
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, login]
img_path: /assets/picoctf/web_exploitation/login
published: true
---

![](room_banner.png){: width="70%"}

> **Description**: _My dog-sitter's brother made this website but I can't get in; can you help?_

1. The homepage consists of a login form:

    ![](home.png){: .normal width="70%"}

2. While viewing the page's source code, we can see a JavaScript script called `index.js`:

    ![](source.png){: .normal width="70%"}

3. Opening the JS file, there is a string that looks encoded. If we put that into [Cyberchef](https://gchq.github.io/CyberChef) and let it work its magic, we will get the flag:

    ![](js_script.png){: .normal}

    ![](flag.png){: .normal}