from subprocess import Popen, PIPE, list2cmdline
import os
import glob
import datetime
import time

python = r"C:\Users\Makdos\AppData\Local\Programs\Python\Python36\python.exe"
arabam_veri_cekici = r"C:\Users\Makdos\Desktop\firsatarabam\insert_arabam_data_into_db.py"
trial = r"C:\Users\Makdos\Desktop\firsatarabam\trial.py"
trial2 = r"C:\Users\Makdos\Desktop\firsatarabam\trial2.py"

commands = { # "arabam_veri_cekici": [python, arabam_veri_cekici],
            "trial": [python, trial],
            "trial2": [python, trial2]}
process_dict = {}


def run_commands(cmds):
    # process_dict["arabam_veri_cekici"] = Popen(cmds[0])
    for i in cmds:
        process_dict[i] = Popen(cmds[i])
    if not cmds:
        return

    def success(b):
        if b.returncode == 1 or b.returncode == 0:
            return 1

    while True:
        for process in process_dict:
            time.sleep(1)
            p = process_dict[process]
            p.poll()
            if success(p):
                process_dict[process] = Popen(cmds[process])

run_commands(commands)
