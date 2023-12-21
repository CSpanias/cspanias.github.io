---
title: PS Access control lab - Insecure Direct Object References
date: 2023-12-21
categories: [Training, PortSwigger]
tags: [portswigger, lab, access_control, burp, idor]
img_path: /assets/portswigger/labs/access_control/
published: true
---

> **Objective**: _This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs. Solve the lab by finding the password for the user `carlos`, and logging into their account._

1. Upon logging in we will notice a *Live chat* functionality on the top right corner. If we submit a random message and click *View transcript* our conversation, named `2.txt`, will be downloaded:

    ![](lab4_live_chat.png)

    ![](lab4_transcript.png)

    ![](lab4_transcript_burp.png)

2. Since our log is `2.txt` it is only logical that `1.txt` will exist:

    ![](lab4_transcript_carlos_burp.png)

    ![](lab4_solved.png)