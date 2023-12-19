---
title: DVWA - Javascript
date: 2023-12-18
categories: [Training, DVWA]
tags: [dvwa, burp, javascript, js, firefox, debugger, console, inspector, burp, obfuscation, deobfuscation, sha256, hash, rot13, md5, encoding, decoding]
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

    ![](low_success_fail.png){: .normal }

2. We can find the token mentioned by inspecting the page:

    ![](low_token.png)

3. If we take a look at the source code, we see that there is a function called `generate_token()` which takes our input and encodes it with ROT13 and then hashes it using MD5:

    ![](low_source.png)

4. We can use [Cyberchef](https://gchq.github.io/CyberChef/) to perform the same process for the word `success`:

    ![](low_enc.png)

5. Now, we can change the token's value, pass `success` to the input box and click *Submit*:

    ![](low_submission.png)

    ![](low_pass.png){: .normal }

### Generate_token()

1. Another way we can solve this is by using the existing `generate_token()` function. We can begin by removing the `type`'s value `hidden` so we can see the token in the browser:

    ![](low_hidden.png)

2. Then we can write `success` in the input box, go to *Console*, and execute the `generate_token()` function. 

    ![](low_generate_token.png)

3. Once executed, it will generate the new token which we can then submit:

    ![](low_token_generated.png)

    ![](low_pass_2.png){: .normal }

### Debugger

1. We can also play around with the *Debugger* and find out what exactly is going on by inserting breakpoints on the function(s) of interest:

    ![](low_debugger_config.png)

    > By just clicking on the number of the code line, `88` in the above case, a breakpoint would be inserted.

2. Once the breakpoints are set and we click submit, with the value of `ChangeMe` in the input box, the code will run and stop on our breakpoint:

    ![](low_paused_on_bp.png)

3. We can then go to the *Console* tab and set the `phrase` variable to `success`:

    ![](console_phrase_success.png){: .normal }

4. Then, if we jump back to the *Debugger* and click the *Resume* button, we will notice that `phrase`'s value will change to `success`:

    ![](low_play_to_success.png)

5. If we click *Step in* until we get inside the `rot13` function and then *Step over*, we will get `success` encoded in ROT13:

    ![](low_step_in_rot13.png)

    ![](changed_inp_to_success.png)

6. If we repeat the above process, i.e., click *Step in* until we get inside the obfuscated function and then *Step over*, we will get the md5 hash value:

    ![](low_step_in_obf.png)

    ![](low_step_over_md5.png)

## Security: Medium
> _The JavaScript has been broken out into its own file and then minimized. You need to view the source for the included file and then work out what it is doing. Both Firefox and Chrome have a Pretty Print feature which attempts to reverse the compression and display code in a readable way ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/javascript/javascript_medium_source.php))._

1. We can take a look at the code via the *Debugger* tab:

    ![](medium_pretty_print.png)

2. We can also check the token's value via the *Inspector* tab:

    ![](medium_changeme_token.png)

3. It is kind of obvious what it is doing: adding as both prefix and suffix the `XX` string, and reversing the input string, `ChangeMe` to `eMegnahC`. So we can try that with `success`:

    ![](medium_pass.png)

4. Similarly with what we did before, we can set a breakpoint on *Debugger* and repeat the above process to see the changes in a more detailed way:

    ![](medium_breakpoint_1.png)

    ![](medium_phrase_success.png){: .normal }

    ![](medium_resume.png)

    ![](medium_breakpoint_2.png)

    ![](medium_breakpoint_3.png)

## Security: High
> _The JavaScript has been obfuscated by at least one engine. You are going to need to step through the code to work out what is useful, what is garbage and what is needed to complete the mission ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/javascript/javascript_high_source.php))._

1. If we check the code, we will notice that is obfuscated:

    ![](high_obf_code.png)

2. We can use a [Java deobfuscator](https://lelinhtinh.github.io/de4js/) to see what we are dealing with:

    ![](java_deobf.png)

3. Skimming through the code, the last few lines seem to be the important part:

    ![](high_code_end.png)

4. We can't use the *Debugger* yet, as the code is still obfuscated. What we can do is replacing the obfuscated code, `high.js`, with the deobfuscated code, `high_deobf.js`, using Burp:

    ![](high_js.png)

5. To do that, we first need to launch an HTTP server where `high_deobf.js` is located:

    ```shell
    $ ls
    high_deobf.js

    $ python3 -m http.server 8888
    Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
    ```

6. Once the HTTP server is up, we can create a *Match and Replace rule*:

    ![](proxy_settings_config.png)

7. When we refresh the page we will get a GET request on our HTTP server, and we will see that the file is now replaced:

    ```shell
    $ python3 -m http.server 8888
    Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
    127.0.0.1 - - [18/Dec/2023 20:04:50] "GET /high_deobf.js HTTP/1.1" 200 -
    ```

    ![](high_deobf.png)

8. Before we start working with the *Debugger* we can also set some addition settings on Burp:

    ![](proxy_settings_config2.png)

9. We can now work with the *Debugger* as before to examine how this works. We first set our breakpoints:

    ![](high_bp_1.png)

10. We submit the phrase `success`, *Step over* once, and check the value `document.getElementById("phrase").value` via *Console*. This is the hash of the existing token suffixed with `ZZ`:

    ![](token_value_1.png){: .normal }

11. If we *Step over* we will jump to `token_part_1()` function which uses the `document.getElementById("phrase").value`. If we *Step in* and then check its value will be set to nothing, so we need to set its value to `success`:

    ![](high_phrase_success.png){: .normal }

12. If we jump back to the *Debugger* and click *Step in* again we will notice that it was changed to `success`. If we continue *Stepping in* we will see that this function is reversing our string:

    ![](token_value_2.png)

13. After reversing, its jumps on `token_part_2()` function which prefixes `success` with `XX`:

    ![](token_value_3.png)

14. Our new token value is generated, and if we click *Resume*, remove our breakpoints, and submit the string `success`:

    ![](high_success.png){: .normal }

## Security: Impossible
> _You can never trust the user and have to assume that any code sent to the user can be manipulated or bypassed and so there is no impossible level._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=3IfHy97pog0).