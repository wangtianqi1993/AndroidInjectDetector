#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

current_path = os.path.dirname(__file__)


# log file path
LOG_PATH = 'detector_logging.log'

DOWNLOAD_PATH = '/root/apk_download_path'
REQUEST_URL = '/apkagent/advertise/'

HEART_IP = 'static.asec.buptnsrc.com'
HEART_PATH = '/apkagent/heartbeat'
HEART_WEB_PORT = '4466'

SEND_WEB_PORT = '4466'
AGENT_ID = 'inject_detector'
MY_LISTENING_PORT = "8899"

# 模拟器的id号
EMUERATE_NAME = "05ca91c70280ea7d"
