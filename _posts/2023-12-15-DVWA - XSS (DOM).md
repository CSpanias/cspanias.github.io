---
title: DVWA - XSS (DOM)
date: 2023-12-15
categories: [CTF, Web Exploitation]
tags: [dvwa, xss, xss-dom, burp, ]
img_path: /assets/dvwa/xss_dom
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

## XSS (DOM)

**Cross-Site Scripting (XSS)** attacks are a type of injection problem, in which malicious scripts are injected into the otherwise benign and trusted web sites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application using input from a user in the output, without validating or encoding it.

**An attacker can use XSS to send a malicious script to an unsuspecting user**. The end user's browser has no way to know that the script should not be trusted, and will execute the JavaScript. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by your browser and used with that site. These scripts can even rewrite the content of the HTML page.

**DOM Based XSS** is a special case of reflected where the **JavaScript is hidden in the URL** and pulled out by JavaScript in the page while it is rendering rather than being embedded in the page when it is served. This can make it stealthier than other attacks and WAFs or other protections which are reading the page body do not see any malicious content.

**Objective**: Run your own JavaScript in another user's browser, use this to steal the cookie of a logged in user.

## Security: Low
> _Low level will not check the requested input, before including it to be used in the output text ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_low_source.php))._


## Security: Medium
> _The developer has tried to add a simple pattern matching to remove any references to `"<script"` to disable any JavaScript. Find a way to run JavaScript without using the script tags ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_medium_source.php))._


## Security: High
> _The developer is now white listing only the allowed languages, you must find a way to run your code without it going to the server ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_high_source.php))._


## Security: Impossible
> _The contents taken from the URL are encoded by default by most browsers which prevents any injected JavaScript from being executed ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_medium_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=X87Ubv-qDm4).