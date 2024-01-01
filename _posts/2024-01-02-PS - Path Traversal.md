---
title: Path Traversal
date: 2024-01-01
categories: [PortSwigger, Path Traversal]
tags: [portswigger, path-traversal, directory-traversal, dot-dot-slash]
img_path: /assets/portswigger/path_traversal
published: true
---

## What is Path Traversal?

**Path traversal**, aka as **directory traversal** or **dot-dot-slash** attack, enables an attacker to read arbitrary files on the server that is running an application. In some cases, an attacker might be able to write to arbitrary files on the server, allowing them to modify app data or behavior, and ultimately take full control of the server.

## Reading arbitrary files via path traversal

Imagine a shopping application that displays images of items for sale. This might load an image using the following HTML: `<img src="/loadImage?filename=218.png">`.

The `loadImage` URL takes a `filename` parameter and returns the contents of the specified file. The image files are stored on disk in the location `/var/www/images/`. To return an image, the application appends the requested filename to this base directory and uses a filesystem API to read the contents of the file. In other words, the application reads from the following file path: `/var/www/images/218.png`.

This application implements no defenses against path traversal attacks. As a result, an attacker can request the following URL to retrieve the `/etc/passwd` file from the server's filesystem: `https://insecure-website.com/loadImage?filename=../../../etc/passwd`. This causes the application to read from the following file path: `/var/www/images/../../../etc/passwd`.

The sequence `../` is valid within a file path, and means to step up one level in the directory structure. The three consecutive `../` sequences step up from `/var/www/images/` to the filesystem root, and so the file that is actually read is: `/etc/passwd`.

On Unix-based operating systems, this is a standard file containing details of the users that are registered on the server, but an attacker could retrieve other arbitrary files using the same technique. On Windows, both `../` and `..\` are valid directory traversal sequences. The following is an example of an equivalent attack against a Windows-based server: `https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini`.

## Lab: File path traversal, simple case

> **Objective**: _This lab contains a path traversal vulnerability in the display of product images. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. It seems we are dealing with an e-shop:

    ![](../server-side/directory_traversal/dir_tra_home.png)

2. We can click on a product and examine the traffic with Burp, but first we need to whitelist images via our filter settings:

    ![](../server-side/directory_traversal/dir_tra_filter_settings.png){: .normal}

    ![](../server-side/directory_traversal/dir_tra_filter_settings_2.png)

3. We can now examine the request via Burp Proxy's HTTP History by refreshing the page. There we can see a GET request to the `/image` URL which takes the `filename` parameter:

    ![](../server-side/directory_traversal/dir_tra_request_image.png){: .normal}

4. We can send it to the Repeater and try our Path Traversal attack:

    ![](../server-side/directory_traversal/dir_tra_repeater.png)

    ![](../server-side/directory_traversal/dir_tra_solved.png)

## Common obstacles to exploiting path traversal vulnerabilities

## Resources

- [Path Traversal](https://portswigger.net/web-security/file-path-traversal).
- [Path Traversal (YouTube version)](https://www.youtube.com/watch?v=NQwUDLMOrHo&t=11s).