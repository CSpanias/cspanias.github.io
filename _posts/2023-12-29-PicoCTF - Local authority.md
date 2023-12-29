---
title: PicoCTF - Local Authority
date: 2023-12-29
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, local-authority]
img_path: /assets/picoctf/web_exploitation/local_authority
published: true
---

![](room_banner.png){: width="70%" .normal}

1. The homepage is a *Secure Customer Portal* which constis of a login form:

    ![](home.png){: .normal}

2. We can try logging in with random credentials, in this case `test:test`, and check what happens behind the scenes with Burp. There is a `POST` HTTP request to `login.php` which contains some interesting code snippets:

    ![](login_failed.png){: .normal}

    ![](login_php.png){: .normal}

    There is hidden directory called `admin.php` that we can send a `POST` request to, which includes the parameter `hash` and it seems to has as its value a hashed string:

    ```php
       <form hidden action="admin.php" method="post" id="hiddenAdminForm">
      <input type="text" name="hash" required id="adminFormHash">
    </form>
    ```

    If we continue reading the script, we will find the `filter(string)` function, which seems to filter the length of the passed string:

    ```php
    function filter(string) {
        filterPassed = true;
        for (let i =0; i < string.length; i++){
          cc = string.charCodeAt(i);
          
          if ( (cc >= 48 && cc <= 57) ||
               (cc >= 65 && cc <= 90) ||
               (cc >= 97 && cc <= 122) )
          {
            filterPassed = true;     
          }
          else
          {
            return false;
          }
        }
        
        return true;
      }
    ```

    Next, we can find out how the `filter()` function is used, and the `hash` parameter's value which seems to be static:

    ```php
      window.username = "test";
      window.password = "test";
      
      usernameFilterPassed = filter(window.username);
      passwordFilterPassed = filter(window.password);
      
      if ( usernameFilterPassed && passwordFilterPassed ) {
      
        loggedIn = checkPassword(window.username, window.password);
        
        if(loggedIn)
        {
          document.getElementById('msg').innerHTML = "Log In Successful";
          document.getElementById('adminFormHash').value = "2196812e91c29df34f5e217cfd639881";
          document.getElementById('hiddenAdminForm').submit();
        }
        else
        {
          document.getElementById('msg').innerHTML = "Log In Failed";
        }
      }
    ```

3. Based on that information, we can try bypass the log in functionality and sent a `POST` request to `admin.php` providing the `hash` parameter with the value of `2196812e91c29df34f5e217cfd639881`:

    ![](flag_burp.png)

4. We could also examine that subsequent `GET` request to `secure.js` as it includes the plaintext credentials which we can use to login in and get the flag this way.

    ![](secure_js.png)

    ![](flag.png){: .normal}