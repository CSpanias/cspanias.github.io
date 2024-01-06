---
title: OverTheWire - Bandit (20-33)
date: 2024-01-02
categories: [OverTheWire, Bandit]
tags: [overthewire, bandit, linux]
img_path: /assets/overthewire/bandit
published: true
---



## [Level 20 &rarr; 21](https://overthewire.org/wargames/bandit/bandit21.html)

> There is a `setuid` binary in the `home` directory that does the following: it makes a connection to `localhost` on the port you specify as a command-line argument. It then reads a line of text from the connection and compares it to the password in the previous level (`bandit20`). If the password is correct, it will transmit the password for the next level (`bandit21`).

> NOTE: Try connecting to your own network daemon to see if it works as you think.

```bash
$ ssh bandit20@bandit.labs.overthewire.org -p 2220
```

We can create a **onetime server**, a server that sends one message and then disconnects, using `nc -lp` and then pass it a message with the combination of the `echo` command and the pipe (`|`) operator. We can background this operation using `&` at the end so we can continue to use our terminal instead of opening a new one:

```bash
bandit20@bandit:~$ echo -n 'VxCazJaVykI6W36BkBU0mJTCM8rR95XT' | nc -lp 1337 &
[1] 3062056
```

Now we need to run the binary using the same port as our server (`1337`) so it can connect to it, receive the password inputted through `echo`, and sends us back the new one:

```bash
bandit20@bandit:~$ ./suconnect 1337 VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Read: VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Password matches, sending next password
NvEJF7oVjkddltPSrdKEFOllh9V1IBcq
[1]+  Done                    echo -n 'VxCazJaVykI6W36BkBU0mJTCM8rR95XT' | nc -lp 1337
```

## [Level 21 &rarr; 22](https://overthewire.org/wargames/bandit/bandit22.html)

> A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

```bash
$ ssh bandit21@bandit.labs.overthewire.org -p 2220

# list directory files
bandit21@bandit:~$ ls /etc/cron.d
cronjob_bandit15_root  cronjob_bandit22  cronjob_bandit24       e2scrub_all  sysstat
cronjob_bandit17_root  cronjob_bandit23  cronjob_bandit25_root  otw-tmp-dir

# display the file content
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null

# display the file content
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

The above bash script modifies the permissions (`chmod 644`) of the `/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv` file and then copies the next level's password to that file. The `644` permissions correspond to the owner of the file (`bandit22`) having read (`r`) and write (`w`) permissions and the group and others having read permissions only. As a result, everyone can read it. 

```bash
# check file's permissions
bandit21@bandit:/etc/cron.d$ ls -l /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
-rw-r--r-- 1 bandit22 bandit22 33 Jan  3 20:22 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv

bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff
```

## [Level 22 &rarr; 23](https://overthewire.org/wargames/bandit/bandit23.html)

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

> NOTE: Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.

```bash
$ ssh bandit22@bandit.labs.overthewire.org -p 2220

bandit22@bandit:~$ ls -l /etc/cron.d
total 36
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit15_root
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit17_root
-rw-r--r-- 1 root root 120 Oct  5 06:19 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct  5 06:19 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct  5 06:19 cronjob_bandit24
-rw-r--r-- 1 root root  62 Oct  5 06:19 cronjob_bandit25_root
-rw-r--r-- 1 root root 201 Jan  8  2022 e2scrub_all
-rwx------ 1 root root  52 Oct  5 06:20 otw-tmp-dir
-rw-r--r-- 1 root root 396 Feb  2  2021 sysstat

bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null

bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

Let's break down what this bash script does:
1. `myname=$(whoami)` The `whoami` commands outputs the current user and since this is written by `bandit23`, the `myname` variable will be assigned that name.
2. `mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)` The first part just outputs 'I am user bandit23', the second part hashes that string using the MD5 hashing algorithm, and then third part splits the output using space as the delimiter and picks the first field. The latter is then assigned to the variable `mytarget`.
3. Then goes on to echo the following string: "Copying passwordfile /etc/bandit_pass/bandit23 to /tmp/<mytarget>".
4. Finally, it copies the password from `/etc/bandit_pass/bandit23` the a file under the `/tmp/` directory with the `mytarget`'s value as its name.

