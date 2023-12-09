---
title: DVWA - File Inclusion
date: 2023-12-09
categories: [DVWA, File Inclusion]
tags: [dvwa, file-inclusion, burp-suite]
img_path: /assets/dvwa/file_inclusion
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

Some web applications *allow the user to specify input that is used directly into file streams* or *allows the user to upload files to the server*. At a later time the web application accesses the user supplied input in the web applications context. By doing this, the web application is allowing the potential for malicious file execution. 

If the file chosen to be included is local on the target machine, it is called **Local File Inclusion (LFI)**. But files may also be included on other machines, which then the attack is a **Remote File Inclusion (RFI)**. When RFI is not an option, using another vulnerability with LFI, such as file upload and directory traversal, can often achieve the same effect.

**Objective**: Read all five famous quotes from `../hackable/flags/fi.php` using only the file inclusion.

## Security: Low

> _This allows for direct input into one of many PHP functions that will include the content when executing. Depending on the web service configuration will depend if RFI is a possibility._

## Security: Medium

> _The developer has read up on some of the issues with LFI/RFI, and decided to filter the input. However, the patterns that are used, isn't enough._

## Security: High

> _The developer has had enough. They decided to only allow certain files to be used. However as there are multiple files with the same basename, they use a wildcard to include them all._

## Security: Impossible

> _The developer calls it quits and hardcodes only the allowed pages, with there exact filenames. By doing this, it removes all avenues of attack._