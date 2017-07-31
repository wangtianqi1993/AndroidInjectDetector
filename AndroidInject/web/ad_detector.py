# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import time
import threading
from threading import Lock
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests
from web.task_queue import detector_task, running_detector_task
from config.config import DOWNLOAD_PATH, SEND_WEB_PORT, REQUEST_URL, AGENT_ID
from log.logger import AdDetectorLogger
from InjectDump.inject_and_dump import ptrace_inject

logger = AdDetectorLogger()


def detector_server():
    print(threading.current_thread().name + ":" + "server....")

    while True:

        # 扫描任务队列，查找是否有需要处理的任务
        if detector_task.getsize():
            logger.info(
                threading.current_thread().name + ": " + "the number of task_queue" + str(detector_task.getsize()))

            # ensure getting element from queue is a atom operator
            lock = Lock()
            lock.acquire()
            task_id = detector_task.task_id.get()
            app_name = detector_task.app_name.get()
            web_ip = detector_task.wed_ip.get()
            sign = detector_task.sign.get()
            if not sign:
                port = detector_task.port.get()
                path = detector_task.path.get()
            # 正在运行的任务数量减1
            running_detector_task.pop(task_id)
            lock.release()
            # apk_path = os.path.join(DOWNLOAD_PATH, app_name)
            apk_path_new = DOWNLOAD_PATH + "/" + app_name
            # print 'apk_path_new', apk_path_new

            detector_report = {}
            detector_report['apk_name'] = app_name
            detector_report["ptrace_sign"] = 1
            detector_report["dump_sign"] = 1
            # start detecting apk ptrace_inject
            try:

                if sign:
                    # ptrace inject detector
                    try:
                        ptrace_sign = ptrace_inject(apk_path_new)
                        detector_report["ptrace_sign"] = ptrace_sign[0]
                        detector_report["dump_sign"] = ptrace_sign[1]
                    except Exception, e:
                        print "ptrace error", e

                logger.info(detector_report)
                # 检测完后删除apk
                os.remove(apk_path_new)
                if sign:
                    r = requests.put("http://" + web_ip + ":" + str(SEND_WEB_PORT) + REQUEST_URL
                                     + task_id, data=json.dumps({"agent_id": AGENT_ID, "status": 4,
                                                                 "detector_report": detector_report}))
                else:
                    r = requests.put("http://" + web_ip + ":" + str(port) + path
                                     + task_id, data=json.dumps({"agent_id": AGENT_ID, "status": 4,
                                                                 "detector_report": detector_report}))

            # return data to client
            except Exception as e:
                logger.info(e)
                try:
                    if sign:
                        r = requests.put("http://" + web_ip + ":" + str(SEND_WEB_PORT) + REQUEST_URL
                                         + task_id,
                                         data=json.dumps({"agent_id": AGENT_ID, "status": 0, "detector_report": ""}))
                    else:
                        r = requests.put("http://" + web_ip + ":" + str(port) + path
                                         + task_id,
                                         data=json.dumps({"agent_id": AGENT_ID, "status": 0, "detector_report": ""}))
                except Exception as e:
                    logger.info(e)

        else:
            print(threading.current_thread().name + ":" + "没有新任务  " + str(len(running_detector_task)) +
                  "正在运行" + "  有" + str(detector_task.getsize()) + "正在等待, 暂停5秒")
            time.sleep(3)


if __name__ == "__main__":
    apk_path = "/home/wtq/develop/workspace/test/"
    # paths = os.listdir(apk_path)
    # for temp_path in paths:
    #     result = ad_detector(os.path.join(apk_path, temp_path))
    #     print result
    # print auto_detector("/home/wtq/develop/workspace/malware_test_apk/malware4.apk", "/home/wtq/develop/workspace/malware_test_apk/malware_class", "malware4")
    # print ad_detector("/home/wtq/develop/workspace/test/waicai.apk")
