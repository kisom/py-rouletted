import random
import subprocess
import sys


# uses who and uniq to grab a unique user list. optionally, pass in a list of sysadmins
# to not kill. note this only kills users logged in interactively, which is the point
# of this little game.
def get_random_user(exclude_list = None):
    command = "who | awk '{ print $1 }' | uniq" 

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    userlist = p.communicate()[0].split()

    if exclude_list:
        userlist = [ user for user in userlist if user and not user in exclude_list ]
    else:
        userlist = [ user for user in userlist if user ] # remove blank entries

    if not userlist:
        sys.stderr.write('empty user list...')        
        if exclude_list:
            sys.stderr.write(' maybe try making the safe list a little less... safe?')
        sys.stderr.write('\n');
        sys.exit(1)

    return random.choice(userlist)

print get_random_user(['kisom'])

