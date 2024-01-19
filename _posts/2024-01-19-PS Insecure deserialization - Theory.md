---
title: Insecure deserialization - Theory
date: 2024-01-19
categories: [PortSwigger, Insecure deserialization]
tags: [portswigger, lab, serialization, deserialization, burp]
img_path: /assets/portswigger/insecure_deserialization/
published: true
image:
    path: ../portswigger_acad_logo.png
---

## Serialization

**Serialization** is the process of converting complex data structures, such as objects and their fields, into a flatter format that can be send and received as a sequential stream of bytes in order to write them to inter-process memory, a file, or a database and/or send complex data over a network, between different network components, or in an API call.

![](https://inspector.dev/wp-content/uploads/2022/12/what-is-serialization-in-php-cover.png)

> [What is serialization in PHP](https://inspector.dev/what-is-serialization-in-php/).

When serializing an object, its **state (its attributes and value) is persisted**.

> _To prevent a field from being serialized, it must be explicitly marked as "**transient**" in the class declaration._

## Deserialization

**Deserialization** is the process of restroing this byte stream to a fully function replica of the original object, so the webiste's logic can then interact with it.

![](https://hazelcast.com/wp-content/uploads/2021/12/deserialization-diagram-800x367-1.png)

Many programming languages offer native support for serialization, but the process may differ: some serialize objects into binary formats, whereas other use different string formats.

> _Serialization may also be referred as "**marshalling**" (Ruby) or "**pickling**" (Python).

## Insecure deserialization

**Insecure deserialization** is when user-controllable data is deserialized by a website: this enables an attacker to manipulate serialized objects in order to pass harmful data into the app code (aka **object injection vulnerability**).

It is possible to replace a serialized object with an object of an entirely different class. Objects of any class that is available to the website will be deserialized and instantiated, regardless of which class was expected. An object of an unexpected class might cause an exception, but the damage may already be done. **Many deserialization-based attacks are completed before deserialization is finished**. 

![](https://hazelcast.com/wp-content/uploads/2021/12/serialization-deserialization-diagram-800x318-1.png)

This means that **the deserialization process itself can initiate an attack**, even if the website's own functionality does not directly interact with the malicious object. For this reason, websites whose logic is based on strongly typed languages can also be vulnerable to these techniques.

## Causes

Insecure deserialization typically arises because there is a general lack of understanding of how dangerous deseriazing user-controllable data can be. Ideally, **user input should never be deserialized at all**.

It is virtually **impossible to implement validation or sanitization** to account for every eventuality. In addition, these checks are fundamentally flawed as they rely on checking the data after it has been deserialized, which in many cases will be too late. Vulnerabilities also arsies because **deserialized objects are often assumed to be trustworthy**. In particular, when using languages with a binary serialization format, developers might think that users cannot read or manipulate the data effectively, which is not true.

Deserialization-based attacks are also made possible due to the number of dependencies that exist in modern websites.An average website many implement many different libraries, which each have their own dependencies as well. This creates a **massive poll of classes and methods that is difficult to manage securely**. It is, therefore, **almost impossible to anticipate the flow of malicious data** and plug every potential hole.

In short, it can be argued that **it is not possible to securely deserialize untrusted input**.

## Impact

The impact of an insecure deserialization can be very severe, as it provides **an entry point to a massively increased attack surface**. It can lead to remote code execution, privilege escalation, arbitrary file access, and denial-of-service attacks.

## Prevention

**Deserialization of user input should be avoided unless absolutely necessary**. If it is necessary, incorporate robust measures to make sure that the data has not been tampered with, such as a digital signature to check its integrity. However, remember that **any checks must take place before beginning the deserialization process**.

If possible, **avoid using generic deserialization features altogether**. These contain all attributes of the original object, including private fields that potentially include sensitive data. Instead, **create you own class-specific serialization methods**, so that you can at least control which fields are exposed.

---

<center> <a href="https://cspanias.github.io/posts/PS-Insecure-deserialization-Practice/">[Insecure deserialization - Practice]</a> </center>

---