An example of what's happening:

```bash
# hashing the string using MD5
bandit22@bandit:~$ echo I am user bandit23 | md5sum
8ca319486bfbbc3663ea0fbe81326349  -

# selecting the first field of the output
bandit22@bandit:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
```

So the password should be stored in the following file `/tmp/8ca319486bfbbc3663ea0fbe81326349`.

```bash
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G
```

## [Level 23 &rarr; 24](https://overthewire.org/wargames/bandit/bandit24.html)

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

> NOTE: This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!

> NOTE 2: Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…

```bash
$ ssh bandit23@bandit.labs.overthewire.org -p 2220

bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null

bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```

Let's break down what the above bash script does:

The `myname` variable is assigned the output of the command `whoami` typed by the user `bandin24`. 

```bash
bandit23@bandit:~$ whoami
bandit23
```

Then iterates through all files within the `/var/spool/bandit24/foo` directory, ignores the current (`.`) and previous (`..`) directories, and then checks who is the owner of the file.  

```bash
bandit23@bandit:/tmp$ stat --format "%U" test.txt
bandit23
```

  > [`stat` command in Linux](https://linuxize.com/post/stat-command-in-linux/).

Finally, if the owner is the user `bandint23`, it executes the script. If the scripts runs for more than 60 seconds, then it will be forcefully terminated. Finally, it deletes the script.

As a result, we have to create a script that reads `bandit24`'s password, move it to the `/var/spool/bandit24/foo/` directory, and wait for it to execute. According to the output of `/etc/cron.d/cronjob_bandit24`, it executes every minute, so it should be executed within maximum of 1 minute.

```bash
# create a new director within /tmp
bandit23@bandit:~$ mkdir /tmp/lvl_23/
# move to the newly-created dir
bandit23@bandit:~$ cd /tmp/lvl_23
# create the required script
bandit23@bandit:/tmp/lvl_23$ nano bandit23.sh
# display the script's content
bandit23@bandit:/tmp/lvl_23$ cat bandit23.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/lvl_23/lvl_24_pass
# create the file that the password will be written to
bandit23@bandit:/tmp/lvl_23$ touch lvl_24_pass
# give appropriate permissions to the script, directory, and password file
bandit23@bandit:/tmp/lvl_23$ chmod +rx bandit23.sh
bandit23@bandit:/tmp/lvl_23$ chmod 777 /tmp/lvl_23
bandit23@bandit:/tmp/lvl_23$ chmod 777 lvl_24_pass
# check files' permissions
bandit23@bandit:/tmp/lvl_23$ ls -la
total 408
drwxrwxrwx    2 bandit23 bandit23   4096 Jan  4 17:18 .
drwxrwx-wt 3062 root     root     405504 Jan  4 17:19 ..
-rwxrwxr-x    1 bandit23 bandit23     67 Jan  4 17:17 bandit23.sh
-rwxrwxrwx    1 bandit23 bandit23      0 Jan  4 17:18 lvl_24_pass
# copy the script to the appropriate directory
bandit23@bandit:/tmp/bandit23_dir$ cp bandit23.sh /var/spool/bandit24/foo/
# wait for a minute and check if the file has changed
bandit23@bandit:/tmp/lvl_23$ cat lvl_24_pass
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar
```

## [Level 24 &rarr; 25](https://overthewire.org/wargames/bandit/bandit25.html)

> A daemon is listening on port `30002` and will give you the password for `bandit25` if given the password for `bandit24` and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called **brute-forcing**. You do not need to create new connections each time.

```bash
$ ssh bandit24@bandit.labs.overthewire.org -p 2220
```

We can connect to the listening port using `nc`:

```bash
bandit24@bandit:/tmp/lvl_24$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
# input the correct flag and a random 4-digit pincode
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar 0000
Wrong! Please enter the correct pincode. Try again.
```

Now we can create a brute-forcing script to get all the possible combinations. We can loop through all possible 4-digit combinations (`for i in {0000..9999}`), add each pin to the flag separated by a space (`echo "$password $i"`), and then append each sequence to a file (`>> pin_combinations.txt`). 

Passing the file as it is, i.e., with the 10000 resulting combinations, makes the connection to timeout, so we have to split it into 2 separate files (`split -l 5000 pin_combinations.txt pin_`). We can then pass each file to the daemon listening (`nc localhost 30002 < pin_aa > results_A` & `nc localhost 30002 < pin_ab >> results_A`), and search for a unique row in the final output (`sort results_A | uniq -u`):

```bash
bandit24@bandit:/tmp/lvl_24$ nano bruteForce.sh
bandit24@bandit:/tmp/lvl_23$ cat bruteForce.sh
#!/bin/bash

# set a variable with the previous level flag
password="VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar"
# confirm the password
echo "The password is: $password."

echo "Creating the pin combination file..."
# iterate through all combinations of a 4-digit password
for i in {0000..9999}
do
        # append the password plus the pin combination separated by a space to a file
        echo "$password $i" >> pin_combinations.txt
done
echo "Done."

echo "Splitting the file into two..."
# split the file into 2 separate files
split -l 5000 pin_combinations.txt pin_
echo "Done."

echo "Brute-force starting...passing the first file..."
# pass the first file and write the results
nc localhost 30002 < pin_aa > results_A
echo "Done."

echo "Brute-force continues...passing the second file..."
# pass the second file and write the results
nc localhost 30002 < pin_ab >> results_A
echo "Done."

echo "Searching for the flag..."
# search for the flag
sort results_A | uniq -u
echo "Flag found!"
```

Now all we have to do, is execute our script:

```bash
# execute the script
bandit24@bandit:/tmp/lvl_23$ ./bruteForce.sh
The password is: VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar.
Creating the pin combination file...
Done.
Splitting the file into two...
Done.
Brute-force starting...passing the first file...
Done.
Brute-force continues...passing the second file...
Done.
Searching for the flag...

Correct!
Exiting.
The password of user bandit25 is p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d
Timeout. Exiting.
Flag found!
```

## [Level 25 &rarr; 26](https://overthewire.org/wargames/bandit/bandit26.html)

> Logging in to `bandit26` from `bandit25` should be fairly easy… The shell for user `bandit26` is not `/bin/bash`, but something else. Find out what it is, how it works and how to break out of it.

```bash
$ ssh bandit25@bandit.labs.overthewire.org -p 2220

# list directory's files
bandit25@bandit:~$ ls
bandit26.sshkey
# display file's content
bandit25@bandit:~$ cat bandit26.sshkey
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0ECgYEA1crBUAR1gSkM+5mGjjoFLJKrFP+IhUHFh25qGI4Dcxxh1f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
```

First, since there is a private key lying around, let's copy and paste it to our machine since we will use to log in to the next level:

```bash
# check file's content
$ head -5 id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
# assign the appropriate permissions to the file
$ sudo chmod 400 id_rsa
# check file's permissions
$ ls -l id_rsa
-r-------- 1 root root 1679 Jan  5 06:56 id_rsa
```

Then going back to our SSH connection, we can check which shell is assigned to each user by checking the `/etc/passwd` file:

```bash
# check users' assigned shells
bandit25@bandit:~$ cat /etc/passwd | grep 'bandit25\|bandit26'
bandit25:x:11025:11025:bandit level 25:/home/bandit25:/bin/bash
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
# check file's content
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

For the user `bandit26` a script called `showtext` is assigned as a shell, which opens the `text.txt` file using `more`. [`more`](https://linux.die.net/man/1/more) is used to view large text files, displaying one screen at a time. Its **interactive mode** only works when the file's content is too large to fully be displayed in the current terminal window and it is based on the `vi` text editor.

As this level's instructions say, we must find a way to break out of `more`. From playing many fullpwn CTFs and constantly using [GTFOBins](https://gtfobins.github.io/gtfobins/vi/#shell), we know that commands can be passed to `vi` and it can be used to break out from restricted environments by spawing an interactive system shell:

![](gtfobins_vi.png){: .normal}

As a result, we can try limiting our terminal's display for `more`'s interactive mode to work, and then spawn a shell through `vi` (using option (b)):

![](level_25_to_26.png){: .normal}

```bash
# connect as bandit26 to SSH
$ sudo ssh bandit26@bandit.labs.overthewire.org -i id_rsa -p 2220
```

After logging in we are in `vi`'s command mode:

![](more_login.png){: .normal}

Now, we can press `v` to go into `vi` and follow GTFOBins instructions:

```bash
# set the user's shell to /bin/bash
:set shell=/bin/bash
# drop into the above-defined shell
:shell
bandit26@bandit:~$
```

Now, we can just read the password of `bandit26` and proceed to the next level:

```bash
bandit26@bandit:~$ cat /etc/bandit_pass/bandit26
c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1
```

## [Level 26 &rarr; 27](https://overthewire.org/wargames/bandit/bandit27.html)

> Good job getting a shell! Now hurry and grab the password for `bandit27`!

To get the password for `bandit27`, we have to login using the solution of the previous level. Once we reach the point that we have dropped on a shell we can see what's within the user's home directory:

```bash
# list directory's files
bandit26@bandit:~$ ls
bandit27-do  text.txt
# use the provided binary to read next level's password
bandit26@bandit:~$ ./bandit27-do
Run a command as another user.
  Example: ./bandit27-do id
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS
```

## [Level 27 &rarr; 28](https://overthewire.org/wargames/bandit/bandit28.html)

> There is a git repository at `ssh://bandit27-git@localhost/home/bandit27-git/repo` via the port `2220`. The password for the user `bandit27-git` is the same as for the user `bandit27`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit27@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp
bandit27@bandit:~$ mkdir /tmp/lvl_27
# move the the /tmp directory
bandit27@bandit:~$ cd /tmp/lvl27
# clone the git repo
bandit27@bandit:/tmp/lvl_27$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit27/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password:
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
# list directory's contents
bandit27@bandit:/tmp/lvl_27$ ls
repo
bandit27@bandit:/tmp/lvl_27$ cd repo
bandit27@bandit:/tmp/lvl_27/repo$ ls
README
bandit27@bandit:/tmp/lvl_27/repo$ cat README
The password to the next level is: AVanL161y9rsbcJIsFHuw35rjaOM19nR
```

## [Level 28 &rarr; 29](https://overthewire.org/wargames/bandit/bandit29.html)

> There is a git repository at `ssh://bandit28-git@localhost/home/bandit28-git/repo` via the port `2220`. The password for the user `bandit28-git` is the same as for the user `bandit28`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit28@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit28@bandit:~$ mkdir /tmp/lvl_28 && cd /tmp/lvl_28
# clone the repo
bandit28@bandit:/tmp/lvl_28$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit28/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password:
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
# display file's content
bandit28@bandit:/tmp/lvl_28$ cat repo/README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
```

We can interact with this repository as it was ours and we can use all `git` commands on it. We can see the logs as follows:

```bash
# check the git's logs
bandit28@bandit:/tmp/lvl_28/repo$ git log
commit 14f754b3ba6531a2b89df6ccae6446e8969a41f3 (HEAD -> master, origin/master, origin/HEAD)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    fix info leak

commit f08b9cc63fa1a4602fb065257633c2dae6e5651b
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    add missing data

commit a645bcc508c63f081234911d2f631f87cf469258
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    initial commit of README.md
```

From the above output we notice the following:
1. The first commit was the creation of the `README.md` file.
2. The second one has as comment "*add missing data*" so this is when `Morla` probably wrote the credentials.
3. The thild and last commit has as comment "*fix info leak*" which is problably when the plaintext password was changed to its current form, i.e., `xxxxxxxxxx`.

So we can find the second commit and get the plaintext password:

```bash
# show the defined commit
bandit28@bandit:/tmp/lvl_28/repo$ git show f08b9cc63fa1a4602fb065257633c2dae6e5651b
commit f08b9cc63fa1a4602fb065257633c2dae6e5651b
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Oct 5 06:19:41 2023 +0000

    add missing data

diff --git a/README.md b/README.md
index 7ba2d2f..b302105 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials

 - username: bandit29
-- password: <TBD>
+- password: tQKvmcwNYcFS6vmPHIUSI3ShmsrQZK8S
```

## [Level 29 &rarr; 30](https://overthewire.org/wargames/bandit/bandit30.html)

> There is a git repository at `ssh://bandit29-git@localhost/home/bandit29-git/repo` via the port `2220`. The password for the user `bandit29-git` is the same as for the user `bandit29`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit29@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit29@bandit:~$ mkdir /tmp/lvl_29 && cd /tmp/lvl_29
# clone the repo
bandit29@bandit:/tmp/lvl_29$ git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit29/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
# display the file's contents
bandit29@bandit:/tmp/lvl_29$ cat repo/README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>
```

We can repeat the process of the previous level to see what we can find:

```bash
# check logs
bandit29@bandit:/tmp/lvl_29$ cd repo && git log
commit 4364630b3b27c92aff7b36de7bb6ed2d30b60f88 (HEAD -> master, origin/master, origin/HEAD)
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:43 2023 +0000

    fix username

commit fca34ddb7d1ff1f78df36538252aea650b0b040d
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Oct 5 06:19:43 2023 +0000

    initial commit of README.md
```

After checking both logs, it does not seem that they include anything of interest. The `README.md` file mentioned "*no password in production!*" which suggests that there might be more than one branch, a development one and a production one. We can list all branches as follows:

```bash
# list branches
bandit29@bandit:/tmp/lvl_29/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

There is indeed a development branch (`dev`), so we can switch to it and check what's in there:

```bash
# switch to the dev branch
bandit29@bandit:/tmp/lvl_29/repo$ git checkout dev
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
Switched to a new branch 'dev'
# check directory's contents
bandit29@bandit:/tmp/lvl_29/repo$ ls -la
total 20
drwxrwxr-x 4 bandit29 bandit29 4096 Jan  5 09:35 .
drwxrwxr-x 3 bandit29 bandit29 4096 Jan  5 09:27 ..
drwxrwxr-x 2 bandit29 bandit29 4096 Jan  5 09:35 code
drwxrwxr-x 8 bandit29 bandit29 4096 Jan  5 09:35 .git
-rw-rw-r-- 1 bandit29 bandit29  134 Jan  5 09:35 README.md
# display file's contents
bandit29@bandit:/tmp/lvl_29/repo$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: xbhV3HpNGlTIdnjUrdAlPzc2L6y9EOnS
```

## [Level 30 &rarr; 31](https://overthewire.org/wargames/bandit/bandit31.html)

> There is a git repository at `ssh://bandit30-git@localhost/home/bandit30-git/repo` via the port `2220`. The password for the user `bandit30-git` is the same as for the user `bandit30`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit30@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit29@bandit:~$ mkdir /tmp/lvl_30 && cd /tmp/lvl_30
# clone the repo
bandit29@bandit:/tmp/lvl_29$ git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit29/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password:
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
# display the file's contents
bandit30@bandit:/tmp/lvl_30$ cat repo/README.md
just an epmty file... muahaha
```

Like most VCSs, Git has the ability to **tag** specific points in a repository’s history as being important. Typically, people use this functionality to mark release points (v1.0, v2.0 and so on).

> [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)

```bash
# check the current tags
bandit30@bandit:/tmp/lvl_30/repo$ git tag
secret
# show the tag's content
bandit30@bandit:/tmp/lvl_30/repo$ git show secret
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt
```

## [Level 31 &rarr; 32](https://overthewire.org/wargames/bandit/bandit32.html)

> There is a git repository at `ssh://bandit31-git@localhost/home/bandit31-git/repo` via the port `2220`. The password for the user `bandit31-git` is the same as for the user `bandit31`. Clone the repository and find the password for the next level.

```bash
$ ssh bandit31@bandit.labs.overthewire.org -p 2220

# create a new directory within /tmp and move into it
bandit31@bandit:~$ mkdir /tmp/lvl_31 && cd /tmp/lvl_31
# clone the repo
bandit31@bandit:/tmp/lvl_31$ git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
Cloning into 'repo'...
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _
                        | |__   __ _ _ __   __| (_) |_
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_
                        |_.__/ \__,_|_| |_|\__,_|_|\__|


                      This is an OverTheWire game server.
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password:
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
# display file's content
bandit31@bandit:/tmp/lvl_31$ cat repo/README.md
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

According to the `README.md` file, we will need to create a file meetings the required specifications and then push it to the repo. 

```bash
# create the file
bandit31@bandit:/tmp/lvl_31/repo$ echo "May I come in?" > key.txt
# check that the file is created
bandit31@bandit:/tmp/lvl_31/repo$ ls -la
total 24
drwxrwxr-x 3 bandit31 bandit31 4096 Jan  6 21:35 .
drwxrwxr-x 3 bandit31 bandit31 4096 Jan  6 21:33 ..
drwxrwxr-x 8 bandit31 bandit31 4096 Jan  6 21:38 .git
-rw-rw-r-- 1 bandit31 bandit31    6 Jan  6 21:33 .gitignore
-rw-rw-r-- 1 bandit31 bandit31   15 Jan  6 21:35 key.txt
-rw-rw-r-- 1 bandit31 bandit31  147 Jan  6 21:33 README.md
# display file's content
bandit31@bandit:/tmp/lvl_31/repo$ cat key.txt
May I come in?
```

The sequence for pushing a file to a Git repo is:
1. Record changes to the repo via [`git commit`](https://git-scm.com/docs/git-commit).
2. Update remote refs along with associated object via [`git push`](https://git-scm.com/docs/git-push).

Before doing that, we can see that there is a [`.gitignore`](https://git-scm.com/docs/gitignore) file in our directory:

```bash
# display file's content
bandit31@bandit:/tmp/lvl_31/repo$ cat .gitignore
*.txt
```

`.gitignore` specifies intentionally untracked files to ignore. In this case, it ignores all `.txt` files (`*.txt`). So trying to go over the above 2-step sequence won't work in this case.

To add the file anyway we can use [`git add`](https://git-scm.com/docs/git-add), which add file contents to the index, before using `git commit`:

```bash
# add file contents to the index
bandit31@bandit:/tmp/lvl_31/repo$ git add -f key.txt
# record the changes to the repo
bandit31@bandit:/tmp/lvl_31/repo$ git commit -a
Unable to create directory /home/bandit31/.local/share/nano/: No such file or directory
It is required for saving/loading search history or cursor positions.

[master 625a650] A random message!
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
# update remote refs
bandit31@bandit:/tmp/lvl_31/repo$ git push
<SNIP>
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 327 bytes | 327.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: rmCBvG56y58BXzv98yZGdO7ATVL5dW8y
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo'
```

## [Level 32 &rarr; 33](https://overthewire.org/wargames/bandit/bandit33.html)

> After all this git stuff its time for another escape. Good luck!

```bash
$ ssh bandit32@bandit.labs.overthewire.org -p 2220
WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: Permission denied
```

It seems that everything we type is automatically converted to uppercase! All the Linux commands are lowercase, so we can't really pass any command. But we can use [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/) which, by convention, have uppercase names.

More specifically, there is the [`$0`](https://linuxhandbook.com/bash-dollar-0/) special variable which can be used in two ways:
1. To find the logged-in shell.
2. To print the name of the script that is being executed.

We are interested in the first use!

```bash
# drop into the logged-in shell
>> $0
# read the password
$ cat /etc/bandit_pass/bandit33
odHo63fHiFqcWWJG9rLiLDtPm45KzUKy
```

## [Level 32 &rarr; 33](https://overthewire.org/wargames/bandit/bandit33.html)

> At this moment, level 34 does not exist yet.

```bash
$ ssh bandit33@bandit.labs.overthewire.org -p 2220

# list directory's files
bandit33@bandit:~$ ls
README.txt
# display file's content
bandit33@bandit:~$ cat README.txt
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game. However, we are constantly working
on new levels and will most likely expand this game with more levels soon.
Keep an eye out for an announcement on our usual communication channels!
In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
```