---
title: PortSwigger SSVs - Access control
date: 2023-12-19
categories: [Training, PortSwigger]
tags: [portswigger, server-side-vulnerabilities, access-control]
img_path: /assets/portswigger/server-side/access_control
published: true
---

## What is access control?

Access control is the application of constraints on who or what is authorized to perform actions or access resources. This is dependent on authentication (_the user is who they say they are_) and session management (_identifies which subsequent HTTP requests are being made by that same user_). Broken access control are common and often present a critical security vulnerability.

## Unprotected functionality (Vertical privilege escalation)

This happens when an app does not enforce any protection for sensitive functionality. 

For example, a website might host sensitive functionality at `https://domain.com/admin`. This might be accessible by any user and not only admins. In some cases, the admin URL might be disclosed in other locations, such as `https:://domain.com/robots.txt`, which can be brute-forced.

### Lab: Unprotected admin functionality

**Objective**: _This lab has an unprotected admin panel. Solve the lab by deleting the user `carlos`._

1. The lab is the same e-shop as before:

    ![](home.png)

2. We can check if a `robots.txt` file is present:

    ![](robots_txt.png)

3. We then visit the `/admininstrator-panel` directory and solve the lab by deleting the user `carlos`:

    ![](admin_panel.png)

    ![](lab_solved.png)

## Unprotected functionality - Continued

In some cases, sensitive functionality is concealed by obfuscating the URL, aka **security by obscurity**. Imagine an app that hosts admin functions at `https://insecure-website.com/administrator-panel-yb556`. This is not directly guessable by an attacker, but the app might still leak it to users. For instance, it might be disclosed in JavaScript that constructs the user interface based on the user's role:

```javascript
<script>
	var isAdmin = false;
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```

### Lab: Unprotected admin functionality with unpredictable URL

**Objective**: _This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application. Solve the lab by accessing the admin panel, and using it to delete the user carlos._

1. If we visit the page's source code, we will find an obfuscated URL:

    ![](lab2_source.png)

2. We can solve this lab, by visiting the `/admin-8893sq` directory and deleting the user `carlos`:

    ![](lab2_solved.png)

## Parameter-based access control methods

Some apps determine the user's access rights or role at login, and then store this info in a user-controllable location, such as a hidden field, cookie or preset query string parameter.

For example, an app can make access control decisions based on the submitted value, like `https://domain.com/login/home.jsp?admin=true` or `https://domain.com/login/home.jsp?role=1`. Since the user can modify these values this is highly insecure.

### Lab: User role controlled by request parameter

**Objective**:  _This lab has an admin panel at `/admin`, which identifies administrators using a forgeable cookie. Solve the lab by accessing the admin panel and using it to delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we try to access the `/admin` directory, we get an unauthorized access message:

    ![](lab3_admin.png)

2. First, we need to enable *Reponse Interception* under *Proxy settings* > *Response interception rules*:

    ![](lab3_proxy_settings.png)

3. Now, we can turn *Intercept* to *On* and login with the given credentials:

    ![](lab3_login_request.png)

4. If we *Forward* the request, we will notice an `Admin` cookie set to `false`. We need to change this to `true` and then *Forward* the request:

    ![](lab3_admin_cookie.png)

5. We will notice that the *Admin panel* option is now available on our browser:

    ![](lab3_admin_panel.png)

6. With our *Intercept* still enabled, we keep changing the `Admin` cookie to `true` on very request, until we manage to delete user `carlos` and solve tha lab:

    ![](lab3_delete.png)

    ![](lab3_solved.png)

## Horizontal privilege escalation

Let's assume that a user might access their account page using `https://domain//myaccount?id=123`. The user might be able to access another user's account by modifying the value of the `id` parameter.

> _This is an example of an **Insecure Direct Object Reference (IDOR)**: user-controller parameter values are used to access resources/functions directly._

In some apps, the exploitable parameter does not have a predictable value. For instance, an app might use Globally Unique IDs (GUIDs). This may prevent an attacker from predicting another user's identifier, but these values might be disclosed elsewhere in the app where users are referenced, such as user messages or reviews.

### Lab: User ID controlled by request parameter, with unpredictable user IDs

**Objective**:  _This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs. To solve the lab, find the GUID for `carlos`, then submit his API key as the solution. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we login with the acc `wiener`, we get an API key:

    ![](lab4_home.png)

    ![](lab4_home_burp.png)

2. If we check the first blog post, we can see that it's written by `carlos` and by examining the response we can find his GUID:

    ![](lab4_carlos_post.png)

    ![](lab4_carlos_guid.png)

3. Now that we know `carlos`'s GUID, we can re-login as `wiener`, intercept the request and replace the GUID to get his API key as a response:

    ![](lab4_login_burp.png)

    ![](lab4_carlos_api_key.png)

4. Then we must submit `carlos`'s API key as a solution to mark this lab as solved:

    ![](lab4_solved.png)

## Horizontal to vertical privilege escalation

An attacker aiming at horizontal privilege escalation might compromise a user with elevated privileges, thus, turn a horizontal privilege escaltion attempt into a vertical one.

### Lab: User ID controlled by request parameter with password disclosure

**Objective**:  _This lab has user account page that contains the current user's existing password, prefilled in a masked input. To solve the lab, retrieve the administrator's password, then use it to delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we log in with the account `wiener`, the GET request includes the parameter `id` which is set with the account name, i.e., `wiener`. On our browser there is an option for changing the accounts password which is already pre-filled with our current password:

    ![](lab5_password.png)

    ![](lab5_login_request.png)

2. We can change the `id` parameter's value to `administrator`, and *Forward* the request:

    ![](lab5_admin_intercept.png)

    ![](lab5_admin_login.png)

3. Now we can login as `administrator`, delete `carlos`, and solve the lab:

    ![](lab5_solved.png)



## Resources

- [Server-side vulnerabilities](https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice).
- Related practice: [DVWA LFI](https://cspanias.github.io/posts/DVWA-File-Inclusion/).