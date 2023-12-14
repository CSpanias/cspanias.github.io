---
title: DVWA - Weak Sessions IDs
date: 2023-12-14
categories: [DVWA, Weak Sessions IDs]
tags: [dvwa, session-ids, burp, burp-repeater, burp-sequencer, burp-intruder, hash, md5, john, cookies]
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

Knowledge of a session ID is often the only thing required to access a site as a specific user after they have logged in, if that session ID is able to be calculated or easily guessed, then an attacker will have an easy way to gain access to user accounts without having to brute force passwords or find other vulnerabilities, such as Cross-Site Scripting.

**Objective**: This module uses four different ways to set the `dvwaSession` cookie value, the objective of each level is to work out how the ID is generated and then infer the IDs of other system users.

## Security: Low
> _The cookie value should be very obviously predictable ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/weak_sessions_ids/weak_sessions_ids_low_source_code.php))._

1. If we click *Generate* we can see the `dvwaSession` cookie's value via *Inspect* > *Storage* > *Cookies*:

    ![](low_cookie1.png)

2. Each time we click *Generate* this value increments by 1, so after clicking 5 times:

    ![](low_cookie6.png)

3. Our objective is to just find out how `dvwaSession` is generated, so in this case, it is just increments by the value of 1.

## Security: Medium
> _The value looks a little more random than on low but if you collect a few you should start to see a pattern ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/weak_sessions_ids/weak_sessions_ids_medium_source_code.php))._

1. If we click *Generate* now the cookie looks more complicated:

    ![](medium_cookie1.png)

2.  If we click a second time:

    ![](medium_cookie2.png)

3. So the first cookie has the value of `1702554076` and the second one the value of `1702554193`; only the last 4 digits changed. If we click a third time similar changes occur:

    ![](medium_cookie3.png)

4. The value now has set to `1702554366`. So we can see that the first 6 digits are the same, and the last 4 are incremented in some way. This 10 digit sequence represents the [current epoch unix timestamp](https://www.unixtimestamp.com/):

    > _The unix time stamp is **a way to track time as a running total of seconds**. This count starts at the Unix Epoch on January 1st, 1970 at UTC. Therefore, **the unix time stamp is merely the number of seconds between a particular date and the Unix Epoch**. It should also be pointed out (thanks to the comments from visitors to this site) that this point in time technically does not change no matter where you are located on the globe. This is very useful to computer systems for tracking and sorting dated information in dynamic and distributed applications both online and client side._

5. On this level, the cookie is taking the value of the current epoch unix timestamp.

## Security: High
> _First work out what format the value is in and then try to work out what is being used as the input to generate the values. Extra flags are also being added to the cookie, this does not affect the challenge but highlights extra protections that can be added to protect the cookies ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/weak_sessions_ids/weak_sessions_ids_high_source_code.php))._

1. Let's start by generating 2 cookies in a row and see how they look using Burp this time:

    ![](high_cookie1.png)

    ![](high_cookie2.png)

2. Another, and more efficient, way to this is to send the request to the Burp's **Sequencer**, configure it to generate a series of cookies, and then save its ouput which looks like this:

> Check how to do this [here](https://braincoke.fr/write-up/dvwa/dvwa-weak-session-i-ds/).

    ![](subl_cookies.png)

3. So these strings look like **MD5 hashes**. If we generate 5 cookies in a row and then try to crack them with `john` we get this result:

    ```shell
    # generate five cookies in a row
    $ cat cookie_hashes
    94bb077f18daa6620efa5cf6e6f178d2
    10ff0b5e85e5b85cc3095d431d8c08b4
    9f96f36b7aae3b1ff847c26ac94c604e
    4ffbd5c8221d7c147f8363ccdc9a2a37
    8396b14c5dff55d13eea57487bf8ed26 

    # crack the hashes with john
    $ john --format=Raw-MD5 cookie_hashes
    Using default input encoding: UTF-8
    Loaded 5 password hashes with no different salts (Raw-MD5 [MD5 512/512 AVX512BW 16x3])
    Warning: no OpenMP support for this hash type, consider --fork=16
    Proceeding with single, rules:Single
    Press 'q' or Ctrl-C to abort, almost any other key for status
    Almost done: Processing the remaining buffered candidate passwords, if any.
    Proceeding with wordlist:/usr/share/john/password.lst
    Proceeding with incremental:ASCII
    4981             (?)
    4980             (?)
    4977             (?)
    4979             (?)
    4978             (?)
    5g 0:00:00:01 DONE 3/3 (2023-12-14 13:14) 3.816g/s 24213Kp/s 24213Kc/s 121069KC/s 46oi..4970
    Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
    Session completed.
    ```

4. So this time the cookie seems to be generated using an MD5 hash of the plaintext session ID. We can see an example of how this can be used for an attack using Burp's **Intruder**. We send the request used to generate the request to Intruder:

    ![](send_to_intruder.png)

5. Then we select *Numbers* at the *Payload type*, we choose just a small range from *1* to *10*, and configure our payload processing with *Hash* and *MD5*:

    ![](intruder_config1.png)

    ![](intruder_config2.png)

6. Now that our payload is configured, we need to indicate where in the request it should be placed via the *Positions* tab. We copy and paste a random MD5 hashed cookie from before as the value of the `dvwaSession`, then select the hash, and finally click *Add §*:

    ![](intruder_config3.png)

7. Now when we click *Start Attack*, Intruder will automatically hash the values 1 to 10, hash them use them MD5, and send them:

    ![](intruder_attack.png)

## Security: Impossible
> _The cookie value should not be predictable at this level but feel free to try. As well as the extra flags, the cookie is being tied to the domain and the path of the challenge. ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/weak_sessions_ids/weak_sessions_ids_impossible_source_code.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=xzKEXAdlxPU).
- Braincoke's [DVWA - Weak Session IDs](https://braincoke.fr/write-up/dvwa/dvwa-weak-session-i-ds/).