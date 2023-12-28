---
title: PicoCTF - It is my Birthday
date: 2023-12-28
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, it-is-my-birthday]
img_path: /assets/picoctf/web_exploitation/it_is_my_birthday
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The website lands us on a login form:

    ![](home.png){: width="60%" .normal}

2. Let's create a PDF file and try to upload it:

    ![](test_pdf.png)

    ![](test_upload.png)

    ![](error_message.png)

3. Let's create a different PDF file and try:

    ![](test1_pdf.png)

    ![](test_upload_1.png)

    ![](error_message_2.png)

4. So we have to upload different files with the same MD5 hash! Let's see the md5 hashes of our PDFs. `test.pdf` and `test2.pdf` has the same content, i.e. `test`:

    ```shell
    $ md5sum test.pdf
    7d2a156b9a52b714cdbbbd7f3b10dc67  test.pdf

    $ md5sum test1.pdf
    db5a11f395bb3568f3fd03467049b5e7  test1.pdf

    $ md5sum test2.pdf
    7d2a156b9a52b714cdbbbd7f3b10dc67  test2.pdf
    ```

5. If we search Google for "MD5 hash collision GitHub" we will find the [corkami's collisions](https://github.com/corkami/collisions) repository. There is a [PDF section](https://github.com/corkami/collisions#pdf) which includes the following examples:

    ![](pdf_repo.png)

6. We can download these PDF files, [poeMD5_A.pdf](https://github.com/corkami/collisions/blob/master/examples/poeMD5_A.pdf) and [poeMD5_B.pdf](https://github.com/corkami/collisions/blob/master/examples/poeMD5_B.pdf), and check their MD5 hashes:

    ```shell
    $ md5sum poeMD5_A.pdf
    b347b04fac568905706c04f3ba4e221d  poeMD5_A.pdf

    $ md5sum poeMD5_B.pdf
    b347b04fac568905706c04f3ba4e221d  poeMD5_B.pdf
    ```

7. Now everything should be ready to go:

    ![](upload_poems.png)

    ![](flag.png)


