---
title: PicoCTF - Don't use client-side
date: 2023-12-28
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, dont-use-client-side]
img_path: /assets/picoctf/web_exploitation/dont_use_client_side
published: true
image:
    path: ../../picoctf_logo.png
---

![](room_banner.png){: width="70%" .normal}

1. The website lands us on a secure login portal:

    ![](home.png){: .normal}

2. If we view the page's source code, we will notice a function called `verify` that has everything we need:

    ![](source_code.png){: .normal}

    ![](pass_verified.png){: .normal}
