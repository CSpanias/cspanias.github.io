---
title: PicoCTF - Who are you?
date: 2023-12-29
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, who-are-you]
img_path: /assets/picoctf/web_exploitation/who_are_you
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The website lands us on an interesting page:

    ![](home.png){: width="60%" .normal}

    ![](home_burp.png)

2. Since it mentions `PicoBrowser` we can add that to the `User-Agent` HTTP header:

    ![](add_picobrowser_burp.png)

    ![](add_picobrowser.png)

3.  Now the message directs us to the request's origin, so let's add the `Referer` HTTP header and set its value to the same original as the `Host`'s header:

    ![](referer_header_burp.png)

    ![](referer_header.png)

4. Based on the message, we can now add the `Date` HTTP header:

    ![](date_header_burp.png)

    ![](date_header.png)

5. Next, let's add the `DNT` (Do-Not-Track) HTTP header:

    ![](dnt_header_burp.png)

    ![](dnt_header.png)

6. Now, we have to find a relevant header that identifies the origin of the IP address, that is, `X-Forwarded-For`, combined with a Swedish IP address:

    ![](swedish_ips.png)

    ![](xForwardedFor_burp.png)

    ![](xForwardedFor.png)

7. Let's also add the `Content-Language` HTTP header:

    ![](accept_language_burp.png)

    ![](accept_language.png)