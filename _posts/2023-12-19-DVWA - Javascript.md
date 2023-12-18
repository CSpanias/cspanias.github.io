---
title: DVWA - Javascript
date: 2023-12-19
categories: [CTF, Web Exploitation]
tags: [dvwa, burp, javascript, js]
img_path: /assets/dvwa/javascript
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

## Javascript

The attacks in this section are designed to help you learn about **how JavaScript is used in the browser and how it can be manipulated**. The attacks could be carried out by just analysing network traffic, but that isn't the point and it would also probably be a lot harder.

**Objective**: Simply submit the phrase "success" to win the level. Obviously, it isn't quite that easy, each level implements different protection mechanisms, the JavaScript included in the pages has to be analysed and then manipulated to bypass the protections.

## Security: Low
> _All the JavaScript is included in the page. Read the source and work out what function is being used to generate the token required to match with the phrase and then call the function manually ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/javascript/javascript_low_source.php))._

### CyberChef

1. When we input `success` in the box, we get an `Invalid token.` message back:

    ![](low_success_fail.png)

2. We can find the token mentioned by inspecting the page:

    ![](low_token.png)

3. If we take a look at the source code, we see that there is a function called `generate_token()` which takes our input and encodes it with ROT13 and then hashes it using MD5:

    ![](low_source.png)

4. So we use [Cyberchef](https://gchq.github.io/CyberChef/) to perform the same process for the word `success`:

    ![](low_enc.png)

5. Now, we can change the token's value and pass `success` to the input box:

    ![](low_submission.png)

    ![](low_pass.png)

### Generate_token()

1. Another way we can solve this is by using the existing `generate_token()` function. We can begin by removing the `type`'s value `hidden` so we can see the token in the browser:

    ![](low_hidden.png)

2. Then we can write `success` in the input box, go to *Console*, and execute the `generate_token()` function. 

    ![](low_generate_token.png)

3. Once executed, it will generate the token we need which we can then submit and pass this level:

    ![](low_token_generated.png)

    ![](low_pass_2.png)

### Debugger

1. We can also play around with the *Debugger* and find out what exactly is going on by inserting breakpoints on the function of interest:

    ![](low_debugger_config.png)

> By just clicking on the number of the code, `88` in the above case, a breakpoint would be inserted.

2. When we click submit with the value of `ChangeMe` the code will run and stop on our breakpoint:

    ![](low_paused_on_bp.png)

3. We can then go to the *Console* tab, set the `phrase` variable to `success`:

    ![](console_phrase_success.png)

4. Then if we jump back to the *Debugger* and click the *Resume* button, we will notice that `phrase`'s value will change to `success`:

    ![](low_play_to_success.png)

5. Then if we click *Step in* until we get inside the `rot13` function and then *Step over*, we will get `success` encoded in ROT13:

    ![](low_step_in_rot13.png)

    ![](changed_inp_to_success.png)

6. If we repeat the above process, i.e., click *Step in* until we get inside the obfuscated function and then *Step over*, we will get the md5 hash value:

    ![](low_step_in_obf.png)

    ![](low_step_over_md5.png)

## Security: Medium
> _The JavaScript has been broken out into its own file and then minimized. You need to view the source for the included file and then work out what it is doing. Both Firefox and Chrome have a Pretty Print feature which attempts to reverse the compression and display code in a readable way ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/javascript/javascript_medium_source.php))._



## Security: High
> _The JavaScript has been obfuscated by at least one engine. You are going to need to step through the code to work out what is useful, what is garbage and what is needed to complete the mission ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/javascript/javascript_high_source.php))._



## Security: Impossible
> _You can never trust the user and have to assume that any code sent to the user can be manipulated or bypassed and so there is no impossible level._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=3IfHy97pog0).