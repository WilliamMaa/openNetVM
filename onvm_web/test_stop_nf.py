# !/usr/bin/env python3

import os
import signal
import shlex

# open the log file to read the process name of the nfs
message = []
with open('./test.txt', 'r') as log_file:
    log = log_file.readline()
    while(log is not None and log != ""):
        log_info = log.split(" ")
        if(log_info[0] == "Starting"):
            command = "ps -ef | grep sudo | grep " + \
                log_info[1] + " | grep -v 'grep' | awk '{print $2}'"
            # command = ["ps", "-ef", "|", "grep", "sudo", "|", "grep", log_info[1], "|", "grep", "-v", "'grep'", "|", "awk", "'{print $2}'"]
            pids = os.Popen(shlex.split(command))
            pid_processes = pids.read()
            if pid_processes != "":
                pid_processes = pid_processes.split("\n")
                message.append(pid_processes)
                for i in pid_processes:
                    os.kill(int(i), signal.SIGKILL)
