import subprocess

def get_random_user(exclude_list):
    command = "who | awk '{ print $1 }' | uniq" 
