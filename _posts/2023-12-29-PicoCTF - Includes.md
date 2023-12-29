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

    ![](source_code.png){: .normal }

3. By visiting these two links, we will finds that the required flag is separated in two parts:

    ![](css.png){: .normal }

    ![](js.png){: .normal }