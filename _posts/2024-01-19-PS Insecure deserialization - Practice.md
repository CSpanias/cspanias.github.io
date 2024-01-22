---
title: Insecure deserialization - Practice
date: 2024-01-19
categories: [PortSwigger, Insecure deserialization]
tags: [portswigger, lab, serialization, deserialization, burp, insecure-deserialisation, serialization, php, type-juggling, hackvertor]
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

This is known as [**Type Juggling**](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md#type-juggling): 

> _PHP is a loosely typed language, which means it tries to predict the programmer's intent and automatically converts variables to different types whenever it seems necessary. For example, a string containing only numbers can be treated as an integer or a float. However, this automatic conversion (or **type juggling**) can lead to unexpected results, especially when comparing variables using the `==` operator, which only checks for value equality (**loose comparison**), and not the `===` operator, which checks for both type and value equality (**strict comparison**)._


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

2. Let's start by log in, send the request to Repeater, and decode the cookie with Hackvertor:

    ![](lab2_hackvertor.png)

3. Upon decoding it, we see that there is the `username` attribute which should be changed to `administrator`. Then there is the `access_token` attribute with a value of `"tx6mwgc00s1475itu4br7ohv7zffdjg2"`.

    To bypass authentication, we need to make `if ($login['access_token'] == $access_token)` evaluate to `true`, that is, we need the stored token to match the token that we will pass. 
    
    We know that PHP will treat any string that **do not start with a number** as of equal to `0`. Thus, if we change the value of the `access_token` attribute to `0`, the following comparison `if ($login['access_token'] == $access_token)` will be converted into `0 == "<storedToken>"`, and if the `storedToken` does not start with a number, it will evaluate to `true`:

    ![](lab2_burp_redirection.png)

    > Remember to update the **type label**  for the `access_token` (`s` to `i`) as well as the length indicators for both `username` (`6` to `13`) and `access_token` (`32` to `0`).

4. If we click on "*Follow redirection*", we will see that we have access to the "*Admin panel*", and we can now delete user `carlos`:

    ![](lab2_adminPanel.png)

    ![](lab2_deleteCarlos.png)

    ![](lab2_solved.png)

### Using application functionality

A website's functionality might perform dangerous operations on data from a deserialized object. This would allow an attacker to pass in unexpected data and maliciously leverage the related functionality.

For example, as part of a website's "*Delete user*" functionality, the user's profile is deleted by accessing the file path in the `$user->image_location` attribute. If the `$user` attribute was created from a serialized object, an attacker could pass in a modified object with the `image_location` set to an arbitrary file path. Deleting their own user acc would then delete this arbitrary file as well.

### Lab: Using application functionality to exploit insecure deserialization

> **Objective**: _This lab uses a serialization-based session mechanism. A certain feature invokes a dangerous method on data provided in a serialized object. To solve the lab, edit the serialized object in the session cookie and use it to delete the `morale.txt` file from Carlos's home directory. You can log in to your own account using the following credentials: `wiener:peter`. You also have access to a backup account: `gregg:rosebud`._

1. After logging in as `wiener`, we can see that there is a "*Delete account*" functionality, and if we click on the button this is what the request looks like:

    ![](lab3_deleteAccount.png){: .normal width="60%"}

    ![](lab3_deleteAccount_burp.png)

2. We notice that there is a path pointing to the current user's avatar (`users/wieners/avatar`); if we simply change that and make point to the `morale.txt` file located within the home directory of user `carlos` (`/home/carlos/morale.txt`) and send the request, then both will be deleted:  

    ![](lab3_delete_file.png)

    If we now click on "*Follow redirection*":

    ![](lab3_solved.png)

### Magic methods

The previous example relies on the attacker **manually invoking the dangerous method via user-accessible functionality**. However, insecure deserialization becomes much more interesting when you create exploits that **pass data into dangerous methods automatically**. This is enabled by the use of "**magic methods**".

**Magic methods** are a special subset of methods that are invoked automatically whenever a particular event occurs. They are sometimes indicated by prefixing or surrounding the method name with **double-underscores**, for example, `__construct()` (PHP) and `__init__` (Python). These are similar methods that are invoked whenever an object of the class is instantiated.

Magic methods can become dangerous when the code that they execute handles attacker-controllable data, for example, from a deserialized object. This can be exploited by an attacker to automatically invoke methods on the deserialized data when the required conditions are met. Most importantly, **some languages have magic methods that are invoked automatically during the deserialization process**. For example, PHP's `unserialize()` methods looks for and invokes an object's `__wakeup()` magic method.

In Java deserialization, the same applies to the `ObjectInputStream.readObject()` method, which is used to read data from the initial byte stream and essentially acts like a constructor for "re-initializing" a serialized object. However, serializable classes can also declare their own `readObject()` method as follows:

```java
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException
{
    // implementation
}
```

A `readObject()` method declared in exactly this way acts as a magic method that is invoked during deserialization and allows the class to control the deserialization of its own fields more closely. 

You should pay close attention to any classes that contain these types of magic methods. They allow you to pass data from a serialized object into the website's code before the object is fully deserialized, which is often the starting point for creating more advanced exploits.

### Injecting arbitrary objects

In object-oriented programming, the methods available to an object are determined by its class. Therefore, if an attacker can manipulate which object class is being passed in as serialized data, they can influence what code is executed after, and even during, deserialization.

**Deserialization methods do not typically check what they are deserializing**, thus, you can pass in objects of any serializable class that is available to the webiste; this allows an attacker to create instances of arbitrary classes. **The fact that this object is not of the expected class does not matter**. The unexpected object migh cause an exception in the app logic, but the malicious object will already be instantiated by then!

If an attacker has source code access, they can study all the available classes in detail. To construct a simple exploit, they would **look for classes containing deserialization magic methods**, then check whether any of them perform dangerous operations on controllable data. The attacker can then pass in a serialized object of this class to use its magic method for an exploit.

### Lab: Arbitrary object injection in PHP

> **Objective**: _This lab uses a serialization-based session mechanism and is vulnerable to arbitrary object injection as a result. To solve the lab, create and inject a malicious serialized object to delete the `morale.txt` file from Carlos's home directory. You will need to obtain source code access to solve this lab. You can log in to your own account using the following credentials: `wiener:peter`._

> _**Hint**: You can sometimes read source code by appending a tilde (`~`) to a filename to retrieve an editor-generated backup file._

1. Logging in as `wiener` and checking the page's source code we see a refence to `CustomTemplate.php`:

    ![](lab4_source_code.png){: .normal}

2. If we append the `~` and send a `GET` request to `/libs/CustomTemplate.php` we will get the source code back. This contains two magic methods: `__construct()` and `__destruct()`:

    ![](lab4_magic_methods.png)

3. The `__destruct()` method invoked the [`unlink()`](https://www.php.net/manual/en/function.unlink.php) method on the `lock_file_path` attribute, which deletes the file on this path. What we need to do, is to create an object of class `CustomTemplate` containing just one attribute, `lock_file_path`, and set's the attribute's value to the desired file path, in this case, `/home/carlos/morale.txt`:

    ![](lab4_objectInjection.png)

    ![](lab4_solved.png){: .normal}


## Related resources

- [Type Juggling](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md).
- [PHP Magic Tricks: Type Juggling](https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf).
- [picoCTF: Super Serial](https://cspanias.github.io/posts/PicoCTF-Super-Serial/).
- [HTB: Precious](https://app.hackthebox.com/machines/Precious/).