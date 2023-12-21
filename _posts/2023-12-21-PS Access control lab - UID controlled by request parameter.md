---
title: PS Access control lab - UID controlled by request parameter
date: 2023-12-21
categories: [Training, PortSwigger]
tags: [portswigger, lab, access_control, burp]
img_path: /assets/portswigger/labs/access_control/
published: true
---

**Objective**: _This lab has a horizontal privilege escalation vulnerability on the user account page. To solve the lab, obtain the API key for the user `carlos` and submit it as the solution. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we login with the account `wiener`, we are given his API key:

    ![](lab2_api_key_wiener.png)

    ![](lab2_api_key_wiener_burp.png)

2. If we change the `id` parameter to `carlos` we will be able to get his API key and submit our solution:

    ![](lab2_api_key_carlos.png)

    ![](lab2_api_key_carlos_burp.png)

    ![](lab2_solved.png)