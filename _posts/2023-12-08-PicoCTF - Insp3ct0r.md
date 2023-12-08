---
title: PicoCTF - Insp3ct0r
date: 2023-12-08
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, inspector, html, css, javascript]
img_path: /assets/picoctf/web_exploitation/insp3ct0r
published: true
---

![](insp3ct0r_banner.png){: width='60%' .normal}

Visiting the site:

![](home_what.png){: width='60%' .normal}

![](home_how.png){: width='60%' .normal}

Since the room is called Insp3ct0r, let's use the Inspector tool to inspect the page's HTML code:

![](html_1_3.png)

The comment mentions that the flag is split in three parts, and since the creator of the website used three technologies to make the website (HTML, CSS, JS), we can also use the same tool to view the contents of the CSS and JS files:

![](css_2_3.png)

![](js_3_3.png)

