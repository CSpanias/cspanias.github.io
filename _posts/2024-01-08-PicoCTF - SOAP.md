---
title: PicoCTF - SOAP
date: 2024-01-08
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, soap, xml, xxe]
img_path: /assets/picoctf/web_exploitation/SOAP
published: true
---

![](room_banner.png){: width="70%"}

> **Description**: _The web project was rushed and no security assessment was done. Can you read the `/etc/passwd` file?_

1. The homepage looks like this: 

    ![](home.png){: .normal}

2. If we click on "*Details* some extra info about each institution is shown:

    ![](request_browser.png){: .normal}

    ![](request_burp.png){: .normal}

3. According to the challenge's tag, this solution is related to an [XXE vulnerability](https://portswigger.net/web-security/xxe):

    **XML external entity injection (XXE)** _is a web security vulnerability that allows an attacker to interfere with an application's processing of XML data. It often allows an attacker to view files on the application server filesystem, and to interact with any back-end or external systems that the application itself can access._

    PayloadAllThings repo has an XXE section, starting with how to [detect the vulnerability](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md#detect-the-vulnerability). Let's try that:

    ![](burp_payload.png){: .normal}

4. We have now confirmed that server is XXE vulnerable, so we can proceed on the repo's [exploiting XXE to retrieve files](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md#exploiting-xxe-to-retrieve-files) section:

    ![](flag.png){: .normal}