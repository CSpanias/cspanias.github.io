---
title: PicoCTF - Scavenger Hunt
date: 2023-12-14
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, html, css, js, dirsearch, burp, burp-repeater, burp-target, dir-busting, apache]
img_path: /assets/picoctf/web_exploitation/scavenger_hunt
published: true
---

![](room_banner.png){: width='80%'}

1. Visiting the site:

    ![](home_what.png){: width='70%' .normal}

    ![](home_how.png){: width='70%' .normal}

2. This looks (almost) identical to the [Insp3ct0r](https://cspanias.github.io/posts/PicoCTF-Insp3ct0r/) challenge. Let's see if by viewing the page's HTML, CSS, and JS code would be enough to get the flag. We will be using Burp Suite this time, so let's start by viewing the HTML:

    ![](html_first_part.png)

3. We got the first part of it: `picoCTF{t`. By switching to the *Target* tab and sending the `mycss.css` and `myjs.js` requests to the *Repeater* we can check the CSS and JS code as well:

    ![](target_css_js.png)

    ![](css_second_part.png)

    ![](js_indexing.png)

4. We managed to get the second part of the flag: `h4ts_4_l0`, thus, we have `picoCTF{th4ts_4_l0`. The question asks us about Google indexing which points us to search for the robots file:

    ![](robots_third_part.png)

5. So we now have: `picoCTF{th4ts_4_l0t_0f_pl4c` and we are asked about the next flag! It lets us know that it is an apache server and has the *Access* with capital *A*, which points towards a common apache directory: `/.htaccess`:

    ![](htaccess_fourth_part.png)

6. This time the flag is gonna be a long one: `picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k`. The last hint talks about storing a lot of information, which indicates to some kind of a database-related directory. We can can perform **dir-busting** to see if that can help:

    ```shell
    $ dirsearch -u http://mercury.picoctf.net:39698/
    /usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
    from pkg_resources import DistributionNotFound, VersionConflict

    _|. _ _  _  _  _ _|_    v0.4.3
    (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

    Output File: /home/kali/reports/http_mercury.picoctf.net_39698/__23-12-14_17-18-34.txt

    Target: http://mercury.picoctf.net:39698/

    [17:18:34] Starting:
    [17:18:39] 403 -    9B  - /.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd
    [17:18:42] 200 -   62B  - /.DS_Store
    [17:18:45] 200 -   95B  - /.htaccess
    [17:18:45] 200 -   95B  - /.htaccess/
    [17:20:33] 200 -  124B  - /robots.txt

    Task Completed
    ```

    ![](ds_store_fifth_part.png)

7. Our complete flag is: `picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_fa04427c}`:

    ![](room_pwned.png)