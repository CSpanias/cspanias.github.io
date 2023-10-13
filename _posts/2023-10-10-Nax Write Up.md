---
title: Nax CTF Write Up
date: 2023-10-10
categories: [CTF Write Up, THM]
tags: [nmap, piet, ascii, nikto, nagiosxi, metasploit]
img_path: /assets/nax/
mermaid: true
---
![nax_room_banner](nax_banner.png)

## 1 Process Summary

[![](https://mermaid.ink/img/pako:eNpNksFq20AQhl9l2V4UiFPHJXHQIaBIChVtbSPJ0MBettqRvFiaFasVdbH9Irn03LfrI3QkN0GX5Wf_b5Z_ZvbIC6OA-7yszc9iJ61jX1OBAotadl0EJbOgWOes2YP_oZzP2cT6Uffw7s3n5VCn1a0XY9-AlU4bvPJ9f8AGY-FtwGqjdMHiGhpA1wlM0EEFllSQhUky5e-8bPsUJWkc5us0iTOBHzUqONy0u5Y0ykqb7qCHEgo5VNx7n5MoilfsreqFuE3yKb_ZrKoJt_SCPA_CLyzbps9BGAtcjY-x7wkriOkm7IOXrtc5C8IwzigC-_v79c94vDNj07OZocT_5ezxhI2kkKj3zgg8UfMXbjFy92NY4syp0g1xrQZH0PICLUenASe7tjZ6cB4E8mtOU22kVrSuIyVhgrsdzVFwn6SSdi-4wDNxsncm-4UF953t4Zr3rZIOIi0rKxvul7Lu6BaUdsZ-u-x__Abnf9IItjU?type=png)](https://mermaid.live/edit#pako:eNpNksFq20AQhl9l2V4UiFPHJXHQIaBIChVtbSPJ0MBettqRvFiaFasVdbH9Irn03LfrI3QkN0GX5Wf_b5Z_ZvbIC6OA-7yszc9iJ61jX1OBAotadl0EJbOgWOes2YP_oZzP2cT6Uffw7s3n5VCn1a0XY9-AlU4bvPJ9f8AGY-FtwGqjdMHiGhpA1wlM0EEFllSQhUky5e-8bPsUJWkc5us0iTOBHzUqONy0u5Y0ykqb7qCHEgo5VNx7n5MoilfsreqFuE3yKb_ZrKoJt_SCPA_CLyzbps9BGAtcjY-x7wkriOkm7IOXrtc5C8IwzigC-_v79c94vDNj07OZocT_5ezxhI2kkKj3zgg8UfMXbjFy92NY4syp0g1xrQZH0PICLUenASe7tjZ6cB4E8mtOU22kVrSuIyVhgrsdzVFwn6SSdi-4wDNxsncm-4UF953t4Zr3rZIOIi0rKxvul7Lu6BaUdsZ-u-x__Abnf9IItjU)

## 2 Background Information

The [Nax room](https://tryhackme.com/room/nax) is the second **medium rated difficulty** room of the Starter Series ([**Dogcat**](https://cspanias.github.io/posts/Dogcat-Write-Up-(2023)/) was the first). 

Working through this felt like a game of [Cluedo](https://en.wikipedia.org/wiki/Cluedo), in a sense that it did not require much pentest tooling usage, but mostly searching constantly for clues. Having said that, I did enjoy working on this room, as I learned a lot of new things such as the **Nagios XI** monitoring tool, some **chemistry**, and the abstract artist **Piet Mondrian**.

With the exception of **Nagios XI**, doesn't sound a lot like a THM CTF challenge, does it?

![piet_artist](piet_artist.png){: width:"40%" height:"40%"}

Reading the room's description:

>_Identify the critical **security flaw in the most powerful and trusted network monitoring software on the market**, that allows an authenticated user to perform **remote code execution**._

and pairing that with the room's note saying that it requires **Metasploit 6**, we can safely assume that we will need to **find a Nagios XI exploit on Metasploit that allows us to perform RCE**. 

That sounds like a pretty straightforward thing to do, but believe me when I say that it's not!

### 2.1 Nagios XI

I encountered **Nagios XI** for the first time, and as a result, I did a bit of reading about it. It seems that [Nagios XI](https://www.edureka.co/blog/nagios-tutorial/) is a tool used mostly in DevOps for continous monitoring of systems, applications, etc. 

In brief, I think of it as a **[boosted crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)**: it periodically runs scripts which can be reached from a command line or a GUI. When something goes wrong, it will generate an alert in the form of an email or SMS, which helps developers start working on the issue right away, before it has any negative impact on the business productivity.

![nagios_graph](Nagios-Working-nagios-Tutorial-Edureka-3.png){: width:"80%" height:"80%"}

### 2.2 The Piet Programming Language

Quoting from [DangerMouse.net](https://www.dangermouse.net/esoteric/piet.html):
>_**Piet** is a programming language in which programs look like abstract paintings. The language is named after **Piet Mondrian**, who pioneered the field of **geometric abstract art**._

Although it would have been nice, we don't have to make any kind of abstract painting ourselves for this room, but just perform some simple enough steps with the **Piet language**.

Armed with the knowledge of what **Nagios XI** is, **Piet's programming language** existence, and the fact that we probably need to **find an exploit within Metasploit to perform RCE**, we are ready to crack on 🏃 !

## 3 CTF Process

### 3.1. Enumeration with nmap and nikto

As always, we can start with an **nmap port-scan**:

![nmap-scan](nmap-scan.png){: width:"60%" height:"60%"}

There is a **web server at port 80**, so let's pay it a visit through our browser:

![homepage](homepage.png){: width:"60%" height:"60%"}

We can **search for subdirectories** to see if we can find anything interesting:

![nikto_scan](nikto.png)

Nikto found multiple index files: `index.php` and `index.html`. Upon visiting the former directory, we can see a Nagiox XI button which redirect us to `/nagiosxi`:

![nagiosxi_dir](nagiosxi_dir.png)

Unfortunately, we don't have any credentials to use yet!

### 3.2 The Periodic Table of Elements & ASCII Characters

Here is where the fun begins! Along with some abstract art, there is a list with some chemical elements on the homepage:  `Ag - Hg - Ta - Sb - Po - Pd - Hg - Pt - Lr`. 

The only thing I remember from high school chemistry is something called the [periodic table](https://en.wikipedia.org/wiki/Periodic_table) which, according to [Wikipedia](https://en.wikipedia.org/wiki/Periodic_table):
>_is a depiction of the periodic law, which says that when **the elements are arranged in order of their atomic numbers** an approximate recurrence of their properties is evident._

![Periodic_table](https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Colour_18-col_PT_with_labels.png/1920px-Colour_18-col_PT_with_labels.png){: width:"60%" height="60%" .w77 .normal}

As a result, we can use the [Interactive Periodic Table of Elements](https://www.fishersci.co.uk/gb/en/periodic-table.html) to convert each listed element to its atomic number, and by doing this we obtain the following number sequence: `47 80 73 51 84 46 80 78 103`.

![interactive_periodic_table](interactive_periodic_table.jpg){: width:"60%" height:"60%"}

We now need to find what this number sequence could possibly represent. The first question of the room is: "_What hidden file did you find?_". Thus, somehow, we need to link this number sequence with a file name. Who is better to ask than **Google**?

![integer_to_string](integer_to_string.png){: width:"60%" height:"60%"}

Clicking on the first link, [OnlineStringTools](https://onlinestringtools.com/convert-decimal-to-string), and putting our decimal string, we get our answer 🍻!

![online_tools](online_tools_decimal_to_ascii_1.png){: width:"60%" height:"60%"}

Visiting the `/PI3T.PNg` directory, we encounter an image with an abstract form of art. The second question asks us about the creator of this image, so we can just download it, and check its metadata to find that out.

![img_metadata](pi3t_png_dir.png){: width:"60%" height:"60%"}

```shell
# download the image locally
wget http://<target-ip>/PI3T.PNg
# view the image's metadata
exiftool PI3T.PNg
# Artist: Piet Mondrian
```
### 3.3 The Piet Programming Language

We now have an Piet-like image on our hands, that we need to process via the **Piet programming language**.

The room's author suggests converting the image by opening **gimp** and export it to `.ppm` format, so let's be proactive and do that now:

```shell
# install gimp
apt install gimp
# launch gimp
gimp
```

1. Go to `File`, then `Open`, and import our `PI3T.PNg` image.
2. Then `File`, `Export As`, and `Select File Type (By Extension)`.

![ppm_export](ppm_export.png)

There is a [Piet Online Interpreter](https://bertnase.de/npiet/npiet-execute.php) that I tried uploading the image, but as it seems that the file is too big for that. As a result, we have to install Piet on our machine by downloading the [`npiet-1.3f.tar.gz`](https://bertnase.de/npiet/) file:

```shell
# download tar file
wget https://bertnase.de/npiet/npiet-1.3f.tar.gz

# extract the tar file
tar zvfx npiet-1.3f.tar.gz

# move into the piet's directory
cd npiet-1.3f

# configure Piet
./configure
make # an error is expected, but does not matter

#launch Piet
./npiet -e 400 PI3T.ppm
# nagiosadmin%n3p3UQ&9BjLp4$7uhWdY
``` 

The `-e 400` flag on our last command defines the execution steps, which by default are unlimited. That means that if we execute it without the `-e` flag, it never completes! After a bit of trial and error, `400` steps are exactly what we need to reveal the credentials needed:

![piet_creds](creds_piet.jpg)

With a pair of valid creds we can now login on `/nagiosxi` directory 🍻 !

### 3.4 Metasploit and RCE

Browsing through the site, we notice the the current Nagios XI's version is `5.5.6`:

![nagios_version](nagios_version.png)

Searching [Exploit-DB](https://www.exploit-db.com/) for "*nagios xi 5.5.6*" we find an RCE exploit, as expected:

![exploit-db_rce](exploit_db.png)

All we have to do now, is first update (`msfupdate`) and launch Metasploit (`msfconsole`), and then search for this exploit either by its CVE number ([CVE-2019-15949](https://nvd.nist.gov/vuln/detail/CVE-2019-15949)), or by the app's name:

![metasploit](metasploit.png)

By defining the required variables and running the exploit, we should receive a meterpreter shell (press `enter` when the payload is completed):

![metasploit_payload](metasploit_payload.png)

The room's questions ask us to find `user.txt` and `root.txt` so lets just search for them:

![metasploit_flags](metasploit_flags.jpg)

Two birds with one stone 🚩 🚩 !