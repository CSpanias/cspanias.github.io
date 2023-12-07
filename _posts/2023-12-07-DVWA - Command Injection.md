---
title: DVWA - Command Injection
date: 2023-12-07
categories: [DVWA, Command Injection]
tags: [dvwa, command-injection]
img_path: /assets/dvwa/command_injection
published: true
---

## Information

- [How to install dvwa on Kali](https://www.kali.org/tools/dvwa/).
- [Official GitHub repository](https://github.com/digininja/DVWA).

> The DVWA server itself contains instructions about almost everything.

_**Damn Vulnerable Web Application (DVWA)** is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and to aid both students & teachers to learn about web application security in a controlled class room environment._

_The aim of DVWA is to practice some of the most common web vulnerabilities, with various levels of difficultly, with a simple straightforward interface._

![](dvwa_home.png)

The DVWA server has **4 different security levels** which can be set as seen below:

![](security_levels.png)

## Security: Low

> [Command injection](https://owasp.org/www-community/attacks/Command_Injection) is an attack in which the goal is execution of arbitrary commands on the host operating system via a vulnerable application.

How it works:
- When we want to execute more than one command we use concatenating characters, such as `;`, `&&`, and `||`, aka *command chaining*.
- The commands are executed from left to right.

| Character | Description |
|:-:|:-:|
| ; | executes all commands regardless of whether the previous ones failed or not
| && | executes the second command only if the preceding command succeeds |
| \|\| | executes the second command only if the precedent command fails |

```shell
# command chaining examples
ls
test  test1

cat test; cat test1
This is the content of test.
This is the content of test1.

cat test && cat test1
This is the content of test.
This is the content of test1.

cat test2 && cat test1
cat: test2: No such file or directory

cat test2 || cat test1
cat: test2: No such file or directory
This is the content of test1.
```

## Security: Low

![](low_ping_command.png)

What the above web application does is simply executing the `ping` command.

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

![](low_id.png)

![](low_os-release.png)

![](low_lsb_release.png)

On the source code below we can see that:
1. The script defines the `$target` variable with whatever we pass it as input.
2. The passes our input directly to the `shell_exec()` function which adds our input to a predefined `ping` or `ping -c 4` command.

> When we input `. | id`, `ping -c 4 . | id` is executed.

![](low_source_code.jpg)




