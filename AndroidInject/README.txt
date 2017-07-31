1. 安装docker, 拷贝镜像android_inject_detector到本地服务器
2. 修改 AndroidInject/config/config.py中的相关配置
3. 在本地对测试机初始化， 介入测试机后，到 AndroidInject/InitEmulator下执行　python init_emulator.py
4. 进入 AndoirdInject/RunShell 将start_detector.sh 中的/home/wtq/develop/workspace/apk_download_path改为要存放apk的路径.
然后执行source start_detector.sh 开启检测服务
