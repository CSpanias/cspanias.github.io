---
title: Marketplace CTF Write Up (2023)
date: 2023-10-20
categories: [CTF Write Up, THM]
tags: [xss, idor, cookies, ]
img_path: /assets/marketplace/
mermaid: true
---

![marketplace_banner](marketplace_banner.png)

## 1 Summary

<!-- Graph summary -->

## 2 Background Information

[The Marketplace](https://tryhackme.com/room/marketplace) room feel like a "real-world" penetration testing scenario, as it involves no guidance at all:

>The sysadmin of The Marketplace, Michael, has given you access to an internal server of his, so you can pentest the marketplace platform he and his team has been working on. He said it still has a few bugs he and his team need to iron out.

And that's all there is! We are now left alone to figure out where those three flags are!

### 2.1 IDOR

Taken from, the highly recommended, TryHackMe's [IDOR room](https://tryhackme.com/room/idor):
 
**Insecure Direct Object Reference** is a type of **access control vulnerability**. This can occur when a web server receives user-supplied input to retrieve objects and the input data is not properly validated on the server-side to confirm the requested object belongs to the user requesting it.

For example, the following link could open a user's own profile: `http://online-service.thm/profile?user_id=1305`. If he could see another user's profile by changing the `id` value, it is an IDOR vulnerability.

## 3 CTF Process

### 3.1 Visiting the webserver

Let's start by visiting the website:

![marketplace_homepage](marketplace_homepage.png)

 The first we always do is checking if there is a [`/robots.txt`](https://moz.com/learn/seo/robotstxt) subdirectory, and in this case there is. We just learned tha `/admin` exist, but, as expected, we are not authorized to view it; yet! 

![robots-txt](robots-txt.png)

![admin-dir-no-auth](admin-dir-not-auth.png)

While exploring the site, there are some more things to note down:

1. There is a **Log In** page. It is always worth experimenting with such as page, as it can give us useful, i.e. informative, error messages.
2. There is also a **Sign up** page. The **hint** provided on the first question, i.e. *If you think a listing is breaking the rules, you can report it!*, make us think that we should probably should create an account and report something.
3. When clicking on the images, the address bar change as follows: `http://<target-ip>/item/1` for the laptop and `/item/2` for the cactus. It might be worth-checking if the site is susceptible to an *IDOR vulnerability*.


Let's start checking each point in sequence.

When trying to log in with random creds, for example, `admin:admin`, we got the following message:

![user-not-found-error](user-not-found-error.png)

The images found on the homepage are having their publishers listed, `michael` and `jake`. If we try to login in with either of the two, we get this:

![invalid-password](invalid-password.png)

So we already have two valid usernames at hand, and we could try a *dictionary attack with `hydra`* to see if we can find their passwords, a similar process we did at the [Mr Robot](https://cspanias.github.io/posts/Mr-Robot-Write-Up-(2023)/#23-dictionary-attack-with-hydra) room, but, unfortunately, it did not work this time.

Let's try to exploit our second point, the **Sign up** page as well as the author's hint, as it should logically guide us to the first flag.

When signing up, a new option appears: *New listing*:

![new-listing](new-listing.png)

We can check if the site is vulnerable to [XSS](https://owasp.org/www-community/attacks/xss/), by writing some simple code and see how the site reacts:

![XSS](xss.mp4)

 🍻🥂🔒🚩🎊🎉