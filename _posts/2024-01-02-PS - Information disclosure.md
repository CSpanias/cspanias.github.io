---
title: Information disclosure
date: 2024-01-02
categories: [PortSwigger, Information disclosure]
tags: [portswigger, information-disclosure]
img_path: /assets/portswigger/info_disclosure
published: true
image:
    path: ../portswigger_acad_logo.png
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

![](burp_scanner.png)

### Using Burp's engagement tools (Pro version only)

Burp provides several engagement tools that we can use to find interesting info in the target website. We can access them from the context menu: just right-click on any HTTP message, Burp Proxy entry, or item in the site map and go to *Engagement tools*. The following tools are particularly useful:
- **Search**: We can use this tool to look for any expression within the selected item. We can fine-tune the results using various advanced search options, such as regex search or negative search. This is useful for quickly finding occurrences (or absences) of specific keywords of interest.
- **Find comments**: We can use this tool to quickly extract any developer comments found in the selected item. It also provides tabs to instantly access the HTTP request/response cycle in which each comment was found.
- **Discover content**: We can use this tool to identify additional content and functionality that is not linked from the website's visible content. This can be useful for findining additional directories and files that won't necessary appear in the site map automatically.

![](burp_engagement_tools.jpg)

### Engineering informative responses

Verbose error messages can sometimes disclose interesting info while we go about our normal testing workflow. However, by studying the way error messages change according to our input, we can take this one step further. In some cases, we might be able to manipulate the website in order to extract arbitrary data via an error message.

One common method is to make the app logic attempt an invalid action on a specific item of data. For example, submitting an invalid parameter value might lead to a stack trace or debug response that contains interesting details. We can sometimes cause error messages to disclose the value of our desired data in the response.

## Common sources of information disclosure

### Files for web crawlers

Many websites provide files at `/robots.txt` and `/sitemap.xml` to help crawlers navigate their site. Among other things, these files often list specific directories that the crawlers should skip, for example, because they may contain sensitive info. As these files are not usually linked from within the website, they may not immediately appear in Burp's site map. However, it is worth trying to navigate to these directories manually to see if we can find anything of use.

### Directory listings

Web servers can be configured to automatically list the contents of directories that do not have an index page present. This can aid an attacker by enabling them to quickly identify the resources at a given path, and proceed directly to analyzing and attacking those resources. It particularly increases the exposure of sensitive files within the directory that are not intended to be accessible to users, such as temp files and crash dumps.

Directory listings themselves are not necessarily a security vulnerability. However, if a website also fails to implement proper access control, leaking the existence and location of sensitive resources in this way is clearly an issue.

### Developer comments

During development, in-line HTML comments are sometimes added to the markup. These are typically stripped before changes are deployed to the production environment. However, they can sometimes be forgotten, missed, or even left in deliberately because someone wasn't fully aware of the security implications. Although these comments are not visible on the rendered page, they can easily be access using Burp, or even the browser's built-in developer tools.

### Error messages

One of the most common causes of information disclosure is verbose error messages. Their content can reveal info about what **input or data type** is expected from a given parameter which can help us to narrow down our attack by identifying exploitable parameters or simply prevent us from wasting time trying to inject payloads that won't work.

In addition, error messages can provide **info about different technologies being used** by the website, which can lead in expanding our attack surface. We might also discover that the website is using some kind of **open-source framework**, so we can study the publicly available source code and construct our own exploits.

Differences between error messages can also reveal different app behavior that is occurring behind the scenes. This is a crucial aspect of many techniques, such as SQLi and username enumeration, among others.

### Lab: Information disclosure in error messages

> **Objective**: _This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework._

