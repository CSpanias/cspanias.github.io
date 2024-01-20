---
title: Insecure deserialization - Practice
date: 2024-01-19
categories: [PortSwigger, Insecure deserialization]
tags: [portswigger, lab, serialization, deserialization, burp, insecure-deserialisation, serialization, php, type-juggling]
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

PHP-based logic is vulnerable to data type manipulation due to the behavior of its **loose comparison operator** (`==`) when comparing different data types. For instance, when performing a loose comparison between an integer and a string, PHP will attempt to convert the string to an integer, meaning that `5 == "5"` will evaluate to `true`!

Unusually, **this also works for any alphanumeric string that starts with a number**. In this case, PHP will effectively convert the entire string to an integer value based on the initial number and the rest of it will be completely ignored. For example, `5 == "5 test"` will be treated as `5 == 5`!

This becomes even stranger when comparing a string to the integer `0`: if there is no initial number on the string, PHP will treat the entire string as the integer `0`. Therefore, `0 == "test"` will evaluate to `true`!

Consider a case where this loose comparison operator is used in conjuction with user-controllable data from a deserialized object. This could potentially result in dangerous **logic flaws**:

```php
$login = unserialize($_COOKIE)
if ($login['password'] == $password) {
    // log in successfully
}
```

Let's say that an attacker modified the `password` attribute so that it contained the integer `0` instead of the expected string. As long as the stored password does not start with a number, the condition would always return `true`, enabling **authentication bypass**! 

> _This is only possible, because **deserialization preserves the data type**. If the code fetched the password from the request directly, the `0` would be converted to a string and the condition would evaluate to `false`._

Be aware that when modifying data types in any serialized object format, it is important to **remember to update any type labels and length indicators** in the serialized data too. Otherwise, the serialized object will be corrupted and won't be deserialized.

#### Lab: Modifying serialized data types

> **Objective**: _This lab uses a serialization-based session mechanism and is vulnerable to authentication bypass as a result. To solve the lab, edit the serialized object in the session cookie to access the administrator account. Then, delete the user `carlos`. You can log in to your own account using the following credentials: `wiener:peter`._

1. We can repeat the process we did for the previous lab:
    1. Login as the user `wiener`.
    2. Decode the cookie using Hackvertor.
    4. Modify the required attributes and send the request.

2. Let's start by logging in, sending the request to Repeater, and decode the cookie with Hackvertor:

    ![](lab2_hackvertor.png)

3. Upon decoding it, we see that there is the `username` attribute which should be changed to `administrator`. Then there is the `access_token` attribute with a value of `"tx6mwgc00s1475itu4br7ohv7zffdjg2"`:

    To bypass authentication, we need to make `if ($login['access_token'] == $access_token)` evaluate to `true`, that is, we need the stored token to match the token that we will pass. 
    
    We know that PHP will treat any string that **do not start with a number** as of equal to `0`. Thus, if we change the value of the `access_token` attribute to `0`, the following comparison `if ($login['access_token'] == $access_token)` will be converted into `0 == "<storedToken>"`, and if the `storedToken` does not start with a number, it will evaluate to `true`:

    ![](lab2_burp_redirection.png)

4. If we click on "*Follow redirection*", we will see that we have access to the "*Admin panel*", and we can now delete user `carlos`:

    ![](lab2_adminPanel.png)

    ![](lab2_deleteCarlos.png)

    ![](lab2_solved.png)


## Futher practice

- [picoCTF: Super Serial](https://cspanias.github.io/posts/PicoCTF-Super-Serial/)
- [HTB: Precious](https://app.hackthebox.com/machines/Precious/)