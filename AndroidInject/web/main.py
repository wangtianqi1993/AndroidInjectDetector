# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#sys.path.append("/home/wangtianqi/develop/workspace/gitlab/PtraceDetector/android-app-security-detector/")
import threading
from ad_detector_service import AppWebService
from ad_detector import detector_server
from log.logger import AdDetectorLogger

logger = AdDetectorLogger()


def main():
    """
    将监听客户端请求的handler函数与对广告进行检测的函数分开作为两个独立的线程
    启动，增强了处理性能
    :return:
    """
    logger.info(threading.current_thread().name + ":" + "main running")
    app_web = AppWebService()

    web_service = threading.Thread(target = app_web.start,)

    heart_beat = threading.Thread(target = app_web.heart_beat, )

    server_thread = threading.Thread(target = detector_server, )
    # auto_detetor(MALWARE_APK_PATH, MALWARE_CLASSES_PATH)
    print ("start...")
    web_service.start()
    heart_beat.start()
    server_thread.start()
    # while not server_thread.is_alive:
    #     server_thread.start()

if __name__ == '__main__':
    main()
