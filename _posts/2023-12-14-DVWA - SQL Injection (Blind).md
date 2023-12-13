---
title: DVWA - SQL Injection (Blind)
date: 2023-12-14
categories: [DVWA, SQL Injection]
tags: [dvwa, sqli, burp-suite, inspector, mariadb, hash, john, md5]
img_path: /assets/dvwa/sqli_blind
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

## SQL Injection (Blind)

When an attacker executes SQLi attacks, sometimes the server responds with error messages from the database server complaining that the SQL query's syntax is incorrect. **Blind SQLi is identical to normal SQLi except that when an attacker attempts to exploit an application, rather then getting a useful error message, they get a generic page specified by the developer instead**. This makes exploiting a potential SQLi attack more difficult but not impossible. An attacker can still steal data by asking a series of True and False questions through SQL statements, and monitoring how the web application response (valid entry retunred or 404 header set).

**"time based" injection** method is often used when there is no visible feedback in how the page different in its response (hence its a blind attack). This means the attacker will wait to see how long the page takes to response back. If it takes longer than normal, their query was successful.

**Objective**: Find the version of the SQL database software through a Blind SQLi attack.

## PHP required configurations

Before start working on this lab, ensure that the `display_errors` PHP configuration is `On`. If not, we won't be able to get any error messages back due to that and not because the developer's code! See how on the [SQLi post](https://cspanias.github.io/posts/DVWA-SQL-Injection/#php-required-configurations).

## Security: Low
> _The SQL query uses RAW input that is directly controlled by the attacker. All they need to-do is escape the query and then they are able to execute any SQL query they wish ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_low_source.php))._

## Security: Medium
> _The medium level uses a form of SQL injection protection, with the function of [`mysql_real_escape_string()`](https://www.php.net/manual/en/function.mysql-real-escape-string.php). However due to the SQL query not having quotes around the parameter, this will not fully protect the query from being altered. The text box has been replaced with a pre-defined dropdown list and uses POST to submit the form ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_medium_source.php))._

## Security: High
> _This is very similar to the low level, however this time the attacker is inputting the value in a different manner. The input values are being transferred to the vulnerable query via session variables using another page, rather than a direct GET request ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_high_source.php))._

## Security: Impossible
> _The queries are now parameterized queries (rather than being dynamic). This means the query has been defined by the developer, and has distinguish which sections are code, and the rest is data ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_impossible_source_code.php))._

## Resources

- [Cryptocat's video walkthrough](https://www.youtube.com/watch?v=uN8Tv1exPMk).