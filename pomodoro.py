###########################################
## Application: Pomodoro
## Author: ss-is-master-chief (Sumit Saha)
## Email: sumit.saha666@gmail.com
## Year: 2020
## Version: 0.1
###########################################
#!/usr/bin/python3

import time 
from datetime import datetime
import argparse
import os
import re
import sys

BANNER = '''
  ____                           _                 
 |  _ \ ___  _ __ ___   ___   __| | ___  _ __ ___  
 | |_) / _ \| '_ ` _ \ / _ \ / _` |/ _ \| '__/ _ \ 
 |  __/ (_) | | | | | | (_) | (_| | (_) | | | (_) |
 |_|   \___/|_| |_| |_|\___/ \__,_|\___/|_|  \___/ 
                                
'''

parser = argparse.ArgumentParser(
    description='Simple Pomodoro Timer for procrastinators')

parser.add_argument(
    '-s',
    default="PomoSession",
    type=str,
    help='the name of session (default: PomoSession)')

parser.add_argument(
    '-sd',
    default=25,
    type=int,
    help='duration of session in mins (default: 25 mins)')

parser.add_argument(
    '-bd',
    default=5,
    type=int,
    help='duration of break in mins (default: 5 mins)')

args = parser.parse_args()

class Pomodoro:
    def __init__(self):
        self.count = 0
        self.restart = "y"
        
        print(BANNER)
        print(f'''🕑 Default working session length: {args.sd} mins''')
        print(f'''🕑 Default break session length: {args.bd} mins''')
        self.restart = input("☕ Start? [y/n]: ").lower()
        self.check_restart()

    def countdown(self, t, session_type): 
        if session_type=="work_session":
            prefix = f'''⏳ Working Session {self.count+1}: '''
        else:
            prefix = f'''⏳ Break Session {self.count+1}: '''
        
        # t = t*60
        
        while t: 
            mins, secs = divmod(t, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(prefix, timer, end="\r") 
            time.sleep(1) 
            t -= 1

        print(" "*(len(prefix)+len(timer)+10), end="\r")
        
    def work_session(self):
        self.countdown(args.sd, "work_session")
        print(f'''✅ Working Session {self.count+1}: {args.sd} mins''')
        os.system(f'''say "Session {self.count+1} is complete, take a break." -r 250''')

    def break_session(self):
        self.countdown(args.bd, "break_session")
        print(f'''✅ Break Session {self.count+1}: {args.bd} mins''')
        os.system(f'''say "Let's get back to work" -r 250''')
        self.count += 1

    def check_restart(self):
        while self.restart=="y":
            self.work_session()
            self.break_session()
            self.restart = input("☕ Start? [y/n]: ").lower()
        if self.restart=="n":
            exit_app = input("Exit? [y/n]: ")
            if exit_app=="y":
                sys.exit()
            else:
                self.restart = input("Start? [y/n]: ").lower()
                self.check_restart()

    def log_session(self):
        pass

if __name__=="__main__":
    os.system('clear')
    Pomodoro()

# # function call 
# session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# countdown(args.sd)
# session_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")