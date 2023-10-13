---
title: Kiba CTF Write Up
date: 2023-10-13
categories: [CTF Write Up, THM]
tags: [kibana, gtfobins, prototypepollution, rce, capabilities]
img_path: /assets/kiba/
mermaid: true
---

![kiba_banner](kiba_banner.png)

## 1 Summary

[![](https://mermaid.ink/img/pako:eNpdkLFOAzEMhl8lMstVaqXOGZBoDxhoRVXYCIN7cWjUXHxKfEJV1RdhYebteARyvQXwYuv_7U_yf4KGLYEGF_i92WMStdqaqErdvDz4HUZ8VbOZ2iQWlmNHasMh9OI5FvlacV1V2-WtMiZ-f358TSZaa8c8Eor52xutgbbEDnc-ePGUB_v--e5x4WO-IBdVYpZ_VyPQxL-9CZhzTU4N3CyJD6Sv3HwOU2gpteht-ew07BqQPbVkQJfRYjoYMPFc9rAXfjrGBrSknqbQdxaFao9vCVvQDkMuKlkvnNZjVJfEzj_4vmhX?type=png)](https://mermaid.live/edit#pako:eNpdkLFOAzEMhl8lMstVaqXOGZBoDxhoRVXYCIN7cWjUXHxKfEJV1RdhYebteARyvQXwYuv_7U_yf4KGLYEGF_i92WMStdqaqErdvDz4HUZ8VbOZ2iQWlmNHasMh9OI5FvlacV1V2-WtMiZ-f358TSZaa8c8Eor52xutgbbEDnc-ePGUB_v--e5x4WO-IBdVYpZ_VyPQxL-9CZhzTU4N3CyJD6Sv3HwOU2gpteht-ew07BqQPbVkQJfRYjoYMPFc9rAXfjrGBrSknqbQdxaFao9vCVvQDkMuKlkvnNZjVJfEzj_4vmhX)

## 2 Background Information

The [Kiba](https://tryhackme.com/room/kiba) room was the first room from the Starter series that did not require the use of tools such as **nmap**, **nikto**, **gobuster**, etc. in order to complete it. It did require a lot of reading for me though, as everything was new, and I mean that literally, E-V-E-R-Y-T-H-I-N-G! 

So let's dive right in, and start learning through the excellent room's questions 👏. 

### 2.1 Kibana software

Kiba is short for **[Kibana](https://www.tutorialspoint.com/kibana/index.htm)**, a browser visualization tool, mainly used for analyzing large volumes of logs in the form of graphs. 

Usually it is combined with **Elasticsearch** and **Logstash**, and the three of them combined are known as the **ELK stack**. Logstash collects the data from various sources, pushes them to Elasticsearch, which in turn acts as a database for Kibana which represents the data as visualizations.

![elk_stack](https://www.tutorialspoint.com/kibana/images/elk_stack.jpg)

## 3 CTF Process

### 3.1 Prototype-based Pollution to RCE

The first question asks us about a vulnerability specific to programming languages with **prototyped-based inheritance**. Let's Google about it:

![prototype_pollution](q1-prototype-based-inheritance.png){: width="60%" height="60%"}

Based on the following excellent [PortSwigger's article](https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications):

>*__Prototype__ __Pollution__ is a type of vulnerability that allows attackers to exploit the rules of the programming language. By __prototype-based__, we mean that when new objects are created, they carry over the properties and methods of the protorype object, which contains basic functionalities.*
>
>*__Object-based__ __inheritance__ gives flexibility and efficiency for programmers, but it also introduces vulnerabilities. By modifying just one object, someone can make application-wide changes to all objects, hence the name __prototype__ __pollution__.*

On the aforementioned article, there is a simple JavaScript example, demonstrating how we can achieve **cross-site scripting (XSS)** using this concept, which we can try on [Playcode](https://playcode.io/javascript) and get a better feel for it:

![js-example](pp1.png){: width="40%" height="40%"}
![js-example2](pp2.png){: width="60%" height="60%"}

A bit later in the article, there is a mention to another [article](https://portswigger.net/daily-swig/elk-stack-exploit-for-kibana-remote-code-execution-flaw-released-on-github) from PortSwigger, which explains how to use prototype pollution on Kibana to gain **Remote Code Execution (RCE)**, and also gives us the CVE number of this vulnerability, the answer for the third question 🥂 !

According to this, there are two ways of doing it:
1. Directly from Kibana's dashboard, as explained [here](https://research.securitum.com/prototype-pollution-rce-kibana-cve-2019-7609/) from the Securitum researcher Michał Bentkowski.
2. By executing a read-made python exploit script, as explained [here](https://www.tenable.com/blog/cve-2019-7609-exploit-script-available-for-kibana-remote-code-execution-vulnerability). 

The vulnerability, as [officially explained](https://discuss.elastic.co/t/elastic-stack-6-6-1-and-5-6-15-security-update/169077) by Elastic, seems simple enough:

>*Kibana versions before 5.6.15 and 6.6.1 contain an arbitrary code execution flaw in the Timelion visualizer. An attacker with access to the Timelion application could send a request that will attempt to execute javascript code. This could possibly lead to an attacker executing arbitrary commands with permissions of the Kibana process on the host system.*

By reading the article, we can also discover in which port Kibana listens:

![kibana_port](port.png){: width="70%" height="70%"}

Upon visiting the service on the browser, we can see Kibana's dashboard 🍾!

![kibana_dashboard](kibana_dashboard.png){: width="70%" height="70%"}

By exploring a bit more, we can find its version under the **Management** tab (the answer of the second question 🍻):

![kibana_version](kibana_version.jpg){: width="70%" height="70%"}

After trying the code used in the article, as well as trying almost every reverse shell mentioned on [HighOn.Coffee's](https://highon.coffee/blog/reverse-shell-cheat-sheet/#php-reverse-shell) blog, the connection kept failing instantly: 

![rce_failed](rce_fail.png)

As a result, we can go with the second approach! We can:
1. Clone the [GitHub repo](https://github.com/LandGrey/CVE-2019-7609/)
2. Execute the python2 script
3. Open a listener on our machine

Soon enough we get a reverse shell, and find our first 🚩!

![rce_success](rce_success.jpg)

### 3.2 Capabilities

The next question asks us about **Capabilities**, and if we visit the web server it says: "_Welcome, 'linux capabilities' is very interesting_". 

![homepage_capabilities](homepage_capabilities.png){: width="60%" height="60%"}

So, let's find out what they are! From [Linux manual page](https://man7.org/linux/man-pages/man7/capabilities.7.html):

>For the purpose of performing permission checks, traditional UNIX implementations distinguish two categories of processes:
1. _privileged_ processes (whose effective user ID is 0, referred to as superuser or root) 
2. _unprivileged_ processes (whose effective UID is nonzero)
>
>Privileged processes bypass all kernel permission checks, while unprivileged processes are subject to full permission checking based on the process's credentials (usually: effective UID, effective GID, and supplementary group list).
>
>Starting with Linux 2.2, **Linux divides the privileges traditionally associated with superuser into distinct units, known as capabilities, which can be independently enabled and disabled. Capabilities are a per-thread attribute**.

In brief, capabilities provide granular control of the root's permissions. By reading [this](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities#binaries-capabilities) HackTricks article, we can find out that binaries can also have capabilities as well as that we can use the `getcap` command to search for them.

By searching recursively (answer to the sixth question 👍), we can see that there is a hidden directory named `/.hackmeplease` which contains the **python3 binary**! 

![binary_cap_search](binary_cap_search.png)

Visiting [GTFOBins](https://gtfobins.github.io/#python), and following the guidance in the [Capabilities section](https://gtfobins.github.io/gtfobins/python/#capabilities), we can get **root access** and find our **root flag** 🚩!

![root_flag.jpg](root_flag.jpg)