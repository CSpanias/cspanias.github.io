---
title: Path traversal
date: 2024-01-01
categories: [PortSwigger, Path traversal]
tags: [portswigger, path-traversal, directory-traversal, dot-dot-slash, burp, burp-intruder]
img_path: /assets/portswigger/path_traversal
published: true
image:
    path: ../portswigger_acad_logo.png
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

If an app strips or blocks directory traversal sequences from the user-supplied filename, it might be possible to bypass the defence using various techniques.
- We might be able to used an absolute path from the filesystem root, such as `filename=/etc/passwd`, to directly reference a file without using any traversal sequence ([Lab](https://cspanias.github.io/posts/PS-Path-Traversal/#lab-file-path-traversal-traversal-sequences-blocked-with-absolute-path-bypass)).
- We might be able to use nested traversal sequences, such as `....//` or `....\/`. There reverse to simple traversal sequences when the inner sequence is stripped ([Lab](https://cspanias.github.io/posts/PS-Path-Traversal/#lab-file-path-traversal-traversal-sequences-stripped-non-recursively), [DVWA example](https://cspanias.github.io/posts/DVWA-File-Inclusion/#local-file-inclusion-1)).
- In some contexts, such as in a URL path or the `filename` parameter of a `multipart/form-data` request, web servers may strip any directory traversal sequences before passing our input to the app. We can sometimes bypass this kind of sanitization by URL encoding, or even double URL encoding, the `../` characters. This results in `%2e%2e%2f` and `%252e%252e%252f`, respectively. Various non-standard encodings, such as `..%c0%af` or `..%ef%bc%8f`, may also work. In Burp Pro, Intruder provides the predefined payload list [**Fuzzing - path traversal**](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/Intruder/directory_traversal.txt), which contains some encoded path traversal sequences we can try ([Lab](https://cspanias.github.io/posts/PS-Path-Traversal/#lab-file-path-traversal-traversal-sequences-stripped-with-superfluous-url-decode)).
- An app may require the user-supplied filename to start with the expected base folder, such as `/var/www/images`. In this case, it might be possible to include the require base folder followed by suitable traversal sequences: `filename=/var/www/images/../../../etc/passwd` ([Lab](https://cspanias.github.io/posts/PS-Path-Traversal/#lab-file-path-traversal-traversal-sequences-stripped-with-superfluous-url-decode)).
- An app may require the user-supplied filename to end with an expected file extension, such as `.png`. In this case, it might be possible to use a **null byte** to effectively terminate the file path before the required extension: `filename=../../../etc/passwd%00.png` ([Lab](https://cspanias.github.io/posts/PS-Path-Traversal/#lab-file-path-traversal-validation-of-file-extension-with-null-byte-bypass)).

## Lab: File path traversal, traversal sequences blocked with absolute path bypass

> **Objective**: _This lab contains a path traversal vulnerability in the display of product images. The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. We first need to enable the Images MIME type:

    ![](lab1_image_filter.png)

2. Upon opening a product's image and intercepting the request we can see that there a `filename` parameter on the `/image` endpoint with the image's value, in this case, `18.jpg`:

    ![](lab1_image_new_tab.png){: width="60%" .normal}

    ![](lab1_image_burp.png)

3. If we try to replicate the path traversal attack from the previous lab, we will notice that it fails:

    ![](lab1_attack_fail.png)

4. However, when we pass the absolute value of the file path we are able to read the file:

    ![](lab1_passwd.png)

    ![](lab1_solved.png)

## Lab: File path traversal, traversal sequences stripped non-recursively

> **Objective**: _This lab contains a path traversal vulnerability in the display of product images. The application strips path traversal sequences from the user-supplied filename before using it. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. When we attempt to use the two previous attack techniques both fail:

    ![](lab2_attack_fail.png)

    ![](lab2_attack_fail_1.png)

2. We can try bypassing the defences by doubling-up our path traversal sequences:

    ![](lab2_attack.png)

    ![](lab2_solved.png)

## Lab: File path traversal, traversal sequences stripped with superfluous URL-decode

> **Objective**: _This lab contains a path traversal vulnerability in the display of product images. The application blocks input containing path traversal sequences. It then performs a URL-decode of the input before using it. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. When we try a simple path traversal attack, it fails:

    ![](lab3_simple_attack.png)

2. We can try to URL-encode our path traversal sequences and try again:

    ![](lab3_url_enc.png)

    ![](lab3_url_enc_once.png)

3. This did not work either, so we can try URL-encoding it for a second time:

    ![](lab3_url_enc_twice.png)

    ![](lab3_solved.png)

### Alternative automated solution

1. PayloadsAllTheThings's GitHub includes the [directory traversal wordlist](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/Intruder/directory_traversal.txt) which we can download and then load on Intruder:

    ![](lab3_path_traversal_enc_wordlist.png)

    ![](lab3_payload_pos.png)

    ![](lab3_payload_settings.png){: width="70%"  .normal}

2. After our attack is completed, we can see that none of the non-encoded payloads worked, but the three that were encoded worked fine:

    ![](lab3_non_enc_payloads.png){: width="60%" .normal}

    ![](lab3_enc_payloads.png){: width="60%"  .normal}


## Lab: File path traversal, validation of start of path

> **Objective**: _This lab contains a path traversal vulnerability in the display of product images. The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. The request of a product image includes the base path `/var/www/images/`:

    ![](lab4_burp.png)

2. If we try a simple path traversal attack, we get an error message:

    ![](lab4_filename_param_missing.png)

3. The `filename` parameter requires the base path (`/var/www/images/`) to be included in its value:

    ![](lab4_base_path.png)

    ![](lab4_solved.png)

## Lab: File path traversal, validation of file extension with null byte bypass

**Objective**: _This lab contains a path traversal vulnerability in the display of product images. The application validates that the supplied filename ends with the expected file extension. To solve the lab, retrieve the contents of the `/etc/passwd` file._

1. If we attempt a simple path traversal attack, it will fail:

    ![](lab5_simple_attack.png)

2. This is because it requires to have the `.png` string included in the `filename` parameter. We can add `.png` at the end of our payload and prefix it with a null byte (`%00`) so it gets ignored by the actual request:

    ![](lab5_attack.png)

## How to prevent a path traversal attack

The most effective way to prevent path traversal vulnerabilities is to avoid passing user-supplied input to filesystem APIs altogether. If we can't avoid passing user-supplied input to filesystem APIs, we can use two layers of defence to prevent attacks:
1. User input validation before processing it. Ideally, we should compare the user input with a whitelist of permitted values. If that is not possible, we should verify that the input contains only permitted content, such as alphanumeric characters only.
2. After user input validation, we could append the input to the base directory and use a platform filesystem API to canocicalize the path, and then verify that the canonicalized path starts with the expected base directory.

Below is an example of some simple Java code to validate the canonical path of a file based on user input:

```java
File file = new File(BASE_DIRECTORY, userInput);
if (file.getCanonicalPath().startsWith(BASE_DIRECTORY)) {
    // process file
}
```

## Resources

- [Path Traversal](https://portswigger.net/web-security/file-path-traversal).
- [Path Traversal (YouTube version)](https://www.youtube.com/watch?v=NQwUDLMOrHo&t=11s).