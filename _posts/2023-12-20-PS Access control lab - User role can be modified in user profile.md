---
title: PS Access control lab - User role can be modified in user profile
date: 2023-12-20
categories: [Training, PortSwigger]
tags: [portswigger, lab, access_control, burp]
img_path: /assets/portswigger/labs/access_control/
published: true
---

**Objective**: _This lab has an admin panel at `/admin`. It's only accessible to logged-in users with a `roleid` of `2`. Solve the lab by accessing the admin panel and using it to delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. When trying to access `/admin` with the user `wiener`:

    ![](lab1_error.png){: .normal}

2. If we try to update `wiener`'s email, intercept the request, and send it to the Repeater it looks like this:

    ![](lab1_email_update.png){: .normal}

    ![](lab1_email_update_request.png)

3. We can see the POST request includes the `email` parameter, but the response includes the `roleid` parameter, among others. Thus, we can intercept the request with Proxy, add the `roleid` parameter and set its value to `2`:

    ![](lab1_email_update_intercept.png){: .normal}

    ![](lab1_admin_panel.png)

4. Now that we have access to the admin panel, we can delete `carlos` and solve the lab:

    ![](lab1_carlos_delete.png){: .normal}

    ![](lab1_solved.png)