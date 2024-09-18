#!/usr/bin/python
#
# quick script for installing NetShield
#

import time
import subprocess
import os
import shutil
from src.core import *
import sys
import errno
import argparse
from src.pyuac import * 
try: input = input
except NameError: pass

import src.globals

# Argument parse. Aimed to provide automatic deployment options
interactive = True # Flag to select interactive install, typically prompting user to answer [y/n]
parser = argparse.ArgumentParser(description='-y, optional non interactive install/uninstall with automatic \'yes\' selection. It must roon with root/admin privileges')
parser.add_argument("-y", action='store_true')
args = parser.parse_args()
if args.y: # Check if non-interactive install argument is provided using an apt parameter style, -y
    print("Running in non interactive mode with automatic \'yes\' selection")
    interactive = False;

# Check to see if we are admin
if is_windows():
    if not isUserAdmin():
        runAsAdmin()# will try to relaunch script as admin will prompt for user\pass and open in seperate window
        sys.exit(1)
    if isUserAdmin():
        print('''
Welcome to the  installer. NetShield is a honeypot, file monitoring, and overall security tool used to protect your nix systems.

Written by: Dave Kennedy (ReL1K)
''')
#create loop for install/uninstall not perfect but works saves answer for next step
    if not os.path.isfile("C:\\Program Files (x86)\\NetShield\\NetShield.py"):
        if interactive:
            answer = input("[*] Do you want to install NetShield [y/n]: ")
        else:
            answer = 'y'
    #if above is false it must be installed so ask to uninstall
    else:
        if os.path.isfile("C:\\Program Files (x86)\\NetShield\\NetShield.py") and interactive:
            #print("[*] [*] If you would like to uninstall hit y then enter")
            answer = input("[*] NetShield detected. Do you want to uninstall [y/n:] ")
        else:
            answer = 'y'
        #put this here to create loop
        if (answer.lower() in ["yes", "y"]) or not interactive:
            answer = "uninstall"

# Check to see if we are root
if is_posix():
    try:   # and delete folder
        if os.path.isdir("/var/NetShield_check_root"):
            os.rmdir('/var/NetShield_check_root')
            #if not thow error and quit
    except OSError as e:
        if (e.errno == errno.EACCES or e.errno == errno.EPERM):
            print ("You must be root to run this script!\r\n")
        sys.exit(1)
    print('''
Welcome to the NetShield installer. NetShield is a honeypot, file monitoring, and overall security tool used to protect your nix systems.

Written by: Dave Kennedy (ReL1K)
''')
#if we are root create loop for install/uninstall not perfect but works saves answer for next step
    if not os.path.isfile("/etc/init.d/NetShield"):
        if interactive:
            answer = input("Do you want to install NetShield and have it automatically run when you restart [y/n]: ")
        else:
            answer = 'y'
    #if above is true it must be installed so ask to uninstall
    else:
        if os.path.isfile("/etc/init.d/NetShield") and interactive:
            answer = input("[*] NetShield detected. Do you want to uninstall [y/n:] ")
        else:
            answer = 'y'
        #put this here to create loop
        if (answer.lower() in ["yes", "y"]) or not interactive:
            answer = "uninstall"

