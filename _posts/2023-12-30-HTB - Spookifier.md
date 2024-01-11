---
title: HTB - Spookifier
date: 2023-12-30
categories: [CTF, Web]
tags: [ctf, web, web-exploitation, htb, hack-the-box, spookifier, ssti]
img_path: /assets/htb/web/spookifier
published: true
image:
    path: room_banner.png
---

## Overview

|:-:|:-:|
|Challenge|[Spookifier](https://app.hackthebox.com/challenges/spookifier)|
|Rank|Very easy|
|Category|Web|

> **Challenge description**: _There's a new trend of an application that generates a spooky name for you. Users of that application later discovered that their real names were also magically changed, causing havoc in their life. Could you help bring down this application?_

1. The home page includes input box which takes our name:

    ![](home.png)

2. After examining the challenge's files, we can see that this app is using the [Mako](https://www.fullstackpython.com/mako.html) template engine:

    ```shell
    # Dockerfile content
    $ cat Dockerfile
    FROM python:3.8-alpine

    RUN apk add --no-cache --update supervisor gcc
    # Upgrade pip
    RUN python -m pip install --upgrade pip

    # Install dependencies
    RUN pip install Flask==2.0.0 mako flask_mako Werkzeug==2.0.0

    <SNIP>
    ```

3. After searching for "*flask mako*" on Google, the first and third results were about **Server Side Template Injection (SSTI)**:

    ![](mako_ssti.png)

    > _**[SSTI](https://portswigger.net/web-security/server-side-template-injection)** is when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side._

4. There is a [list of payloads](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection) on Hacktricks for detecting SSTI, and upon trying the `${7*7}` we can see that is works:

    ![](ssti_detection.png)

5. [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#mako) also has a `Python Mako` section with specific payloads for that template:

```shell
cd ../;cat flag.txt
```