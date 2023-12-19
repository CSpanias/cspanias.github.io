---
title: DVWA - Open HTTP Redirect
date: 2023-12-19
categories: [CTF, Web Exploitation]
tags: [dvwa, burp, open-http-redirect, http, http-codes]
img_path: /assets/dvwa/open_http_redirect
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

## Open HTTP Redirect

 OWASP define this as:

_Unvalidated redirects and forwards are possible **when a web application accepts untrusted input that could cause the web application to redirect the request to a URL contained within untrusted input**. By modifying untrusted URL input to a malicious site, an attacker may successfully launch a phishing scam and steal user credentials._

As suggested above, a common use for this is to create a URL which initially goes to the real site but then redirects the victim off to a site controlled by the attacker. This site could be a clone of the target's login page to steal credentials, a request for credit card details to pay for a service on the target site, or simply a spam page full of advertising.

**Objective**: Abuse the redirect page to move the user off the DVWA site or onto a different page on the site than expected.

## Security: Low
> _The redirect page has no limitations, you can redirect to anywhere you want ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/open_http_redirect/open_http_redirect_low_source.php))._

1. The home page includes two links, and upon clicking the first one the address bar changes like this:

    ![](low_home.png)

    ![](low_quote_1.png)

2. If we interecept the traffic with Burp, we will notice a `redirect` parameter:

    ![](low_request.png)

    > [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

3. We can send this request to the Repeater, and try to manipulate the `redirect` parameter:

    ![](low_redirection.png)

4. If we now try this on our browser, we should be redirected to the target website:

    ![](low_browser_redirection.png)

    ![](low_browser_redirection_1.png)

## Security: Medium
> _The code prevents you from using absolute URLs to take the user off the site, so you can either use relative URLs to take them to other pages on the same site or a [Protocol-relative URL](https://en.wikipedia.org/wiki/Wikipedia:Protocol-relative_URL) ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/open_http_redirect/open_http_redirect_medium_source.php))._

1. When we try the same redirection method as before, we will find that this time does not work:

    ![](medium_500_burp.png)

2. That's easily bypassed by removing the `https://` and turning the absolute to a relative URL:

    ![](medium_302_burp.png)

## Security: High
> _The redirect page tries to lock you to only redirect to the info.php page, but does this by checking that the URL contains "info.php" ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/open_http_redirect/open_http_redirect_high_source.php))._

1. This time we are only allowed to redirect to the info page:

    ![](high_500.png)

2. All the server is looking for is `info.php` within the URL. So we can add that after using a

    ![](high_302.png)

    ![](high_302_browser.png)

## Security: Impossible
> _Rather than accepting a page or URL as the redirect target, the system uses ID values to tell the redirect page where to redirect to. This ties the system down to only redirect to pages it knows about and so there is no way for an attacker to modify things to go to a page of their choosing ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/open_http_redirect/open_http_redirect_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=I5jko9mLNO4&list=PLHUKi1UlEgOJLPSFZaFKMoexpM6qhOb4Q&index=17).
- Snyk's [Open redirect](https://learn.snyk.io/lesson/open-redirect/).
- Mozilla's [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).