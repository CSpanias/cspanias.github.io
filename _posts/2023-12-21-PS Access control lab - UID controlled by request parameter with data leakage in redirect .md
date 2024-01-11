---
title: Access control - UID controlled by request parameter with data leakage in redirect
date: 2023-12-21
categories: [PortSwigger, Lab]
tags: [portswigger, lab, access_control, burp]
img_path: /assets/portswigger/labs/access_control/
published: true
image:
    path: ../../portswigger_acad_logo.png
---

> **Objective**: _This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response. To solve the lab, obtain the API key for the user `carlos` and submit it as the solution. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we login with `wiener` a POST request is sent, and then we will notice a GET request which includes the `id` parameter:

    ![](lab3_wiener_login_burp.png)

    ![](lab3_wiener_login_response_burp.png)

2. If we changes `id`'s value to `carlos` we will be redirected (status code: `302`) to the login page, but the redirection will include `carlos`'s info:

    ![](lab3_carlos_login_response_burp.png)

    ![](lab3_carlos_redirect_burp.png)

    ![](lab3_solved.png)