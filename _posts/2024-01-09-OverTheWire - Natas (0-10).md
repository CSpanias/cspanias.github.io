---
title: OverTheWire - Natas (0-10)
date: 2024-01-09
categories: [OverTheWire, Natas]
tags: [overthewire, natas, web-security]
img_path: /assets/overthewire/natas
published: true
image:
    path: natas.png
---

[Natas](https://overthewire.org/wargames/natas/) teaches the basics of **serverside web-security**.

Each level of natas consists of its own website located at http://natasX.natas.labs.overthewire.org, where `X` is the level number. There is no SSH login. To access a level, enter the username for that level (e.g. `natas0` for level `0`) and its password.

Each level has access to the password of the next level. Your job is to somehow obtain that next password and level up. All passwords are also stored in `/etc/natas_webpass/`. E.g. the password for `natas5` is stored in the file `/etc/natas_webpass/natas5` and only readable by `natas4` and `natas5`. Start here:
- Username: `natas0`
- Password: `natas0`
- URL: `http://natas0.natas.labs.overthewire.org`

## [Level 0](https://overthewire.org/wargames/natas/natas0.html)

![](natas0_home.png){: .normal}

If we just right click > *View Page Source* and check the page's source code, we can find the pass:

![](natas0_source.png){: .normal width="60%"}

![](natas0_pass.png){: .normal width="60%"}


## [Level 0 &rarr; 1](https://overthewire.org/wargames/natas/natas1.html)

> Password: g9D9cREhslqBKtcA2uocGHPfMZVzeFK6

![](natas1_home.png){: .normal}

We need to find the hotkey for viewing the page source by clicking the **three lines at the top right corner** > **More Tools** > **Page Source** or just hitting `CTRL + U`:

![](natas1_page_source_hotkey.png){: .normal width="60%"}

![](natas1_pass.png){: .normal width="60%"}

## [Level 1 &rarr; 2](https://overthewire.org/wargames/natas/natas2.html)

> Password: h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7

![](natas2_home.png){: .normal}

On the page's source code there is an image called `pixel.png`:

![](natas2_source.png){: .normal width="65%"}

When we click on it, we can see that is indeed only a pixel:

![](natas2_pixel.png){: .normal width="60%"}

However, this image resides within a `files/` directory, so we can try accessing that:

![](natas2_source2.png){: .normal width="70%"}

Within the `files/` directory many files exists, including `users.txt`:

![](natas2_pass.png){: .normal width="70%"}

## [Level 2 &rarr; 3](https://overthewire.org/wargames/natas/natas3.html)

> Passwrod: G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q

![](natas2_home.png){: .normal}

Viewing the page source with `CTRL + U`:

![](natas3_source.png){: .normal width="65%"}

The comment about Google points us to the existence of the [`robots.txt`](https://developers.google.com/search/docs/crawling-indexing/robots/intro) file: *A `robots.txt` file is used primarily to manage crawler traffic to your site, and **usually to keep a file off Google**, depending on the file type.*

![](natas3_robots.png){: .normal width="70%"}

The `robots.txt` file has blacklisted the `/s3cr3t` directory:

![](natas3_secret.png){: .normal width="70%"}

![](natas3_pass.png){: .normal width="70%"}

## [Level 3 &rarr; 4](https://overthewire.org/wargames/natas/natas4.html)

> Password: tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm

![](natas4_home.png){: .normal}

This challenge requires some familiarity with [**HTTP headers**](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields), and specifically the [**Referer**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer) header:

*The **Referer HTTP request header** contains the absolute or partial address from which a resource has been requested. The Referer header allows a server to identify referring pages that people are visiting from or where requested resources are being used.*

All we have to do is modify this request header before reaching the server. We can achieve this in many ways. We will do it using the browser extension [Tamper Data For FF Quantum](https://addons.mozilla.org/en-US/firefox/addon/tamper-data-for-ff-quantum/), the web app testing suite [Burp](https://portswigger.net/burp), and the API testing app [Postman](https://www.postman.com/).

### Tamper Data For FF Quantum

After adding the extension on our browser, we can click on it and click **Start**:

![](natas4_tamper_data_config.png){: .normal width="60%"}

After refreshing the page, we will find a list with all the HTTP headers used for this `GET` request. We need to modify the **Referer** value to http://natas5.natas.labs.overthewire.org/ and then click OK:

![](natas4_tamper_data_referer.png){: .normal width="60%"}

![](natas4_pass_browser.png){: .normal}

### Burp Suite

We can interecept and `GET` request and send it to the **Repeater** by pressing `CTRL + R`. The request looks like this: 

![](natas4_home_burp.png)

Again, we need to modify the value of the **Referer** header and then send the request:

![](natas4_pass_burp.png)

### Postman

We also use Postman's web GUI to do the same thing:

![](natas4_referer.png)

![](natas4_pass.png)

## [Level 4 &rarr; 5](https://overthewire.org/wargames/natas/natas5.html)

> Password: Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD

![](natas5_home.png){: .normal}

If we intercept the traffic with Postman, we will see that this is a `GET` request which includes a `loggedin` cookie with the value of `0`:

![](natas5_postman_request.png)

We can modify the cookie's value by first clicking to **Cookies** and then setting the value to `1`:

![](natas5_cookies.png){: .normal width="75%"}

![](natas5_cookies1.png){: .normal width="75%"}

If we send the request now, we should receive next level's password in the response:

![](natas5_pass.png)

## [Level 5 &rarr; 6](https://overthewire.org/wargames/natas/natas6.html)

> Password: fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR

![](natas6_home.png){: .normal width="70%"}

It seems that we have to find a secret query in order to get the next level's password. Let's check the page's source code:

![](natas6_source.png){: .normal}

The code tell us all we need: we need to submit a `POST` request to `/includes/secret.inc` directory for revealing the secret query:

![](natas6_secret.png)

We can now submit the secret query and obtain the password for the next level:

![](natas6_pass.png){: .normal width="70%"}

## [Level 6 &rarr; 7](https://overthewire.org/wargames/natas/natas7.html)

> Password: jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr

![](natas7_home.png){: .normal width="70%"}

There are two hyperlinks to click on: `Home` and `About`. When we click on one of them, for example, `Home`, we notice that a parameter called `page` appears on the address bass with the value of `home`:

![](natas7_page_param.png){: .normal}

If we check the response with Burp, we can see that there is a hint disguised as a comment:

![](natas7_home_burp.png)

We can set the value of the `page` parameter to `/etc/natas_webpass/natas8` and we will receive the next level's password in the response:

![](natas7_pass.png)

## [Level 7 &rarr; 8](https://overthewire.org/wargames/natas/natas8.html)

> Password: a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB

![](natas8_home.png){: .normal width="70%"}

Let's check the source code:

![](natas8_source.png){: .normal}

The source code includes the `encondedSecret` variable assigned the value of `3d3d516343746d4d6d6c315669563362`. Right below that there is the `encodeSecret` function from which we can see how the secret was encoded:
1. ASCII &rarr; Base64
2. The output was reversed.
3. The reverse output was encoded to hexadecimal which produced the `encodedSecret`'s value.

So we will need to reverse that process in order to get the original ASCII string back:
1. Hex &rarr; ASCII.
2. Reverse string.
3. Base64 &rarr; ASCII.

To achieve that, we can either use [CyberChef](https://gchq.github.io/CyberChef), or Bash:

![](natas8_cyberchef.png){: .normal width="70%"}

```bash
# convert hex to ASCII
$ echo 3d3d516343746d4d6d6c315669563362 | xxd -r -p
==QcCtmMml1ViV3b
# reverse string
$ echo ==QcCtmMml1ViV3b | rev
b3ViV1lmMmtCcQ==
# base64 to ASCII
$ $ echo b3ViV1lmMmtCcQ== | base64 -d
oubWYf2kBq

# in a single command
$ echo 3d3d516343746d4d6d6c315669563362 | xxd -r -p | rev | base64 -d
oubWYf2kBq
```

When we submit this query as our secret string, we get the password for the next level:

![](natas8_pass.png){: .normal width="70%"}

## [Level 8 &rarr; 9](https://overthewire.org/wargames/natas/natas9.html)

> Password: Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd

![](natas9_home.png){: .normal width="70%"}

![](natas9_source.png){: .normal}

If we input the string `random` and intercept the traffic with Burp, this is what the request looks like:

![](natas9_params_burp.png)

Based on the page's source code, whatever we input in the search box, goes straight into the `grep` command without any validation or sanitization. That makes this app vulnerable to a [**command injection**](https://cspanias.github.io/posts/DVWA-Command-Injection/#command-injection). Let's check if it works:

![](natas9_ci.png)

Now that we have confirmed the CI vulnerability, we can replace the `id` command and instead read `natas10`'s password:

> Highlight the payload and press `CTRL+U` to URL encode it before sending the request.

![](natas9_pass.png)

## [Level 9 &rarr; 10](https://overthewire.org/wargames/natas/natas10.html)

> Password: D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE

![](natas10_home.png){: .normal width="70%"}

![](natas10_source.png){: .normal}

Now the developer filters our input and removes characters that are commonly used for a [command injection](https://cspanias.github.io/posts/DVWA-Command-Injection/#command-injection) attack, such as `;`, `|`, and `&`. Howenver, we can leverage the `grep` utility itself this time, since our input is still passed directly to it. 

We can use the regex `.*` which matches any sequence of characters and then search for `/etc/natas_webpass/natas11` and `dictionary.txt` (which is already within the command). This will result in grepping everything that matches these 2 strings:

![](natas10_pass.png)

---

<center> <a href="https://cspanias.github.io/posts/OverTheWire-Natas-(11-20)/">[Level 11-20]</a> </center>

---