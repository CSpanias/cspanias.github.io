---
title: DVWA - Command Injection
date: 2023-12-07
categories: [DVWA, Command Injection]
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

## Security: Low

> _[Command Injection](https://owasp.org/www-community/attacks/Command_Injection) is an attack in which the goal is execution of arbitrary commands on the host operating system via a vulnerable application._

How it works:
- When we want to execute more than one command we use concatenating characters to chain commands, such as `;`, `&&`, and `||`.
- The commands are executed from left to right.

> The `&&` and `||` are [Boolean operators](https://www.scaler.com/topics/linux-operators/).

|||
|:-:|:-:|
| Character | Description |
| ; | executes all commands regardless of whether the previous ones failed or not
| && | executes the second command only if the preceding command succeeds |
| \|\| | executes the second command only if the precedent command fails |

![](command_chaining.png)

## Security: Low

![](low_ping_command.png){: width='75%'}

What the above web application does is simply executing the `ping` command with the given input:

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

If we try the first two commands, i.e. `1.1.1.1 && id` and `1.1.1.1; cat /etc/os-release`, they won't work. However the third command, `. || lsb_release -a`, will work just fine!

![](low_lsb-release.jpg){: width='75%'}

Looking at the source code below, we can see that a blacklist was added which essentially removes the `&&` and `;` operators, but not the `||` operator! 

![](medium_source_code.jpg){: width='75%'}

## Security: High

Now none of our three commands work! As we can see below, the blacklist was extended included Boolean and Bitwise operators, among others.  

![](high_source_code.jpg)

However, if we watch carefully the pipe operator on the third item on the blacklist, a space is included: `| `. Thus, if we use `|` without a space our payload should work:

![](high_id.jpg){: width='75%'}