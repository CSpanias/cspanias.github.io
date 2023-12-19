---
title: DVWA - Authorisation Bypass
date: 2023-12-19
categories: [CTF, Web Exploitation]
tags: [dvwa, auth-bypass]
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

If the `Authorisation Bypass` tab is not appearing on the vulnerabilities menu, just go to appropriate directory and it should come up:

![](auth_bypass_dir.png)

## Authorisation Bypass

When developers have to build authorisation matrices into complex systems it is easy for them to miss adding the right checks in every place, especially those which are not directly accessible through a browser, for example API calls.

As a tester, you need to be looking at every call a system makes and then testing it using every level of user to ensure that the checks are being carried out correctly. This can often be a long and boring task, especially with a large matrix with lots of different user types, but it is critical that the testing is carried out as one missed check could lead to an attacker gaining access to confidential data or functions.

**Objective**: Your goal is to test this user management system at all four security levels to identify any areas where authorisation checks have been missed. The system is only designed to be accessed by the admin user, so have a look at all the calls made while logged in as the admin, and then try to reproduce them while logged in as different user. If you need a second user, you can use `gordonb / abc123`.

## Security: Low
> _Non-admin users do not have the 'Authorisation Bypass' menu option ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_low_source.php))._



## Security: Medium
> _The developer has locked down access to the HTML for the page, but have a look how the page is populated when logged in as the admin ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_medium_source.php))._



## Security: High
> _Both the HTML page and the API to retrieve data have been locked down, but what about updating data? You have to make sure you test every call to the site ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_high_source.php))._



## Security: Impossible
> _Hopefully on this level all the functions correctly check authorisation before allowing access to the data. There may however be some non-authorisation related issues on the page, so do not write it off as fully secure ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/auth_bypass/auth_bypass_impossible_source.php))._

## Resources

