---
title: PicoCTF - More Cookies
date: 2023-12-15
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, cookies]
img_path: /assets/picoctf/web_exploitation/more_cookies
published: true
image:
    path: ../../picoctf_logo.png
---

![](room_banner.png)

1. The homepage seems simple enough:

    ![](home.png)

2. By intercepting and inspecting the request with Burp, we see that there is a cookie called `auth_name` which seems to be Base64 encoded:

    ![](cookie_burp.png)

3. Decoding the cookie produces a series of strings seperated by a `/`:

    ![](base64_decoding.png)

4. Trying splitting the strings, base64 encoding them, and sending a new request with each one does not produce any interesting results:

    ![](base64_encoding.png)

5. If we decode it using Base64 a second time we get this:

    ```shell
    $ echo "ZmhwcEZQRVVUSlNxUWtjR08vVFJBdkJ2cVNVL1pCWHhlY0FNYVVhRzBzQzgrZ255R1JkTWhGNG0xZzFrYWJMUWVNMWRlbHBTZ2lHTG5UL2Jsbkh4Z3JJYUw3YjZBM0c0UFU5V3NyOTVHNnNjVitZUUlkbVRhM0lkb0V1aEFYTzE=" | base64 -d | base64 -d
    ~⸮i�L��BG;���o�%?d�y�
    di��x�]zZR�!��?ۖq�⸮/��q�=OV��yW�!ٓkr�K�s�
    ```

6. It's time to look up the first hint which is just a [Wikipedia article](https://en.wikipedia.org/wiki/Homomorphic_encryption), but after searching a bit more about it, I found this brilliant article about [Homomorphic Encryption](https://brilliant.org/wiki/homomorphic-encryption/#:~:text=Homomorphic%20encryption%20is%20malleable%20by,plain%20text%20that%20makes%20sense.):

    _**Homomorphic encryption is a cryptographic method that allows mathematical operations on data to be carried out on cipher text, instead of on the actual data itself**. The cipher text is an encrypted version of the input data (also called plain text). It is operated on and then decrypted to obtain the desired output. The critical property of homomorphic encryption is that the same output should be obtained from decrypting the operated cipher text as from simply operating on the initial plain text._

7. As always, when encountering complex topics for the first time reading led to even more reading. After going through some walkthroughs like [this](https://docs.abbasmj.com/ctf-writeups/picoctf2021#more-cookies), [this](https://www.youtube.com/watch?v=i9KiOjeE-VY), and [this](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md) there are some things to note down:

    1. Some letters are capitalized in the challenge's description which is a common way for authors to pass hints:

        ![](cbc.png)

    2. CBC stands for [**Cipher Block Chaining**](https://www.techtarget.com/searchsecurity/definition/cipher-block-chaining) which is a mode of operation for a block cipher and its key characteristic is that it uses a chaining process that causes the decrytpion of a block of ciphertext to depend on all the preceding ciphertext blocks.

    3. Essentially, there is a single bit that determines if the user is an admin. Maybe there is a parameter like `admin=0` and if we change the correct bit then we can set `admin=1`. However, the position of this bit is unknown, so we can try every position until we get the flag.

8. So at least we now know (kind of) what we are dealing with. After searching how we can break CBC, we learned that there is a common attack called the [**CBC Byte Flipping Attack**](https://www.techtarget.com/searchsecurity/definition/cipher-block-chaining) and there is even a [Python-written PoC](https://github.com/kelalaka153/CBC-Bit-Flipping-Attack/tree/main) for it. 

    Instead of reinventing the wheel, we can minimally modify HHousen's [code](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/improved_script.py) to perform the CBC Byte Flipping attack and get the flag as well as the encoded cookie value so we can then pass it to the request if we like to:

    ![](py_script.png)

    > You can find the modified code [here](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/picoctf/web_exploitation/more_cookies/cbc_byte_flipping_attack.py).

9. We can replace the cookie's value in our browser, refresh the page, and confirm that it is working:

    ![](flag_browser.png)

