# !/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wtq'

import os, sys
import time
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from androguard.core.bytecodes import apk
from config.config import EMUERATE_NAME

MEM_COUNT = "100"


def ptrace_inject(apk_path):
    """
    inject_sign: 0->ptrace fail, 1->ptrace success, -1->detect fail
    :return:
    """

    inject_sign = 1
    dump_sign = 1

    start_time = time.time()
    # install apk to emulator
    success_install_sign = install_apk(apk_path)

    package_name = " "
    try:
        a = apk.APK(apk_path)
        package_name = a.get_package()
    except Exception, e:
        print "get apk package name error", e

    # start apk
    run_apk_sign = run_apk(package_name)

    # get apk package to get pid and try ptrace inject
    if run_apk_sign:

        pid = get_pid(package_name)

        # 检测进程地址是否可以被dump

        if pid:
            dump_sign = dump_mem(pid, package_name)
            # use pid to inject apk
            inject_sign = inject_apk(pid)

        try:
            uninstall_shell = "adb -s "+ EMUERATE_NAME + " uninstall " + package_name
            p_uninstall = subprocess.Popen(uninstall_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
            p_uninstall.wait()
            print 'apk uninstall success'
        except Exception, e:
            print "uninstall error", e

    print "execute over!"
    end_time = time.time()
    print "use_time", end_time - start_time

    print "out ", inject_sign, dump_sign
    out = []	
    out.append(inject_sign)
    out.append(dump_sign)
    return out


def install_apk(apk_path):
    """

    :return:
    """
    success_install_sign = 0
    try:
        install_shell = "adb -s "+ EMUERATE_NAME +" install " + apk_path
        p_install = subprocess.Popen(install_shell, shell=True, executable="/bin/bash")
        p_install.wait()
        print "intall apk success!"
        success_install_sign = 1
    except Exception, e:
        print "install apk error!"

    return success_install_sign


def run_apk(package_name):
    """

    :return:
    """
    run_apk_sign = 0
    try:
        run_apk = "adb -s "+ EMUERATE_NAME +" shell monkey -p " + package_name + " -c android.intent.category.LAUNCHER 1"
        p_run = subprocess.Popen(run_apk, shell=True, executable="/bin/bash")
        p_run.wait()
        print "apk start success!"
        run_apk_sign = 1
    except Exception, e:
        print "apk start error!"
    return run_apk_sign


def get_pid(package_name):
    """

    :return:
    """
    get_pid_shell = "adb -s " + EMUERATE_NAME +" shell ps | grep " + package_name
    pid = 0
    try:
        p_install = subprocess.Popen(get_pid_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        p_install.wait()
        p_out = p_install.communicate()

        print p_out[0]

        pid_line = str(p_out[0]).split("\n")

        pid = pid_line[0].split(" ")[4]
    except Exception, e:
        print "get pid error", e
    return pid


def dump_mem(pid, package_name):
    """
    若是abd shell cat.....permission deny时，将 adb shell cat改成 adb root cat ...
    :return:
    """
    dump_sign = 0
    address = 0
    try:
        target_file = "/proc/" + pid + "/maps"
        get_address_shell = "adb -s " + EMUERATE_NAME +" shell cat " + target_file

        p_file = subprocess.Popen(get_address_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        p_file.wait()
        p_file_out = p_file.communicate()
        # print "maps content", p_file_out[0]
        first_line = str(p_file_out[0]).split("\n")[0]
        address = int(first_line.split("-")[0], 16)

        dd_shell = "adb -s " + EMUERATE_NAME +" shell dd if=/proc/" + pid + "/mem " + "of=/sdcard/" + package_name + " skip=" + str(address) + " ibs=1 " + "count=" + MEM_COUNT

        dump_out_shell = "adb -s " + EMUERATE_NAME +" shell ls -l /sdcard/" + package_name

        apk_dump = subprocess.Popen(dd_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        apk_dump.wait()

        dump_out = subprocess.Popen(dump_out_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        dump_out.wait()
        dump_out = dump_out.communicate()

        mem_file = dump_out[0].split(" ")
        if mem_file[12] == MEM_COUNT:
            dump_sign = 1

        # delete the file
        delete_shell = "adb -s " + EMUERATE_NAME + " shell rm -rf /sdcard/" + package_name
        delete_file = subprocess.Popen(delete_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        delete_file.wait()
    except Exception, e:
        print "dump mem fail ", e
    return dump_sign


def inject_apk(pid):
    """

    :param pid:
    :return:
    """
    inject_sign = 0

    try:

        inject_shell = "adb -s " + EMUERATE_NAME +" shell ./data/local/tmp/injectTarget " + pid
        p_inject = subprocess.Popen(inject_shell, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
        p_inject.wait()
        p_inject_out = p_inject.communicate()

        if "attach success" in p_inject_out[0]:
            inject_sign = 1

    except Exception, e:
        print "inject error", e
        inject_sign = 1

    return inject_sign


if __name__ == "__main__":
    ptrace_inject("Apk774.apk")
