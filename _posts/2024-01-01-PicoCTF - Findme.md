---
title: PicoCTF - Findme
date: 2024-01-01
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, findme]
img_path: /assets/picoctf/web_exploitation/findme
published: true
---

![](room_banner.png){: width="70%"}

> **Description**: _Help us test the form by submiting the username as `test` and password as `test`! Additional details will be available after launching your challenge instance._

1. Upon launching an instance we face a login form. When we use `test:test` as credentials, it instructs to use `test:test!` instead:

    ![](home.png){: .normal}

    ![](home_2.png){: .normal}

2. When we login with `test:test!` as our creds, we get into the `/home` directory. Intercepting the traffic with Bup the request looks like this:

    ![](login_with_test!.png)

    ![](login_with_test!_burp.png)

3. It seems like we get redirected to another page, more specifically `/next-page/id=cGljb0NURntwcm94aWVzX2Fs`. Landing there, we get redirected again to `/next-page/id=bF90aGVfd2F5X2JlNzE2ZDhlfQ==`:

    ![](login_with_test!_burp_2.png)

4. The latter seems like a base64 encoding string, so we can try to decode it:

    ```shell
    # decoding the base64 encoded string
    $ echo "bF90aGVfd2F5X2JlNzE2ZDhlfQ==" | base64 -d
    l_the_way_be716d8e}
    ```

5. This seems to be the second part of the flag, so the first redirection might also be encoded in base64:

    ```shell
    # decoding the base64 encoded string
    $ echo "cGljb0NURntwcm94aWVzX2Fs" | base64 -d
    picoCTF{proxies_al
    ```

6. We can join the two strings and submit our whole flag:

    ```shell
    $ echo "cGljb0NURntwcm94aWVzX2FsbF90aGVfd2F5X2JlNzE2ZDhlfQ==" | base64 -d
    picoCTF{proxies_all_the_way_be716d8e}
    ```