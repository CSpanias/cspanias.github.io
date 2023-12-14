---
title: DVWA - Command Injection
date: 2023-12-07
categories: [CTF, Web Exploitation]
tags: [dvwa, command-injection, boolean-operators, bitwise-operators, command-chaining]
img_path: /assets/dvwa/command_injection
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

## Command Injection

The purpose of the **command injection** attack is to inject and execute commands specified by the attacker in the vulnerable application. In situation like this, the application, which executes unwanted system commands, is like a pseudo system shell, and the attacker may use it as any authorized system user. However, commands are executed with the same privileges and environment as the web service has.

Command injection attacks are possible in most cases because of lack of correct input data validation, which can be manipulated by the attacker (forms, cookies, HTTP headers etc.).

The syntax and commands may differ between the Operating Systems (OS), such as Linux and Windows, depending on their desired actions. This attack may also be called "Remote Command Execution (RCE)".

How it works:
- When we want to execute more than one command we use concatenating characters to chain commands, such as `;`, `&&`, and `||`.
- The commands are executed from left to right.

> `&&` and `||` are [Boolean operators](https://www.scaler.com/topics/linux-operators/).

|||
|:-:|:-:|
| Character | Description |
| ; | executes all commands regardless of whether the previous ones failed or not
| && | executes the second command only if the preceding command succeeds |
| \|\| | executes the second command only if the precedent command fails |

![](command_chaining.png)

> Source [video walkthrough](https://www.youtube.com/watch?v=WiqRvlN_UIU).

## Security: Low

> _This allows for direct input into one of many PHP functions that will execute commands on the OS. It is possible to escape out of the designed command and executed unintentional actions. This can be done by adding on to the request, "once the command has executed successfully, run this command"._

What this web application does is simply executing the `ping` command with the given input:

![](low_ping_command.png){: width='75%'}

```shell
# executing the same command via the terminal
ping 1.1.1.1 -c 4
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=56 time=18.9 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=56 time=18.1 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=56 time=16.7 ms
64 bytes from 1.1.1.1: icmp_seq=4 ttl=56 time=16.1 ms

--- 1.1.1.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 16.141/17.477/18.886/1.087 ms
```

So we can try some command chaining, such as:

![](low_and_id.jpg){: width='75%'}

![](low_os-release.jpg){: width='75%'}

![](low_lsb-release.jpg){: width='75%'}

On the source code below we can see that:
1. The script defines the `$target` variable with whatever we pass it as input.
2. The passes our input directly to the `shell_exec()` function which adds our input to a predefined `ping` or `ping -c 4` command.

![](low_source_code.jpg){: width='75%'}

> When we give `. | id` as input , `ping -c 4 . | id` is executed.

## Security: Medium

> _The developer has read up on some of the issues with command injection, and placed in various pattern patching to filter the input. However, this isn't enough. Various other system syntaxes can be used to break out of the desired command._

If we try the first two commands, i.e. `1.1.1.1 && id` and `1.1.1.1; cat /etc/os-release`, they won't work. However the third command, `. || lsb_release -a`, will work just fine!

![](low_lsb-release.jpg){: width='75%'}

Looking at the source code below, we can see that a blacklist was added which essentially removes the `&&` and `;` operators, but not the `||` operator! 

![](medium_source_code.jpg){: width='75%'}

## Security: High

> _In the high level, the developer goes back to the drawing board and puts in even more pattern to match. But even this isn't enough. The developer has either made a slight typo with the filters and believes a certain PHP command will save them from this mistake._

Now none of our three commands work! As we can see below, the blacklist was extended included Boolean and Bitwise operators, among others.  

![](high_source_code.jpg)

However, if we watch carefully the pipe operator on the third item on the blacklist, a space is included: `| `. Thus, if we use `|` without a space our payload should work:

![](high_id.jpg){: width='75%'}

## Security: Impossible

> _In the impossible level, the challenge has been re-written, only to allow a very stricted input. If this doesn't match and doesn't produce a certain result, it will not be allowed to execute. Rather than "black listing" filtering (allowing any input and removing unwanted), this uses "white listing" (only allow certain values)._