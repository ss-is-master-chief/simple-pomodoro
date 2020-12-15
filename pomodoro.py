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


class Pomodoro:
    def __init__(self):
        self.count = 0
        self.restart = "y"
        self.command_regex = r"""(start\s{0,}(?P<work_duration>\d+))?\s{0,}(break\s{0,}(?P<break_duration>\d+))?\s{0,}(session\s{0,}(?P<session_name>\w+))?"""
        self.work_duration = 25
        self.break_duration = 5
        self.session_name = "PomoSession"
        self.last_session_id = 0
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

        self.command = input("🍅 > ")
        self.execute_command()

    def countdown(self, t, session_type):
        if session_type == "work_session":
            prefix = f"""⏳ [{self.session_name}] Working Session {self.count+1}: """
        else:
            prefix = f"""⏳ [{self.session_name}] Break Session {self.count+1}: """

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
        self.session_names.append(self.session_name)
        print(
            f"""✅ [{self.session_name}] Working Session {self.count+1}: {self.work_duration} mins"""
        )
        os.system(f"""say "Session {self.count+1} is complete, take a break." -r 250""")

    def break_session(self):
        self.countdown(self.break_duration, "break_session")
        print(
            f"""✅ [{self.session_name}] Break Session {self.count+1}: {self.break_duration} mins"""
        )
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

    def log_session(self):
        with open("session_log.json", "r") as f:
            dic = json.load(f)

            if dic["session_id"] != []:
                self.last_session_id = max(dic["session_id"])

            dic["session_names"] += self.session_names
            dic["start_times"] += self.start_times
            dic["end_times"] += self.end_times

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

    def execute_command(self):
        if self.command == "start":
            self.work_session()
            self.break_session()
            self.command = input("🍅 > ")
            self.execute_command()
        elif self.command == "exit":
            if self.count > 0:
                self.get_session_stats()
                self.log_session()
            sys.exit()
        else:
            dic = list(re.finditer(self.command_regex, self.command))[0].groupdict()
            if list(dic.values()) == [None, None, None]:
                print(
                    f"""🤔 Didn't get you. Here are a few examples:
    Command Format:
        - 'start': start timer with default value
        - 'start <work_duration>': update default session duration and start
        - 'break <break_duration>': update default break duration and start
        - 'session <session_name>': update session name and start
        - 'start <work_duration> break <break_duration>': update session & break and start
        - 'exit': close program
            """
                )
                self.command = input("🍅 > ")
                self.execute_command()
            else:
                if dic["work_duration"] != None:
                    self.work_duration = int(dic["work_duration"])
                if dic["break_duration"] != None:
                    self.break_duration = int(dic["break_duration"])
                if dic["session_name"] != None:
                    self.session_name = dic["session_name"]
                print(
                    f"""🕑 Default working session length: {self.work_duration} mins"""
                )
                print(f"""🕑 Default break session length: {self.break_duration} mins""")
                self.work_session()
                self.break_session()
                self.command = input("🍅 > ")
                self.execute_command()


if __name__ == "__main__":
    os.system("clear")
    Pomodoro()
