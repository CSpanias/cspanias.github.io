---
title: HTB - JSCalc
date: 2023-12-29
categories: [CTF, Web]
tags: [ctf, web, web-exploitation, htb, hack-the-box, js, jscalc]
img_path: /assets/htb/web/jscalc
published: true
---

![](room_banner.png)

## Overview

|:-:|:-:|
|Challenge|[JSCalc](https://app.hackthebox.com/challenges/jscalc)|
|Rank|Easy|
|Category|Web|

> CONTENT HIDDEN - ACTIVE MACHINE!
{: .prompt-warning}

<!-- 1. The home page is _a super secure Javascript calculator_:

    ![](home.png)

2. When we perform a calculation, it sends a `POST` request to `/api/calculate` including our calculation as a JSON value to `formula`:

    ![](calc_browser.png)

    ![](calc_burp.png)

3. When we open the link attached to the [`eval()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval) function, the following message appears:

    ![](eval.png)

4. In the `calculatorHelper.js` file, our input is directly passed into the `eval()` function:

    ```javascript
    // calculatorHelper.js
        module.exports = {
        calculate(formula) {
            try {
                return eval(`(function() { return ${ formula } ;}())`);

            } catch (e) {
                if (e instanceof SyntaxError) {
                    return 'Something went wrong!';
                }
            }
        }
    }


    // ocd
    ```

4. As a result we can pass JavaScript code as payload directly into the input box. For example, we can try including our file system:

    ![](require_fs.png)

    _The [Node.js file system module](https://www.w3schools.com/nodejs/nodejs_filesystem.asp) allows you to work with the file system on your computer. A common use for the File System module is to **read files**. To include the File System module, use the `require()` method:_
    
    ```javascript
    var fs = require('fs');
    ```

5. We can try reading `flag.txt` using the [`readFileSync()`](https://www.geeksforgeeks.org/node-js-fs-readfilesync-method/) function:

    ![](flag_buffer.png)

6. We get a series of numbers, thus, we can use the [`toString()`](https://www.w3schools.com/jsref/jsref_tostring_number.asp) method which returns a number as a string:

    ![](flag.png) -->

    ![](machine_pwned.png){: width="60%" .normal}