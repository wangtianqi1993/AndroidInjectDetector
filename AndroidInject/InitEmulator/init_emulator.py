# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wtq'

import os, sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

current_path = os.path.join(os.path.dirname(__file__), "..")


def launch_emulator(emulator_name="inject"):
    """
    开启android模拟器, 并初始化模拟器
    :return:
    """
    # start a emulator
    # p1 = subprocess.Popen("emulator -avd " + emulator_name, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
    # p1.wait()

    # push inject to emulator
    inject_file = current_path + "/InjectCore/injectTarget/jni/push.py"
    p2 = subprocess.Popen("python " + inject_file, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
    p2.wait()
    print "push success!"

if __name__ == "__main__":
    launch_emulator()
