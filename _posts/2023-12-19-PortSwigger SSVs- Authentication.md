---
title: PortSwigger SSVs - Authentication
date: 2023-12-19
categories: [Training, PortSwigger]
tags: [portswigger, server-side-vulnerabilities, authentication, brute-force, burp-intruder]
img_path: /assets/portswigger/server-side/authentication
published: true
---

## Authentication vulnerabilities

**Authentication vulnerabilities** can allow attackers to gain access to sensitive data and functionality as well as expand their attack surface.

As a reminder, **authentication** is the process of verifying that a user is who they claim to be, while **authorization** involves verifying whether a user is allowed to do something. For example, an authentication mechanism will determine if someone who is trying to access a website with the username `Maria` is the same person who owns the account. Once `Maria` is authenticated, her permissions determine what they are authorized to do.

## Brute-force attacks

This kind of attack happens when an attacker uses a system of trial and error to guess valid user credentials (usually in an automated way). Websites that relay on password-based login as their sole authentication mechanism can be vulnerable to such attacks. 

## Username enumeration

**Username enumeration** is when an attacker is able to observe changes in the website's behavior in order to identify whether a given username is valid. While attempting to brute-force a log in page, we should pay attention to any differences in:
- **Status codes**: The returned HTTP status code is likely to be the same for the majority of guesses since most of them will be wrong. Responses with different status codes can indicate that the username exists. It is best practice for websites to always return the same status code regardless of the outcome, but this is not always the case.
- **Error messages**: Sometimes the returned error message is different depending on whether both the username and the password are incorrect or only the password was incorrect.
- **Response times**: If most of the (incorrect) requests were handled with a similar response time, any deviation could suggest that the username exist. For example, a website might only check whether the password is correct if the username is valid: this extra step might cause an increase in the response time. This might be subtle, but an attacker can make this delay more obvious by entering a excessively long password.

### Lab: Username enumeration via different responses

**Objective**:  _This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:_
- [_Candidate usernames_](https://raw.githubusercontent.com/CSpanias/cspanias.github.io/main/assets/portswigger/server-side/authentication/auth_lab_usernames.txt)
- [_Candidate passwords_](https://raw.githubusercontent.com/CSpanias/cspanias.github.io/main/assets/portswigger/server-side/authentication/auth_lab_passwords.txt)

_To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page._

1. We can try to login using random credentials, i.e., `test:test`, *intercept* the request with *Burp Proxy* and sent it to *Intruder*:

    ![](lab1_invalid_username.png)

    ![](lab1_send_to_intruder.png)

2. We will start with username enumeration. From the *Positions* tab on *Intruder*, we select *Sniper* as our attack type, then we highlight the value of the `username` parameter and click the `Add §` button, and finally we leave a random password as the value of the `password` parameter:

    ![](lab1_username_payload_positions.png)

3. Next, on the *Payloads* tab, we set the given username list as the *Payload set*, either via uploading a text file (*Load ...*) or by a direct copy and *Paste*:

    ![](lab1_payload_list_1.png)

4. Now we are ready to click the *Start attack* button and wait. Once the attack is complete, we will notice just one username with a different length than the others: `atlanta`:

    ![](lab1_username_found.png)

5. We will continue our attack by brute-forcing the password. First, on the *Positions* tab, we set the value of `username` to `atlanta` and add section signs to the value of the `password`'s parameter. Then, we move to the *Payloads* tab and set the given password list:

    ![](lab1_password_payload_positions.png)

    ![](lab1_password_payload.png)

6. We are ready again to click *Start attack*. From the results, only one password value stands out, `monitor`:

    ![](lab1_password_found.png)

7. We can now use our obtained credentials and solve the lab:

    ![](lab1_solved.png)


## Resources

- [Server-side vulnerabilities](https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice).
- Related practice: [DVWA Authorization Bypass](https://cspanias.github.io/posts/DVWA-Authorisation-Bypass/).