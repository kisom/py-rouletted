import random
import subprocess
import sys

# global options
full_chamber = True         # set to false if you want to load only one bullet, aka
                            # every time this wakes up, there is a 1 / 6 chance a 
                            # user will be killed


def die(errstr):
    if errstr:
        sys.stderr.write("%s\n" % errstr)
    sys.exit(1)

# uses who and uniq to grab a unique user list. optionally, pass in a list of sysadmins
# to not kill. note this only kills users logged in interactively, which is the point
# of this little game.
def get_random_user(exclude_list = None):
    command = "who | awk '{ print $1 }' | uniq | xargs" 

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    userlist = p.communicate()[0].split()

    if exclude_list:
        userlist = [ user for user in userlist if user and not user in exclude_list ]
    else:
        userlist = [ user for user in userlist if user ] # remove blank entries

    if not userlist:
        err = 'empty user list...'        
        if exclude_list:
            err += ' maybe try making the safe list a little less... safe?'

        die(err)

    if full_chamber:
        return random.choice(userlist)
    else:
        # code me!
        return None

# if you don't pass in a user as a string, you get whatever is coming to you
def get_user_process_list(user = None):
    if not user:
        die('try passing a user?')

    cmd = 'pgrep -U %s | xargs' % user

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    proclist = p.communicate()[0].strip()

    return proclist

# give it a user and let 'er rip!
def kill_users_procs(user = None):
    if not user:
        die('you probably shouldn\'t be running this...')

    proclist = get_user_process_list(user)
    p = subprocess.Popen(command, shell=True)
    retval = os.waitpid(p.pid, 0)[1]            # get return code

    if retval:
        print "pkill returned $d..." % retval
    else:
        print "%s was killed!" % user

# here we go!
def spin_the_cylinder(exclude_list):
    kill_users_procs(user) 

print get_random_user(['kisom'])



