---
title: PicoCTF - Includes
date: 2023-12-29
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, includes]
img_path: /assets/picoctf/web_exploitation/includes
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The homepage includes some information about the `include` directive and contains a `Say hello` button:

    ![](home.png)

    ![](home_1.png)

2. By viewing the page's source code, we can see two links: one for the CSS file, `style.css`, and the other for the JavaScript code, `script.js`:

    ![](css.png)

    ![](js.png)

    By combining the two parts, we can submit the challenge's flag!