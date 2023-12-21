---
title: PS Authentication lab - Password reset broken logic
date: 2023-12-21
categories: [Training, PortSwigger]
tags: [portswigger, lab, authentication, burp]
img_path: /assets/portswigger/labs/authentication/
published: true
---

**Objective**: _This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page._
- _Your credentials: `wiener:peter`._
- _Victim's username: `carlos`._

1. The site has a *Forgot password?* functionality, so let's use that for the account `wiener` to see how it works:

    ![](lab1_forgot_password.png)

    ![](lab1_forgot_user.png)

2. When we reset `wiener`'s password, it prompts up to check our email. So let's login and do that:

    ![](lab1_wiener.png)

    ![](lab1_reset_email.png)

    ![](lab1_forgot_new_pass.png)

3. If we examine the request when we submit a new password, we will see that it includes a `username` parameter which we might be able to manipulate:

    ![](lab1_forgot_new_pass_burp.png)

4. We will do the process all over again, intercept the request when submitting our new password, and change the `username` parameter value to `carlos`:

    ![](lab1_forgot_new_pass_carlos_burp.png)

5. Then we will login with `carlos` account and his new password:

    ![](lab1_solved.png)

