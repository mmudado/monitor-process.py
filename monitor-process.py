#!/usr/bin/python3

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Check if PID exists - if not, starts process."""

import os, signal
import time
import subprocess, select
import sys, signal
import argparse
import string
from datetime import datetime

FNULL = open(os.devnull, 'w')
BASH = "/bin/bash"
PGREP =  "/usr/bin/pgrep"

def pgrep_process(process):
    command = PGREP + " -i " + process
    pid = 0
    try:
        pid = (subprocess.getoutput(command))
    except (IOError, OSError) as e:
        raise e
    return pid

def run_script(script):
    args = [BASH, script]
    try:
        subprocess.run(args)
    except (IOError, OSError) as e:
        raise e
    return True

####################
# RUNNING THE SCRIPT
####################
parser = argparse.ArgumentParser(description="checks process pid - runs process if pid is absent.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", required=False, action="store_true")
parser.add_argument("-p", "--process_name", required=True, type=str, help="name of the process: eg.: cardano-node ")
parser.add_argument("-s", "--script_full_path", required=True, type=str, help="full path for the script: eg.: /home/ubuntu/scripts/script.sh ")
args = parser.parse_args()

#### CHECK IF PROCESS IS RUNNING
if (pgrep_process(args.process_name)):
    pass
else:
    if (args.verbose):
        print("{} Process does not exist, running script...".format(datetime.now()))
    run_script(args.script_full_path)
