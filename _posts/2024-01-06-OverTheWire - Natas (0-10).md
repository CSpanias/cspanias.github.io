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

The homepage says this:

![](natas0_home.png)

If we just right click > *View Page Source* and check the page's source code, we can find the pass:

![](natas0_source.png)

![](natas0_pass.png)

<!--
---

<center> <a href="https://cspanias.github.io/posts/OverTheWire-Natas-(0-10)/">[Level 0-10]</a> </center>

---
-->