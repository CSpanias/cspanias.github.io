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

## What is serialization?

**Serialization** is the process of converting complex data structures, such as objects and their fields, into a flatter format that can be send and received as a sequential stream of bytes in order to write them to inter-process memory, a file, or a database and/or send complex data over a network, between different network components, or in an API call.

![](https://inspector.dev/wp-content/uploads/2022/12/what-is-serialization-in-php-cover.png)

> [What is serialization in PHP](https://inspector.dev/what-is-serialization-in-php/).

When serializing an object, its **state (its attributes and value) is persisted**.

> _To prevent a field from being serialized, it must be explicitly marked as "**transient**" in the class declaration._

## Serialization vs deserialization

**Deserialization** is the process of restroing this byte stream to a fully function replica of the original object, so the webiste's logic can then interact with it.

![](https://portswigger.net/web-security/images/deserialization-diagram.jpg)

Many programming languages offer native support for serialization, but the process may differ: some serialize objects into binary formats, whereas other use different string formats.

> _Serialization may also be referred as "**marshalling**" (Ruby) or "**pickling**" (Python).

## What is insecure deserialization?

