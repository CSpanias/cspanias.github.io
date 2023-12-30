---
title: PicoCTF - Search source
date: 2023-12-30
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, search-source, html, css, microsoft-edge]
img_path: /assets/picoctf/web_exploitation/search_source
published: true
---

> **Description**: _The developer of this website mistakenly left an important artifact in the website source, can you find it? The website is [here](http://saturn.picoctf.net:65086/)._

> **Hint**: _How could you mirror the website on your local machine so you could use more powerful tools for searching?_

![](room_banner.png){: width="70%" .normal}

1. The website lands us on an interesting page:

    ![](home.png)

2. The tile of the challenge, *Search source*, points on viewing the page's source code:

    ![](source.png)

3. After searching all JavaScript and many CSS files, we can find the flag at the `style.css` file:

    ![](flag.png)

4. A quicker way to do this, using Microsoft Edge, is by searching all files via the *Inspect* functionality:

    ![](inspector_search_sources.png)

    ![](inspector_search_sources_1.png)

