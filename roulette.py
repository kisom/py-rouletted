import subprocess

def get_random_user(exclude_list):
    command = "who | awk '{ print $1 }' | uniq" 

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