1. When we select an product, there is a `productId` parameter which has as a value an integer number:

    ![](lab1_home.png){ .normal width="70%}

2. If we change this value to something other than the integer that it expects, it will give us an error message that includes the web app framework's version:

    ![](lab1_version.png){ .normal width="70%}

    ![](lab1_solved.png)

### Debugging data

For debugging purposes, many websites generate custom error messages and logs that contain large amounts of info about the app's behavior. Debug messages can sometimes contain vital info for developing an attack, such as:
- Values for key session variables that can be manipulated via user input
- Hostnames and credentials for back-end components
- File and directory names on the server
- Keys used to encrypt data transmitted via the client

Debugging info may sometimes be logged in a separate file. If an attacker is able to gain access to this file, it can serve as a useful reference for understanding the app's runtime state. It can also provide several clues as to how they can supply crafted input to manipulate the app state and control the information received.

### Lab: Information disclosure on debug page

> **Objective**: _This lab contains a debug page that discloses sensitive information about the application. To solve the lab, obtain and submit the `SECRET_KEY` environment variable._

1. If we select any product from the homepage and visit its source code, we will find an HTML comment listing a directory used for Debug purposes:

    ![](lab2_source.png){: .normal}

2. Upon visiting this directory, we can search and find the `SECRET_KEY` value:

    ![](lab2_secret_key.png)

    ![](lab2_solved.png)

### User account pages

Inherently a user's profile usually contains sensitive info, such as the user's email address, phone number, API key, etc. Normally, users have only access to their own account page, but some websites contain **logic flaws** that potentially allow an attacker to leverage these pages in order to view other user's data. For example, consider a website that determines which user's account page to load based on a `user` parameter: `GET /user/personal-info?user=carlos`. Most websites will take steps to prevent an attacker from simply changing this parameter to access arbitrary users' account pages. 

However, sometimes the logic for loading individual items of data is not as robust. An attacker may not be able to load another user's account page entirely, but the logic for fetching and rendering the user's registered email address, for instance, might not check that the `user` parameter matches the user that is currently logged in. In this case, simply changing the `user` parameter would allow an attacker to display arbitrary users' email addresses on their own account page.

### Source code disclosure via backup files

Obtaining source code makes it much easier for an attacker to understand the app's behavior and construct high-severity attacks. Sensitive data is sometimes even hard-coded within it, such as API keys and credentials for accessing back-end components. If we can identify that a particular open-source technology is being used, this provides easy access to a limited amount of source code.

Occasionally, it is even possible to cause the website to expose its own source code. When mapping out a website, we might find that some source code files are referenced explicitly. Unfortunately, requesting them does not usually reveal the code itself. When a server handles files with a particular extension, such as `.php`, it will typically execute the code, rather than simply sending it to the client as text. 

However, in some situations, we can trick a website into returning the contents of the file instead. For example, text editors often generate temp backup files while the original file is being edited. These are usually indicated in some way, such as by appending a tilde (`~`) to the filename or adding a different file extension. Requesting a code file using a backup file extension can sometimes allow us to read the contents of the file in the response.

### Lab: Source code disclosure via backup files

> **Objective**: _This lab leaks its source code via backup files in a hidden directory. To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code._

1. This website includes a `/robots.txt` directory which contains a listing for a `/backup` directory:

    ![](lab3_robots.png)

2. The `/backup` directory contains a backup file (indicated by the `.bak` extension). This file has hardcoded the connection details needed for the PostgreSQL server which includes the password:

    ![](lab3_backup_dir.png)

    ![](lab3_pass.png)

    ![](lab3_solved.png)

### Information disclosure due to insecure configuration

Websites are sometimes vulnerable as a result of misconfigurations. This is especially common due to the widespread use of third-party technologies, whose vast array of configuration options are not necessarily well-understood by those implementing them.

In other cases, developers might forget to disable various debugging options in the production environment. For example, HTTP `TRACE` method is designed for diagnostic purposes. If enabled, the web server will respond to requests that use it by echoing in the response the exact request that was received. This may seem harmless, but occasionally leads to info disclosure, such as the name of internal authentication headers that may be appended to requests by reverse proxies.

### Lab: Authentication bypass via information disclosure

> **Objective**: _This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end. To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we try to access the `/admin` interface as the user `wiener`, we get a message saying that it is only accessble to local users:

    ![](lab4_admin_error.png)

    ![](lab4_admin_error_burp.png)

2. If we change the HTTP method from `GET` to `TRACE`, we can see at the end of the response that the `X-Custom-IP-Authorization` header, containing our IP address, was automatically appended to our request. This header is used to determine whether or not the request came from the `localhost` IP address. Since the `/admin` interface is only available to `localhost` we can change this header as follows:

    ![](lab4_match_and_replace.png)

3. When we do that, the admin panel wil be available and we can use it to delete the user `carlos`:

    ![](lab4_admin_panel.png)

    ![](lab4_solved.png)

### Version control history

Virtually all websites are developed using some form of version control system, such as Git. By default, a Git project stores all of its version control data in a folder called `.git`. Occasionally, websites expose this directory in the production environment. In this case, we might be able to access it by simply browsing to `/.git`.

While it is often impractical to manually browse the raw file structure and contents, there are various methods for the downloading the entire `.git` directory which may include logs containing committed changes and other interesting info. This might not give us access to the full source code, but comparing the diff will allow you to read small snippets of code and we might be lucky in finding sensitive data hard-coded within some changed lines.

> Practice: Try Hack Me's [Git Happens](https://cspanias.github.io/posts/THM-Git-Happens/) machine.

### Lab: Information disclosure in version control history

> **Objective**: _This lab discloses sensitive information via its version control history. To solve the lab, obtain the password for the `administrator` user then log in and delete the user `carlos`._

1. This website has a `/.git` directory:

    ![](lab5_git.png)

2. We can download the whole directory locally using [Gitools](https://github.com/internetwache/GitTools):

    ```shell
    # download .git directory
    $ /opt/GitTools/Dumper/gitdumper.sh https://0afa00ea047350a68206bf7b001100ce.web-security-academy.net/.git/ ~/portswigger/info_disclosure/
    ###########
    # GitDumper is part of https://github.com/internetwache/GitTools
    #
    # Developed and maintained by @gehaxelt from @internetwache
    #
    # Use at your own risk. Usage might be illegal in certain circumstances.
    # Only for educational purposes!
    ###########

    [*] Destination folder does not exist
    [+] Creating /home/kali/portswigger/info_disclosure//.git/
    [+] Downloaded: HEAD
    [-] Downloaded: objects/info/packs
    [+] Downloaded: description
    [+] Downloaded: config
    [+] Downloaded: COMMIT_EDITMSG
    [+] Downloaded: index
    [-] Downloaded: packed-refs
    [+] Downloaded: refs/heads/master
    [-] Downloaded: refs/remotes/origin/HEAD
    [-] Downloaded: refs/stash
    [+] Downloaded: logs/HEAD
    [+] Downloaded: logs/refs/heads/master
    [-] Downloaded: logs/refs/remotes/origin/HEAD
    [-] Downloaded: info/refs
    [+] Downloaded: info/exclude
    [-] Downloaded: /refs/wip/index/refs/heads/master
    [-] Downloaded: /refs/wip/wtree/refs/heads/master
    [+] Downloaded: objects/df/f527d734b5cfa13ef20f554309408fd16f68e6
    [-] Downloaded: objects/00/00000000000000000000000000000000000000
    [+] Downloaded: objects/0f/119caba173aa611b01fac27ce40dc34f7edfca
    [+] Downloaded: objects/21/54555944002791a4d27412bf6e9a6f29e942fa
    [+] Downloaded: objects/ab/21e339e998069d4f315136e882e16f590c8ed8
    [+] Downloaded: objects/21/d23f13ce6c704b81857379a3e247e3436f4b26
    [+] Downloaded: objects/89/44e3b9853691431dc58d5f4978d3940cea4af2
    [+] Downloaded: objects/90/55fb5b8127f7e82802db7ee9f66e61644fb3ef
    ```

    > We can also use `wget -r https://0afa00ea047350a68206bf7b001100ce.web-security-academy.net/.git/`.

3. We can now interact with it as it was our own:

    ```shell
    $ cd ~/portswigger/info_disclosure/.git
    $ ls
    COMMIT_EDITMSG  config  description  HEAD  index  info  logs  objects  refs
    ```

    For example, we can check the logs using `git log`:

    ```shell
    $ git log
    commit dff527d734b5cfa13ef20f554309408fd16f68e6 (HEAD -> master)
    Author: Carlos Montoya <carlos@evil-user.net>
    Date:   Tue Jun 23 14:05:07 2020 +0000

        Remove admin password from config

    commit 0f119caba173aa611b01fac27ce40dc34f7edfca
    Author: Carlos Montoya <carlos@evil-user.net>
    Date:   Mon Jun 22 16:23:42 2020 +0000

        Add skeleton admin panel
    ```

    We are interestingly mostly on the commits included in the log. We can achieve this by [chaining commands](https://www.diskinternals.com/linux-reader/bash-chain-commands/#:~:text=Chaining%20usually%20means%20binding%20things,by%20simply%20introducing%20an%20operator.) using the pipe operator (`|`):

    ```shell
    $ git log | grep commig | cut -d " " -f2 | xargs git show > commits
    
    $ cat commits
    commit dff527d734b5cfa13ef20f554309408fd16f68e6
    Author: Carlos Montoya <carlos@evil-user.net>
    Date:   Tue Jun 23 14:05:07 2020 +0000

        Remove admin password from config

    diff --git a/admin.conf b/admin.conf
    index 9055fb5..21d23f1 100644
    --- a/admin.conf
    +++ b/admin.conf
    @@ -1 +1 @@
    -ADMIN_PASSWORD=y2c7pbp5mfhxql197pjn
    +ADMIN_PASSWORD=env('ADMIN_PASSWORD')
    ```

    > A detailed analysis of the command can be found [here](https://cspanias.github.io/posts/THM-Git-Happens/#33-git-repositories-and-gittools).

4. Now that we got the password of the user `administrator`, we can log in and delete `carlos`:

    ![](lab5_solved.png)

## How to prevent information disclosure vulnerabilities

There are some general best practices that we can follow to minimize the risk of this kind of vulnerability:
- Make sure that everyone involved in producing the website is fully aware of what information is considered sensitive. Sometimes seemingly harmless information can be much more useful to an attacker than people realize. Highlighting these dangers can help make sure that sensitive information is handled more securely in general by your organization.
- Audit any code for potential information disclosure as part of your QA or build processes. It should be relatively easy to automate some of the associated tasks, such as stripping developer comments.
- Use generic error messages as much as possible. Don't provide attackers with clues about application behavior unnecessarily.
- Double-check that any debugging or diagnostic features are disabled in the production environment.
- Make sure you fully understand the configuration settings, and security implications, of any third-party technology that you implement. Take the time to investigate and disable any features and settings that you don't actually need.


## Resources

- [Infromation disclosure](https://portswigger.net/web-security/information-disclosure).