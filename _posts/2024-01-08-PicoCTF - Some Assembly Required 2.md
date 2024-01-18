---
title: PicoCTF - Some Assembly Required 2
date: 2024-01-18
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation]
img_path: /assets/picoctf/web_exploitation/some_assembly_required_2
published: true
image:
    path: ../../picoctf_logo.png
---

![](room_banner.png){: width="70%"}

> **Description**: _The web project was rushed and no security assessment was done. Can you read the `/etc/passwd` file?_

1. The homepage looks like this: 

    ![](home.png){: .normal width="70%"}

2. This is a continuation of the [Some Assembly Required 1](https://cspanias.github.io/posts/PicoCTF-Some-Assembly-Required-1/) challenge, and it looks pretty similar. If we use the browser's developer tools and look at the sources (where the flag in the first challenge was) we see the following:

    ![](wasm_code.png)

3. If we grab the string inside the double quotes and put it into CyberChef's Intensive mode, we can see the flag, which is decoded using XOR with the value `8` as the key:

    ![](flag.png)

    ![](flag_browser.png)