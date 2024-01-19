---
title: Insecure deserialization - Practice
date: 2024-01-19
categories: [PortSwigger, Insecure deserialization]
tags: [portswigger, lab, serialization, deserialization, burp]
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

## Futher practice

- [picoCTF: Super Serial](https://cspanias.github.io/posts/PicoCTF-Super-Serial/)