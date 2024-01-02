---
title: Information disclosure
date: 2024-01-01
categories: [PortSwigger, Information disclosure]
tags: [portswigger, information-disclosure]
img_path: /assets/portswigger/info_disclosure
published: true
---

## What is information disclosure?

**Information disclosure**, aka **information leakage**, is when a website unintentionally reveals sensitive info to its users, such as data about other users, business data, technical details about the website and its infrastructure, etc. The latter can be the starting point for exposing an additional attack surface leading to high-severity attacks.

Sometimes, sensitive info might be carelessly leaked to users who are simply browsing the website. However, an attacker needs to elicit the info disclosure by interacting with the webiste in unexpected or malicious ways. Some basic examples of info disclosure are:
- Revealing the names of hidden directories, their structure, and their contents via a `robots.txt` file or directory listing
- Providing access to source code files via temporary backups
- Explicitly mentioning database table or column names in error messages
- Unnecessarily exposing highly sensitive information, such as credit card details
- Hard-coding API keys, IP addresses, database credentials, and so on in the source code
- Hinting at the existence or absence of resources, usernames, and so on via subtle differences in application behavior

## How do information disclosure vulnerabilities arise?

Info disclosure vulnerabilities can broadly be categorized as follows:
- **Failure to remove internal content from public content**. For example, developer comments in markup are sometimes visible to users in the production environment.
- **Insecure configuration of the website and related technologies**. For example, failing to disable debugging and diagnostic features can sometimes provide attackers with useful tools to help them obtain sensitive information. Default configurations can also leave websites vulnerable, for example, by displaying overly verbose error messages.
- **Flawed design and behavior of the application**. For example, if a website returns distinct responses when different error states occur, this can also allow attackers to enumerate sensitive data, such as valid user credentials.

## What is the impact of information disclosure vulnerabilities?

Info disclosure vulnerabilities can have both a direct and indirect impact depending on the purpose of the website and what info an attacker is able to obtain. In some cases, the act of disclosing sensitive info alone can have a high direct impact on the affected parties. On the other hand, leaking technical info may have little to no direct impact, but it may be used to construct any number of exploits.

During testing, the **disclosure of technical info** is often only of interest if we are able to demonstrate how an attacker could do something harmful with it. Therefore, our main focus should be on the impact and exploitability of the leaked info, not just the presence of info disclosure as a standalone issue.

## How to test for information disclosure vulnerabilities

It is important not to develop tunnel vision during testing, i.e., avoid focusing too narrowly on a particular vulnerability. We will often find sensitive data while testing for something else, and we should be able to recognize interesting info whenever and wherever we do come across it.

### Fuzzing

If we identify interesting parameters, we can try submitting unexpected data types and specially crafted fuzz strings to see what effect this has. We need to pay close attention: although responses sometimes may explicitly discole interesting info, they can also hint at the app's behavior more subtly, for example, the time taken to process the request. Even if the content of an error message does not disclose anything, sometimes the fact that one error case was encountered instead of another one is useful info in itself.

We can automate much of this process using tools like Intruder:
- **Add payload positions to parameters and use pre-built wordlists** of fuzz strings to test a high volume of different inputs in quick succession.
- **Easily identify differences in responses** by comparing HTTP status codes, response times, lengths, etc.
- Use **grep matching rules** to quickly identify occurences of keywords, such as `error`, `invalid`, `SELECT`, etc.
- Apply **grep extraction rules** to extract and compare the content of interesting items within responses.

We can also use the *Logger++* extension which allows us to define advanced filters for highlighting interesting entries.

### Using Burp Scanner (Pro version only)

**Burp Scanner** provides live scanning features for auditing items while we browse, or we can schedule automated scans to crawl and audit the target site on our behalf. Both approaches will automatically flag many info disclosure vulnerabilities for us. For example, it will alert us if it finds sensitive info, such as private keys, email addresses, credit card numbers, etc. It will also identify any backup files, directory listings, and so on.

![](https://portswigger.net/cms/images/25/ac/d4b31263a79c-article-screen_shot_2018-09-13_at_13.13.54.png)

### Using Burp's engagement tools (Pro version only)

Burp provides several engagement tools that we can use to find interesting info in the target website. We can access them from the context menu: just right-click on any HTTP message, Burp Proxy entry, or item in the site map and go to *Engagement tools*. The following tools are particularly useful:
- **Search**: We can use this tool to look for any expression within the selected item. We can fine-tune the results using various advanced search options, such as regex search or negative search. This is useful for quickly finding occurrences (or absences) of specific keywords of interest.
- **Find comments**: We can use this tool to quickly extract any developer comments found in the selected item. It also provides tabs to instantly access the HTTP request/response cycle in which each comment was found.
- **Discover content**: We can use this tool to identify additional content and functionality that is not linked from the website's visible content. This can be useful for findining additional directories and files that won't necessary appear in the site map automatically.

![](https://portswigger.net/cms/images/13/e2/e233-article-burp-suite-pro-discover-content.jpg)

### Engineering informative responses

Verbose error messages can sometimes disclose interesting info while we go about our normal testing workflow. However, by studying the way error messages change according to our input, we can take this one step further. In some cases, we might be able to manipulate the website in order to extract arbitrary data via an error message.

One common method is to make the app logic attempt an invalid action on a specific item of data. For example, submitting an invalid parameter value might lead to a stack trace or debug response that contains interesting details. We can sometimes cause error messages to disclose the value of our desired data in the response.


## How to prevent information disclosure vulnerabilities

There are some general best practices that we can follow to minimize the risk of this kind of vulnerability:
- Make sure that everyone involved in producing the website is fully aware of what information is considered sensitive. Sometimes seemingly harmless information can be much more useful to an attacker than people realize. Highlighting these dangers can help make sure that sensitive information is handled more securely in general by your organization.
- Audit any code for potential information disclosure as part of your QA or build processes. It should be relatively easy to automate some of the associated tasks, such as stripping developer comments.
- Use generic error messages as much as possible. Don't provide attackers with clues about application behavior unnecessarily.
- Double-check that any debugging or diagnostic features are disabled in the production environment.
- Make sure you fully understand the configuration settings, and security implications, of any third-party technology that you implement. Take the time to investigate and disable any features and settings that you don't actually need.


## Resources

- [Path Traversal](https://portswigger.net/web-security/file-path-traversal).
- [Path Traversal (YouTube version)](https://www.youtube.com/watch?v=NQwUDLMOrHo&t=11s).