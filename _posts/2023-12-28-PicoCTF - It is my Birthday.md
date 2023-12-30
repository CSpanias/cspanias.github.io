---
title: PicoCTF - It is my Birthday
date: 2023-12-28
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, it-is-my-birthday, hash, MD5, collision]
img_path: /assets/picoctf/web_exploitation/it_is_my_birthday
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The website lands us on an upload functionality:

    ![](home.png){: width="60%" .normal}

2. Let's create a PDF file and try to upload it:

    ![](test_pdf.png){: width="70%" .normal}

    ![](test_upload.png){: width="75%" .normal}

    ![](error_message.png){: .normal}

3. Let's create a different PDF file and try:

    ![](test1_pdf.png){: width="70%" .normal}

    ![](test_upload_1.png){: width="75%" .normal}

    ![](error_message_2.png){: .normal}

4. Let's calculate the MD5 hashes of our PDFs:

    ```shell
    $ md5sum test.pdf
    7d2a156b9a52b714cdbbbd7f3b10dc67  test.pdf

    $ md5sum test1.pdf
    db5a11f395bb3568f3fd03467049b5e7  test1.pdf
    ```

5. So we have to find two different files, ideally PDFs, with the same MD5 hash!

## Solution 1

6. If we search Google for "MD5 hash collision GitHub" we will find the [corkami's collisions](https://github.com/corkami/collisions) repository. There is a [PDF section](https://github.com/corkami/collisions#pdf) which includes the following examples:

    ![](pdf_repo.png)

7. We can download these PDF files, [poeMD5_A.pdf](https://github.com/corkami/collisions/blob/master/examples/poeMD5_A.pdf) and [poeMD5_B.pdf](https://github.com/corkami/collisions/blob/master/examples/poeMD5_B.pdf), and check their MD5 hashes:

    ```shell
    $ md5sum poeMD5_A.pdf
    b347b04fac568905706c04f3ba4e221d  poeMD5_A.pdf

    $ md5sum poeMD5_B.pdf
    b347b04fac568905706c04f3ba4e221d  poeMD5_B.pdf
    ```

8. Now everything should be ready to go:

    ![](upload_poems.png){: width="75%" .normal}

    ![](flag.png){: .normal}


## Solution 2

6. There is also [Selinger's MD5 Collision Demo](https://www.mscs.dal.ca/~selinger/md5collision/) which includes different binaries with the same MD5 hash:

    ![](bins_md5.png)

7. Let's check the binaries' MD5 hashes, and then try to upload them:

    ```shell
    $ md5sum erase
    da5c61e1edc0f18337e46418e48c1290  erase

    $ md5sum hello
    da5c61e1edc0f18337e46418e48c1290  hello
    ```

    ![](bin_upload_browser.png){: width="75%" .normal}

    ![](bin_upload_fail.png){: .normal}

8. We can try changing the [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) of the binaries using Burp:

    ![](erase_upload_burp.png)

    ![](erase_upload_burp_mod.png)