# !/bin/bash
# $1 为项目的根路径
sudo docker run -d -p 5037:5037 -p 5554:5554 -p 5555:5555 -p 9515:9515 -p 8899:8899 -v /dev/bus/usb:/dev/bus/usb -v /home/wtq/develop/workspace/apk_download_path:/root/apk_download_path -v /home/wtq/develop/workspace/github/AndroidInject:/root/AndroidInject --privileged android_inject_detector:v0.1 sh /root/AndroidInject/RunShell/start_detector.sh

