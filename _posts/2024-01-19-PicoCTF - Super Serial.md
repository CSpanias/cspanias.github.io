---
title: PicoCTF - Super Serial
date: 2024-01-19
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, super-serial, phps]
img_path: /assets/picoctf/web_exploitation/super_serial
published: true
image:
    path: ../../picoctf_logo.png
---

![](room_banner.png){: width="70%"}

> **Description**: Try to recover the flag stored on this website `http://mercury.picoctf.net:2148/`.

1. The homepage looks like this: 

    ![](home.png){: .normal width="60%"}

2. When visiting `robots.txt` we get the following:

    ![](robots.png){: .normal}

3. Strangely enough, if we visit `/admin.phps` we get an error:

    ![](admin_phps.png){: .normal}

4. After searching what exactly `.phps` files are, we find [this] article:

    > ..._PHP files will get interpreted by the Web server and PHP executable, and you will never see the code behind the PHP file. If you make the file extension `.PHPS`, **a properly-configured server will output a color-formated version of the source** instead of the HTML that would normally be generated._

5. Based on that, we can infer that our server is configured to have `.phps` files, since there is a `/admin.phps` directory, so we can try see if that works on the `/index.php` by visiting `/index.phps`:

    ![](index_phps_browser.png)

    ![](index_phps_source.png)

6. We have 3 things of interest on the above code:
    1. A new script: `cookie.php`.
    2. Another script: `authentication.php`.
    3. A `setcookie` method which includes serialization.

7. After visiting the source code for each page, i.e., `/cookie.phps` and `/authentication.phps`, we see that the latter has an object of the class `access_log` which has the `log_file` attribute and uses the `__toString` method to read that log and get its content:

    ```php
    class access_log
    {
        public $log_file;

        function __construct($lf) {
            $this->log_file = $lf;
        }

        function __toString() {
            return $this->read_log();
        }

        function append_to_log($data) {
            file_put_contents($this->log_file, $data, FILE_APPEND);
        }

        function read_log() {
            return file_get_contents($this->log_file);
        }
    ```

    We know that our flag is under `../flag`, therefore, if we have an `access_log` object equal to that would be really handy.

8. On the `cookie.phps` code we have the following code:

    ```php
    if(isset($_COOKIE["login"])){
        try{
            $perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
            $g = $perm->is_guest();
            $a = $perm->is_admin();
        }
        catch(Error $e){
            die("Deserialization error. ".$perm);
        }
    }
    ```

    The `.$perm` variable represents our flag and it is shown when a **deserialization error** occurs. Thus, our goal is to trigger such an error. 

9. If we go to the `/authentication` directory and manually add the `login` cookie giving it a random value we get the following:

    ![](authentication_php_cookie.png)

    ![](login_cookie.png)

10. So we managed to invoke a **deserialization error**. The next step is to find a way to properly serializes the cookie with its value as `../flag`. We can replicate the serialization process based on `index.phps` code: `setcookie("login", urlencode(base64_encode(serialize($perm_res)))`. We can try serializing a simple string and check it gets deserialized when we pass it as a cookie:

    > [W3 PHP Online Compiler](https://www.w3schools.com/php/phptryit.asp?filename=tryphp_compiler).

    ![](test_cookie.png)

    ![](test_cookie1.png)

11. It successfully deserialized our cookie. Instead of just a string, we need an object of class `access_log` whose `log_file` attribute will be equal to `../flag`:

    ![](flag_cookie.png)

12. If we now pass that string as the value of the cookie `login`, we will get the flag back:

    ![](flag.png)


## Resources

- [Insecure deserialization - Theory](https://cspanias.github.io/posts/PS-Insecure-deserialization-Theory/)
- [Insecure deserialization - Practice](https://cspanias.github.io/posts/PS-Insecure-deserialization-Practice/)