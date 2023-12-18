---
title: DVWA - CSP Bypass
date: 2023-12-18
categories: [CTF, Web Exploitation]
tags: [dvwa, csp, csp-bypass]
img_path: /assets/dvwa/csp_bypass
published: true
---

> This task has an active issue: [CSP Bypass can't be solved with Hastebin anymore (once again) #539](https://github.com/digininja/DVWA/issues/539)
{: .prompt-warning}

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

## Content Security Policy (CSP) Bypass

CSP is used to **define where scripts and other resources can be loaded or executed from**. This module will walk you through ways to bypass the policy based on common mistakes made by developers. None of the vulnerabilities are actual vulnerabilities in CSP, they are vulnerabilities in the way it has been implemented.

**Objective**: Bypass Content Security Policy (CSP) and execute JavaScript in the page.

## Security: Low
> _Examine the policy to find all the sources that can be used to host external script files ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_low_source.php))._

1. If we take a look at the source code, we will find a whitelist of sources that we can use to achieve our objective:

    ```php
    $headerCSP = "Content-Security-Policy: script-src 'self' https://pastebin.com hastebin.com www.toptal.com example.com code.jquery.com https://ssl.google-analytics.com ;"; // allows js from self, pastebin.com, hastebin.com, jquery and google analytics.

    header($headerCSP);
    
    # These might work if you can't create your own for some reason
    # https://pastebin.com/raw/R570EE00
    # https://www.toptal.com/developers/hastebin/raw/cezaruzek
    ```

## Security: Medium
> _The CSP policy tries to use a nonce to prevent inline scripts from being added by attackers ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_medium_source.php))._


## Security: High
> _The page makes a JSONP call to source/jsonp.php passing the name of the function to callback to, you need to modify the jsonp.php script to change the callback function ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_high_source.php))._


## Security: Impossible
> _This level is an update of the high level where the JSONP call has its callback function hardcoded and the CSP policy is locked down to only allow external scripts ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=ERksJHl0DC0).
- [Content Security Policy Reference](https://content-security-policy.com/).
- Mozilla's [CSP for the web we have](https://blog.mozilla.org/security/2014/10/04/csp-for-the-web-we-have/).
- PortSwigger's [Content Security Policy](https://portswigger.net/web-security/cross-site-scripting/content-security-policy).