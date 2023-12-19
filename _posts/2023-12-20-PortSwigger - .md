---
title: PortSwigger Server-side vulnerabilities - File Path Traveral
date: 2023-12-20
categories: [Training, PortSwigger]
tags: [portswigger, server-side-vulnerabilities, directory-traversal]
img_path: /assets/portswigger/server-side/directory_traversal
published: true
---

> PortSwigger's [Server-side vulnerabilities](https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice).

## Path traversal

A path, aka directory or dot-dot-slash, vulneratibility enables the attacker to access (read or write) arbitrary files on the application server.


1. Let's say that a shopping app displays images loading this HTML code:

    ```html
    <img src="/loadImage?filename=218.png">
    ```

    The `loadImage` URL takes a `filename` parameter and returns the contents of `218.png`. The image is stored under `/var/www/images`, so it is essentially calling `/var/www/images/218.png`.

2. We can use `../` to navigate directories and requested anything we want from other directories:

    ```html
    https://insecure-website.com/loadImage?filename=../../../etc/passwd
    ```

    This translates to `/var/www/images/../../../etc/passwd`. 

    > On Windows, both `../` and `..\` are valid. 


> Related practice: [DVWA LFI](https://cspanias.github.io/posts/DVWA-File-Inclusion/).

## Lab: File path traversal, simple case

**Objective**: _This lab contains a path traversal vulnerability in the display of product images. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. It seems we are dealing with an e-shop:

    ![](dir_tra_home.png)

2. When we click on a product, we are directed to the `product` URL which has the `productId` parameter:

    ![](dir_tra_item.png)

3. If we view the page's source, we can find the image's path:

    ![](dir_tra_source.png)

4. We can examine this request via Burp Proxy's HTTP History, send it to the Repeater, and attempt our path traversal attack:

    ![](dir_tra_request.png)

5. We notice that our filter settings are hiding Images, among other things, so we need to change that:

    ![](dir_tra_filter_settings.png)

6. Now, when we refresh the page, we can see a new GET request to `/image` with the `filename` parameter:

    ![](dir_tra_request_image.png)

7. We can send it to the Repeater and try our Path Traversal attack:

    ![](dir_tra_repeater.png)

8. To mark this lab as `solved`, we need to actually intercept the request via Proxy, modify it, and Forward it:

    ![](dir_tra_intercept.png)

    ![](dir_tra_intercept_forward.png)

    ![](dir_tra_solved.png)