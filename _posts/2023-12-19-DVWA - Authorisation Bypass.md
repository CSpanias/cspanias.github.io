---
title: DVWA - Authorisation Bypass
date: 2023-12-19
categories: [CTF, Web Exploitation]
tags: [dvwa, auth-bypass, idor, authentication, authorization]
img_path: /assets/dvwa/auth_bypass
published: true
---

## Information

- [How to install dvwa on Kali](https://www.kali.org/tools/dvwa/).
- [Official GitHub repository](https://github.com/digininja/DVWA).

> The DVWA server itself contains instructions about almost everything.

_**Damn Vulnerable Web Application (DVWA)** is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and to aid both students & teachers to learn about web application security in a controlled class room environment._

_The aim of DVWA is to practice some of the most common web vulnerabilities, with various levels of difficultly, with a simple straightforward interface._

![](dvwa_home.png){: width='70%' }

The DVWA server has **4 different security levels** which can be set as seen below:

![](security_levels.png){: width='70%' }

- **Low**: This security level is completely vulnerable and has no security measures at all. It's use is to be as an example of how web application vulnerabilities manifest through bad coding practices and to serve as a platform to teach or learn basic exploitation techniques.
- **Medium**: This setting is mainly to give an example to the user of bad security practices, where the developer has tried but failed to secure an application. It also acts as a challenge to users to refine their exploitation techniques.
- **High**: This option is an extension to the medium difficulty, with a mixture of harder or alternative bad practices to attempt to secure the code. The vulnerability may not allow the same extent of the exploitation, similar in various Capture The Flags (CTFs) competitions.
- **Impossible**: This level should be secure against all vulnerabilities. It is used to compare the vulnerable source code to the secure source code.

> The `Authorisation Bypass` tab is only visible with the `admin` account on the vulnerabilities menu. If we cannot see it, that means we are not logged in as `admin`, so we must logout and login again.

## Authorisation Bypass

When developers have to build authorisation matrices into complex systems it is easy for them to miss adding the right checks in every place, especially those which are not directly accessible through a browser, for example API calls.

As a tester, you need to be looking at every call a system makes and then testing it using every level of user to ensure that the checks are being carried out correctly. This can often be a long and boring task, especially with a large matrix with lots of different user types, but it is critical that the testing is carried out as one missed check could lead to an attacker gaining access to confidential data or functions.

**Objective**: Your goal is to test this user management system at all four security levels to identify any areas where authorisation checks have been missed. The system is only designed to be accessed by the admin user, so have a look at all the calls made while logged in as the admin, and then try to reproduce them while logged in as different user. If you need a second user, you can use `gordonb / abc123`.

## Security: Low
> _Non-admin users do not have the 'Authorisation Bypass' menu option ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_low_source.php))._

1. Our goal is to log in as a non-admin user and explore authorization vulnerabilities. Just to clear on what we are trying to achieve, let's clarify the difference between [Authentication vs Authorization](https://portswigger.net/web-security/authentication#what-is-the-difference-between-authentication-and-authorization):

    > _**Authentication** is the process of verifying that a user is who they claim to be. **Authorization** involves verifying whether a user is allowed to do something._

2. So let's now login as a non-admin user, in this case `gordonb`:

    ![](gordon_login.png)

3. One way of trying to access this directory is through the use of an [Insecure Direct Object Reference (IDOR)](https://portswigger.net/web-security/access-control/idor) vulnerability:

    > _**Insecure direct object references (IDOR)** are a type of access control vulnerability that arises when an application uses user-supplied input to access objects directly._

    As already mentioned, the `/vulnerabilities/authbypass/` directory is intended to be accessed by the `admin` account only. But if `gordonb` tries to access this directory directly, it seems that it can: 

    ![](low_dir.png)

## Security: Medium
> _The developer has locked down access to the HTML for the page, but have a look how the page is populated when logged in as the admin ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_medium_source.php))._

1. If we try to exploit the same IDOR vulnerability, we will find out that we cannot:

    ![](med_unauth.png)

2. The `/vulnerabilities/authbypass/` directory is populated with some user data which originate from `/vulnerabilities/authbypass/get_user_data.php`:

    ![](med_admin_data.png)

    Let's check if `gordonb` can access the data file instead of the directory, which would be another IDOR vulnerability:

    ![](med_gordon_access.png)

## Security: High
> _Both the HTML page and the API to retrieve data have been locked down, but what about updating data? You have to make sure you test every call to the site ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_high_source.php))._

1. If we login with the `admin` acc and try to update our data, for instance, change `Bob` to `Robert`, and capture that request with Burp, this is how it looks like:

    ![](high_update_robert.png)

    ![](high_admin_update_request.png)

2. We can interecept the traffic from `gordonb`'s session (by refreshing the DVWA page) via Proxy, choose to respond to it, copy and paste the above request (but changing the cookie to `gordonb` session's values), modify the data and forward the POST request. Under normal circumnstances this should not work, but it does:

    ![](high_gordon_intercept.png)

    ![](high_gordon_mod_request.png)

    ![](high_gordon_mod_request1.png)

3. If we now login with the `admin` acc, we can see that the data has indeed been modified:

    ![](high_data_changed.png)

## Security: Impossible
> _Hopefully on this level all the functions correctly check authorisation before allowing access to the data. There may however be some non-authorisation related issues on the page, so do not write it off as fully secure ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=Qcgu34eWQa4&list=PLHUKi1UlEgOJLPSFZaFKMoexpM6qhOb4Q&index=17&t=68s).
- PortSwigger's [Insecure direct object references (IDOR)](https://portswigger.net/web-security/access-control/idor).