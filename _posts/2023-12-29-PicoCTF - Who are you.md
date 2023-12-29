---
title: PicoCTF - Who are you?
date: 2023-12-29
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, who-are-you, http, http-headers]
img_path: /assets/picoctf/web_exploitation/who_are_you
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The website lands us on an interesting page:

    ![](home.png){: width="60%" .normal}

    ![](home_burp.png)

2. This challenge is focusing on HTTP headers, so having a [list of HTTP header fields](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields) open would be handy. Since it mentions `PicoBrowser` we can add that to the `User-Agent` HTTP header:

    > _The [User-Agent](https://en.wikipedia.org/wiki/User-Agent_header) header is an HTTP header intended to identify the user agent responsible for making a given HTTP request._

    ![](add_picobrowser_burp.png)

    ![](add_picobrowser.png){: width="60%" .normal}

3.  Now the message directs us to the request's origin, so let's add the `Referer` HTTP header and set its value to the same origin as the `Host`'s header:

    > _In HTTP, "[Referer](https://en.wikipedia.org/wiki/HTTP_referer)" (a misspelling of Referrer) is an optional HTTP header field that identifies the address of the web page (i.e., the URI or IRI), from which the resource has been requested. By checking the referrer, the server providing the new web page can see where the request originated._

    ![](referer_header_burp.png)

    ![](referer_header.png){: width="60%" .normal}

4. Based on the message, we can now add the `Date` HTTP header:

    > _The [Date](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Date) general HTTP header contains the date and time at which the message originated._

    ![](date_header_burp.png)

    ![](date_header.png){: width="60%" .normal}

5. Next, let's add the `DNT` (Do-Not-Track) HTTP header:

    > _[Do Not Track (DNT)](https://en.wikipedia.org/wiki/Do_Not_Track) is a formerly official HTTP header field, designed to allow internet users to opt-out of tracking by websites._

    ![](dnt_header_burp.png)

    ![](dnt_header.png){: width="60%" .normal}

6. Now, we have to find a relevant header that identifies the origin of the IP address, that is, `X-Forwarded-For`, combined with a Swedish IP address:

    > _The [X-Forwarded-For (XFF)](https://en.wikipedia.org/wiki/X-Forwarded-For) HTTP header field is a common method for identifying the originating IP address of a client connecting to a web server through an HTTP proxy or load balancer._

    > [Sweden IP Address Ranges](https://lite.ip2location.com/sweden-ip-address-ranges?lang=en_US).

    ![](swedish_ips.png){: .normal}

    ![](xForwardedFor_burp.png)

    ![](xForwardedFor.png){: width="60%" .normal}

7. Let's also add the `Accept-Language` HTTP header:

    > _The [Accept-Language](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language) request HTTP header indicates the natural language and locale that the client prefers._

    > [List of Hreflang Country and Language Codes](https://martinkura.com/list-hreflang-country-language-codes-attributes/).

    ![](accept_language_burp.png)

    ![](accept_language.png){: .normal}