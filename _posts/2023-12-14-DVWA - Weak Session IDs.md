---
title: DVWA - Weak Sessions IDs
date: 2023-12-14
categories: [DVWA, Weak Sessions IDs]
tags: [dvwa, session-ids]
img_path: /assets/dvwa/weak_session_ids
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

## Weak Session IDs



**Objective**: 


## Security: Low
> _ ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli/sqli_low_source_code.php))._



## Security: Medium
> _ ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli/sqli_medium_source_code.php))._



## Security: High
> _ ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli/sqli_high_source_code.php))._


## Security: Impossible
> _ ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli/sqli_impossible_source_code.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=xzKEXAdlxPU).