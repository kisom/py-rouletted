#!/usr/bin/env python

# IN CASE OF SKYNET:
# note (and this may be important): there is a signal handler for SIGUSR1 to kill
# the daemon. this is how you prevent skynet from taking over.

# license: public domain
# disclaimer: in case you are from a culture that is not familiar with the concept of
# russian roulette, I strongly recommend you delete this code and familiarise yourself
# with the 'game'. 
#
# DISCLAIMER: this will (most-likely) cause order and respect among your user base,
# especially when the script starts killing off problem children. however, your 
# kingdom / server is yours to run, and not my problem. this is released under the
# ISC license. the LICENSE file should have been distributed with this software. read
# it.

import os
import random
import subprocess
import sys
import time

# global options
full_chamber = True             # set to false if you want to load only one bullet, aka
                                # every time this wakes up, there is a 1 / 6 chance a 
                                # user will be killed
debug    = False
safelist = [ 'kisom' ]          # users not to kill
problem_children = None         # user list to serve as the pool
minwait  = 30;                  # one hour minimum between cylinder spinning
maxwait  = 90;                  # one day maximum between cylinder spinning

def die_handler(signum, frame):
    die('received signal %d' % signal)

def die(errstr):
    if errstr:
        sys.stderr.write("%s\n" % errstr)
    sys.exit(1)

# uses who and uniq to grab a unique user list. optionally, pass in a list of sysadmins
# to not kill. note this only kills users logged in interactively, which is the point
# of this little game.
def get_random_user(exclude_list = None):

    # lteo requested the ability to narrow down the kill pool; if the problem_children
    # list is not None, our userlist is the list of problem_children
    if problem_children:
        userlist = problem_children[:]
    # if there isn't a problem_children list select from the list of logged in users
    else:
        command = "who | awk '{ print $1 }' | uniq | xargs" 
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        userlist = p.communicate()[0].split()

    # filter the list of users
    # if there is a safe list, remove any entries from that list
    if exclude_list:
        userlist = [ user for user in userlist if user and not user in exclude_list ]
    # remove blank entries (the above case will remove blank entries as well)
    else:
        userlist = [ user for user in userlist if user ] # remove blank entries

    # fail on an empty user list
    if not userlist:
        err = 'empty user list...'        
        if exclude_list:
            err += ' maybe try making the safe list a little less... safe?'

        # all user-based functions should expect to receive at some time the user
        # None (for the case of a partially-filled chamber) so this should not 
        # cause an error. just means we need to lurk and wait... to KILLLLL
        if debug: die(err)
        else: return None

    if full_chamber:
        return random.choice(userlist)
    else:
        # code me!
        return None

# if you don't pass in a user as a string, you get whatever is coming to you
def get_user_process_list(user = None):
    if not user:
        die('try passing a user?')

    command = 'pgrep -U %s | xargs' % user

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    proclist = p.communicate()[0].strip()

    return proclist

# give it a user and let 'er rip!
def pull_the_trigger(user = None):
    if not user:
        print "lucked out!"
        return False

    proclist = get_user_process_list(user)
    command = 'kill -9 %s' % (proclist, )

    print command

    p = subprocess.Popen(command, shell=True)
    retval = os.waitpid(p.pid, 0)[1]            # get return code

    if retval:
        print "pkill returned %d..." % retval
    else:
        print "%s was killed!" % user

# here we go!
def spin_the_cylinder(exclude_list):
    pull_the_trigger(get_random_user(exclude_list)) 

def daemonise():
    # taken from http://code.activestate.com/recipes/66012/ because it was faster
    # than rewriting the code I've done in C a million times

    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)

    except OSError, e: 
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit from second parent, print eventual PID before
            print "Daemon PID %d" % pid 
            sys.exit(0) 
    except OSError, e: 
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

    # set signal handlers
    signal.signal(signal.SIGUSER1, die_handler)

    # start the daemon main loop
    main() 


def main():
    while True:
        delay = random.randrange(minwait, maxwait)
        print "sleep for %d seconds..." % delay
        time.sleep(delay)
        spin_the_cylinder(safelist)



if __name__ == '__main__':
    daemonise()
