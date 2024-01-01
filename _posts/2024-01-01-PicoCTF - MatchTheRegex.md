---
title: PicoCTF - MatchTheRegex
date: 2024-01-01
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, matchtheregex, regex]
img_path: /assets/picoctf/web_exploitation/match_the_regex
published: true
---

![](room_banner.png){: width="70%"}

> **Description**: _How about trying to match a regular expression?_

1. The homepage consists of an input box where we can try putting our regular expression, aka regex, to try and match the flag:

    ![](home.png){: .normal}

2. When trying `test` as a test to see how this works we get a `wrong match! Try again!` message:

    ![](home_test.png){: .normal}

3. We could try a site like [regex101](https://regex101.com/) and build a regex that match the general picoCTF flag structure, such as the following:

    ![](regex_101.png)

4. Unfortunately, that did not work. We can take a look at the page's source code:

    ![](source_code.png)

5. As it seems it only needs a string sequence that matches the pattern in the comment, i.e., `^p.....F!?`:
    1. We need a sequence starting with the letter `p` (`^p`).
    2. Followed by any 5 characters (`.....`).
    3. Followed by the letter `F` (`F`).
    4. And we can have an exclamation mark (or not) at the end (`!?`). The `?` signifies that the preceded character is optional.

    So any string sequence that matches the above pattern will give us the flag:

    ![](flag.png)

    ![](flag1.png)

    ![](flag2.png)