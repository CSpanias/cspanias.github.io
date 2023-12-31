---
title: OverTheWire - Natas (0-10)
date: 2024-01-06
categories: [OverTheWire, Natas]
tags: [overthewire, natas, web-security]
img_path: /assets/overthewire/natas
published: true
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



## [Level 5 &rarr; 6](https://overthewire.org/wargames/natas/natas6.html)

> Password:



## [Level 6 &rarr; 7](https://overthewire.org/wargames/natas/natas7.html)

> Password: 



## [Level 7 &rarr; 8](https://overthewire.org/wargames/natas/natas8.html)

> Password: 



## [Level 8 &rarr; 9](https://overthewire.org/wargames/natas/natas9.html)

> Password: 


## [Level 9 &rarr; 10](https://overthewire.org/wargames/natas/natas10.html)

> Password: 



<!--
---

<center> <a href="https://cspanias.github.io/posts/OverTheWire-Natas-(0-10)/">[Level 0-10]</a> </center>

---
-->