---
title: PicoCTF - Logon
date: 2023-12-28
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, logon, burp, parameters]
img_path: /assets/picoctf/web_exploitation/logon
published: true
---

    ![](room_banner.png){: width="70%" .normal}

1. The website lands us on a login form:

    ![](home.png){: width="60%" .normal}

2. If we try to log in as `Joe` we get an error message:

    ![](joe_failed_login.png)

2. When we put random credentials as a test, e.g. `test:test`, we are able to log in:

    ![](test_login.png){: width="80%" .normal}

3. Let's start Burp Suite and examine what's happening behind the scenes:

    ![](login_process_burp.png)

4. It seems that when we logged in with `test:test`, a `POST` request was send to `/problem/44573/login` directory which included a cookie called `admin` which was set to `False`. Next, there was a `GET` request which also included the `admin` cookie:

    ![](get_flag_request.png)

5. If we modify the latter request and then send it, we can get the flag in the response:

    ![](modified_request.png)

    ![](flag.png)

    ![](flag_browser.png){: width="80%" .normal}



