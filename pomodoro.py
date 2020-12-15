###########################################
## Application: Pomodoro
## Author: ss-is-master-chief (Sumit Saha)
## Email: sumit.saha666@gmail.com
## Year: 2020
## Version: 0.1
###########################################

import time
from datetime import datetime
import argparse
import os
import re
import sys
import json
import signal

BANNER = """
  ____                           _                 
 |  _ \ ___  _ __ ___   ___   __| | ___  _ __ ___  
 | |_) / _ \| '_ ` _ \ / _ \ / _` |/ _ \| '__/ _ \ 
 |  __/ (_) | | | | | | (_) | (_| | (_) | | | (_) |
 |_|   \___/|_| |_| |_|\___/ \__,_|\___/|_|  \___/ 
                                
"""

parser = argparse.ArgumentParser(
    description="Simple Pomodoro Timer for procrastinators"
)

parser.add_argument(
    "-s",
    default="PomoSession",
    type=str,
    help="the name of session (default: PomoSession)",
)

parser.add_argument(
    "-sd", default=25, type=int, help="duration of session in mins (default: 25 mins)"
)

parser.add_argument(
    "-bd", default=5, type=int, help="duration of break in mins (default: 5 mins)"
)

args = parser.parse_args()


class Pomodoro:
    def __init__(self):
        self.count = 0
        self.restart = "y"
        self.work_duration = args.sd
        self.break_duration = args.bd
        self.last_session_id = -1
        self.session_id = []
        self.session_names = []
        self.start_times = []
        self.end_times = []

        signal.signal(signal.SIGINT, self.signal_handler)

        if self.check_log_exist() == False:
            placeholder_dict = {
                "session_id": [],
                "session_names": [],
                "start_times": [],
                "end_times": [],
            }

            self.last_session_id = 0

            with open("session_log.json", "w") as f:
                json.dump(placeholder_dict, f, indent=4)

        print(BANNER)
        print(f"""🕑 Default working session length: {self.work_duration} mins""")
        print(f"""🕑 Default break session length: {self.break_duration} mins""")

        # self.command = input("> ")
        self.restart = input("☕ Start? [y/n]: ").lower()
        self.check_restart()

    def countdown(self, t, session_type):
        if session_type == "work_session":
            prefix = f"""⏳ Working Session {self.count+1}: """
        else:
            prefix = f"""⏳ Break Session {self.count+1}: """

        t = t * 60

        while t:
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(prefix, timer, end="\r")
            time.sleep(1)
            t -= 1

        print(" " * (len(prefix) + len(timer) + 10), end="\r")

    def work_session(self):

        self.start_times.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.countdown(self.work_duration, "work_session")
        self.end_times.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"""✅ Working Session {self.count+1}: {self.work_duration} mins""")
        os.system(f"""say "Session {self.count+1} is complete, take a break." -r 250""")

    def break_session(self):
        self.countdown(self.break_duration, "break_session")
        print(f"""✅ Break Session {self.count+1}: {self.break_duration} mins""")
        os.system(f"""say "Let's get back to work" -r 250""")
        self.count += 1

    def get_session_stats(self):
        total_working_time = self.work_duration * self.count
        hrs, mins = divmod(total_working_time, 60)

        print(
            f"""
                    SESSION STATISTICS
        =======================================
         Sessions           |    {self.count}
         Total Working Time |    {hrs} hrs {mins} mins
        =======================================
        """
        )

    def check_log_exist(self):
        return os.path.exists("session_log.json")

    def check_restart(self):
        while self.restart == "y":
            self.work_session()
            self.break_session()
            self.restart = input("☕ Start? [y/n]: ").lower()
        if self.restart == "n":
            exit_app = input("⬅️  Exit? [y/n]: ")
            if exit_app == "y":
                if self.count > 0:
                    self.get_session_stats()
                    self.log_session()
                sys.exit()
            else:
                self.restart = input("Start? [y/n]: ").lower()
                self.check_restart()

    def log_session(self):
        with open("session_log.json", "r") as f:
            dic = json.load(f)

            dic["session_names"] += [args.s] * self.count
            dic["start_times"] += self.start_times
            dic["end_times"] += self.end_times

            if self.last_session_id != 0:
                self.last_session_id = max(dic["session_id"])
            dic["session_id"] += [
                val + self.last_session_id for val in range(1, self.count + 1)
            ]

        with open("session_log.json", "w") as f:
            json.dump(dic, f, indent=4)

    def signal_handler(self, sig, frame):
        if self.count > 0:
            self.get_session_stats()
            self.log_session()

        print("Stopping session")

        sys.exit(0)


if __name__ == "__main__":
    os.system("clear")
    Pomodoro()
