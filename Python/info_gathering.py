#!/bin/python
# -*- coding: ISO-8859-1 -*- 

#. Description:     Tool to automatize information gathering step

#. Pense-bête : Il faudra rajouter une option d'update pour la recherche d'exploit

import os, sys, os.path, apt, socket, re

##Définitions des variables
scriptname = sys.argv[0]
cache = apt.Cache()
prerequisites = "/tmp/prerequisites.txt"
services = ["ssh", "http", "https", "ftp", "smtp", "pop3", "imap"]
ports = ["21/", "22/", "23/", "25/", "80/", "465/", "587/", "3306/", "8080/"] #On rajoute le '/' à la fin à cause du formatage de l'output de Nmap
soft_versions = "/tmp/soft_versions.txt"
tmp1 = "/tmp/tmp1"
yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])


##Usage function
def usage ():
    print ("This is the list of available options:")
    print ("\t -t : Set the target domain name")
    print ("\t -p : Set a person name \n")
    print ("\t Example : python "+scriptname+" -h example.com")

##Check if necessary packages are installed
def check_package():
    ##On définit une liste des paquets requis pour le script
    file = open(prerequisites, 'wb')
    file.write("nikto\ntor\nproxychains\nnmap")
    file.close()
    
    ##On check si chacun d'eux est installé
    with open(prerequisites, 'r') as f:
        for line in f:
            line = line.rstrip('\n') ##Faire en sorte d'enlever les \n en trop
            if cache[line].is_installed: 
                print (line+" :[OK]")
            else:
                os.system('which'+line)
                test_dpkg = os.system('echo $?')
                if test_dpkg == "1":
                    print (line+" is not installed. Do you want the script to install it for you ? [Y/n]")
                    choice = raw_input().lower()
                    if choice in yes:
                        os.system('apt-get install -y '+line)
                    else:
                        print ("The script won't work without the "+line+"package")
                else:
                    print (line+" :[OK]")
def scan_target():
    target = sys.argv[2]
    ##Error handling for NX domains##
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print ("The target does not exist")
        sys.exit()
        
    path = os.getenv("HOME")
    os.chdir(path)
    try:
        os.mkdir(target)
    except OSError:
        print ("The directory"+target+" exists. Try again")
        sys.exit()
    
    #Target results in a specific directory

    scan_directory = (path+'/'+target+'/')
    print ("Do you want to proxychains the target scan ? [Y/n]")
    choice = raw_input().lower()
    if choice in yes:
        nmap_scan = os.system('proxychains nmap -A -T4 -sV '+target_ip+' -oA '+scan_directory+'nmap_scan')
    else:
        nmap_scan = os.system('nmap -A -T4 -sV '+target_ip+' -oA '+scan_directory+'nmap_scan')
    #result = subprocess.check_output(nmap_scan, shell=True)

def exploits_search():
    #Must grep nmap output and search for possible exploits through the web ##Exploit search https://github.com/rfunix/Pompem
    foobar = open(soft_versions,"wb")
    for i in range(len(ports)):
        #print services[i]
        for line in open("/root/serv_pulido.nmap", 'r'):
            if ports[i] in line:
                print (line)

    foobar.close()

    os.system('cat '+soft_versions+' | awk \'{print $4 " " $5}\' > '+tmp1)
    ''' 
    with open(tmp1, 'r') as foo:
        for line in foo:
            if line =="":
                print ("the variable must be empty")
            else:
                print ("the variable is not empty")
    '''

def main_prog():
    for arg in sys.argv:
        if arg == "-t":
            #scan_target()
            exploits_search()
        if len(sys.argv) == 1:
            usage()

print ("===== Prerequisites =====\n")
check_package()
print ("==========================\n")
main_prog()


