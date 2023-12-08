---
title: PicoCTF - Cookies
date: 2023-12-08
categories: [PicoCTF, Web Exploitation]
tags: [picoctf, web-exploitation, cookies, http-requests, burp-suite]
img_path: /assets/picoctf/web_exploitation/cookies
published: true
---

![](cookie_banner.png)

Visiting the link:

![](home.png)

Putting `snickerdoodle` as input results to:

![](snickerdoodle_cookie.png)

Intercepting the traffic with Burp and refreshing the page:

![](0_snickerdoodle.png)

We have a cookie called `name` set to value `0`. Sending requests with different cookie values results to different responses, including the flag:

![](1_chock.png)

![](2_oat.png)

![](18_flag.jpg)

![](28_mac.png)