if answer.lower() in ["yes", "y"]:
    init_globals()
    if is_posix():
        #kill_NetShield()

        print("[*] Beginning installation. This should only take a moment.")

        # if directories aren't there then create them
        #make root check folder here. Only root should
        #be able to create or delete this folder right?
        # leave folder for future installs/uninstall?
        if not os.path.isdir("/var/NetShield_check_root"):
            os.makedirs("/var/NetShield_check_root")
        if not os.path.isdir("/var/NetShield/database"):
            os.makedirs("/var/NetShield/database")
        if not os.path.isdir("/var/NetShield/src/program_junk"):
            os.makedirs("/var/NetShield/src/program_junk")

        # install to rc.local
        print("[*] Adding NetShield into startup through init scripts..")
        if os.path.isdir("/etc/init.d"):
            if not os.path.isfile("/etc/init.d/NetShield"):
                fileopen = open("src/startup_NetShield", "r")
                config = fileopen.read()
                filewrite = open("/etc/init.d/NetShield", "w")
                filewrite.write(config)
                filewrite.close()
                print("[*] Triggering update-rc.d on NetShield to automatic start...")
                subprocess.Popen(
                    "chmod +x /etc/init.d/NetShield", shell=True).wait()
                subprocess.Popen(
                    "update-rc.d NetShield defaults", shell=True).wait()

            # remove old method if installed previously
            if os.path.isfile("/etc/init.d/rc.local"):
                fileopen = open("/etc/init.d/rc.local", "r")
                data = fileopen.read()
                data = data.replace(
                    "sudo python /var/NetShield/NetShield.py &", "")
                filewrite = open("/etc/init.d/rc.local", "w")
                filewrite.write(data)
                filewrite.close()
    #Changed order of cmds. was giving error about file already exists.
    #also updated location to be the same accross all versions of Windows
    if is_windows():
        program_files = os.environ["PROGRAMFILES(X86)"]
        install_path = os.getcwd()
        shutil.copytree(install_path, program_files + "\\NetShield\\")
        os.makedirs(program_files + "\\NetShield\\logs")
        os.makedirs(program_files + "\\NetShield\\database")
        os.makedirs(program_files + "\\NetShield\\src\\program_junk")


    if is_posix():
        if interactive:
            choice = input("[*] Do you want to keep NetShield updated? (requires internet) [y/n]: ")
        else:
            choice = 'y'
        if choice in ["y", "yes"]:
            print("[*] Checking out NetShield through github to /var/NetShield")
            # if old files are there
            if os.path.isdir("/var/NetShield/"):
                shutil.rmtree('/var/NetShield')
            subprocess.Popen(
                "git clone https://github.com/binarydefense/NetShield /var/NetShield/", shell=True).wait()
            print("[*] Finished. If you want to update NetShield go to /var/NetShield and type 'git pull'")
        else:
            print("[*] Copying setup files over...")
            subprocess.Popen("cp -rf * /var/NetShield/", shell=True).wait()

        # if os is Mac Os X than create a .plist daemon - changes added by
        # contributor - Giulio Bortot
        if os.path.isdir("/Library/LaunchDaemons"):
            # check if file is already in place
            if not os.path.isfile("/Library/LaunchDaemons/com.NetShield.plist"):
                print("[*] Creating com.NetShield.plist in your Daemons directory")
                filewrite = open(
                    "/Library/LaunchDaemons/com.NetShield.plist", "w")
                filewrite.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n<key>Disabled</key>\n<false/>\n<key>ProgramArguments</key>\n<array>\n<string>/usr/bin/python</string>\n<string>/var/NetShield/NetShield.py</string>\n</array>\n<key>KeepAlive</key>\n<true/>\n<key>RunAtLoad</key>\n<true/>\n<key>Label</key>\n<string>com.NetShield</string>\n<key>Debug</key>\n<true/>\n</dict>\n</plist>')
                print("[*] Adding right permissions")
                subprocess.Popen(
                    "chown root:wheel /Library/LaunchDaemons/com.NetShield.plist", shell=True).wait()

    check_config()
    if interactive:
        choice = input("[*] Would you like to start NetShield now? [y/n]: ")
    else:
        choice = 'y'
    if choice in ["yes", "y"]:
        if is_posix():
            # this cmd is what they were refering to as "no longer supported"? from update-rc.d on install.
            # It looks like service starts but you have to manually launch NetShield
            subprocess.Popen("/etc/init.d/NetShield start", shell=True).wait()
            print("[*] Installation complete. Edit /var/NetShield/config in order to config NetShield to your liking")
        #added to start after install.launches in seperate window
        if is_windows():
            os.chdir("src\windows")
            #copy over banlist
            os.system("start cmd /K banlist.bat")
            #Wait to make sure banlist is copied over
            time.sleep(2)
            #launch from install dir
            os.system("start cmd /K launch.bat")
            #cleanup cache folder
            time.sleep(2)
            os.system("start cmd /K del_cache.bat")


#added root check to uninstall for linux
if answer == "uninstall":
    if is_posix():
        try:   #check if the user is root
            if os.path.isdir("/var/NetShield_check_root"):
                os.rmdir('/var/NetShield_check_root')
               #if not throw an error and quit
        except OSError as e:
            if (e.errno == errno.EACCES or e.errno == errno.EPERM):
                print ("[*] You must be root to run this script!\r\n")
            sys.exit(1)
        else:# remove all of NetShield
            os.remove("/etc/init.d/NetShield")
            subprocess.Popen("rm -rf /var/NetShield", shell=True)
            subprocess.Popen("rm -rf /etc/init.d/NetShield", shell=True)
            #added to remove service files on kali2
            #subprocess.Popen("rm /lib/systemd/system/NetShield.service", shell=True)
            #kill_NetShield()
            print("[*] NetShield has been uninstalled. Manually kill the process if it is still running.")
    #Delete routine to remove NetShield on windows.added uac check
    if is_windows():
        if not isUserAdmin():
            runAsAdmin()
        if isUserAdmin():
            #remove program files
            subprocess.call(['cmd', '/C', 'rmdir', '/S', '/Q', 'C:\\Program Files (x86)\\NetShield'])
            #del uninstall cache
            os.chdir("src\windows")
            os.system("start cmd /K del_cache.bat")
            #just so they can see this message slleep a sec
            print("[*] NetShield has been uninstalled.\n[*] Manually kill the process if it is still running.")
            time.sleep(3)
