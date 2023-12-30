---
title: PicoCTF - Search source
date: 2023-12-30
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, search-source, html, css, microsoft-edge]
img_path: /assets/picoctf/web_exploitation/search_source
published: true
---

![](room_banner.png){: width="70%"}

> **Description**: _The developer of this website mistakenly left an important artifact in the website source, can you find it?_

> **Hint**: _How could you mirror the website on your local machine so you could use more powerful tools for searching?_

1. The website lands us on an interesting page:

    ![](home.png)

2. The tile of the challenge, *Search source*, points on viewing the page's source code:

    ![](source.png){: .normal}

3. After searching all JavaScript and many CSS files, we can find the flag at the `style.css` file:

    ![](flag.png)

## Microsfot Edge alternative (faster)

1. A quicker way to do this, using Microsoft Edge, is by searching all files via the *Inspect* functionality:

    ![](inspector_search_sources.png)

    ![](inspector_search_sources_1.png)

## Website mirroring alternative (local)

1. We can mirror the entire website locally by using the `wget -m` option:

    ```shell
    # mirror the entire website
    $ wget -m http://saturn.picoctf.net:65086/
    --2023-12-30 14:23:21--  http://saturn.picoctf.net:65086/
    Resolving saturn.picoctf.net (saturn.picoctf.net)... 13.59.203.175
    Connecting to saturn.picoctf.net (saturn.picoctf.net)|13.59.203.175|:65086... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 15920 (16K) [text/html]
    Saving to: ‘saturn.picoctf.net:65086/index.html’

    saturn.picoctf.net:65086/index 100%[====================================================>]  15.55K  76.4KB/s    in 0.2s

    2023-12-30 14:23:21 (76.4 KB/s) - ‘saturn.picoctf.net:65086/index.html’ saved [15920/15920]

    Loading robots.txt; please ignore errors.
    --2023-12-30 14:23:21--  http://saturn.picoctf.net:65086/robots.txt
    Reusing existing connection to saturn.picoctf.net:65086.
    HTTP request sent, awaiting response... 404 Not Found
    2023-12-30 14:23:22 ERROR 404: Not Found.

    --2023-12-30 14:23:22--  http://saturn.picoctf.net:65086/css/bootstrap.min.css
    Reusing existing connection to saturn.picoctf.net:65086.
    HTTP request sent, awaiting response... 200 OK
    Length: 140421 (137K) [text/css]
    Saving to: ‘saturn.picoctf.net:65086/css/bootstrap.min.css’

    saturn.picoctf.net:65086/css/b 100%[====================================================>] 137.13K   277KB/s    in 0.5s

    2023-12-30 14:23:22 (277 KB/s) - ‘saturn.picoctf.net:65086/css/bootstrap.min.css’ saved [140421/140421]

    <SNIP>

    FINISHED --2023-12-30 14:23:36--
    Total wall clock time: 15s
    Downloaded: 20 files, 655K in 11s (61.5 KB/s)
    ```

2. We can see at the end of the above output that it has downloaded 20 files in total. We can see their structure using the `tree` command:

    ```shell
    ─$ tree
    .
    └── saturn.picoctf.net:65086
        ├── css
        │   ├── bootstrap.min.css
        │   ├── owl.carousel.min.css
        │   ├── responsive.css
        │   └── style.css
        ├── images
        │   ├── 1.png
        │   ├── 2.png
        │   ├── 3.png
        │   ├── banner.jpg
        │   ├── loading.gif
        │   ├── logo.png
        │   ├── mail_icon.png
        │   └── phone_icon.png
        ├── index.html
        └── js
            ├── bootstrap.bundle.min.js
            ├── custom.js
            ├── jquery-3.0.0.min.js
            ├── jquery.mCustomScrollbar.concat.min.js
            ├── jquery.min.js
            ├── owl.carousel.min.js
            └── popper.min.js

    5 directories, 20 files
    ```

3. Now we can use `grep` recursively to search for the string of interest:

    ```shell
    $ grep -R "picoCTF"
    saturn.picoctf.net:65086/css/style.css:/** banner_main picoCTF{1nsp3ti0n_0f_w3bpag3s_587d12b8} **/
    ```

## Resources

- John Hammond's [Search Across Web Elements (PicoCTF #22 'search-source')](https://www.youtube.com/watch?v=7PqL1g_25QQ).