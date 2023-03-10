# systemd

初窥systemd
https://www.oocolo.com/184040.html

## 缺so 导致的服务无法启动

https://blog.csdn.net/ecjtusanhu/article/details/108465408

查看环境变量是否包含so $LD_LIBRARY_PATH

但是该环境变量，并不存在与系统环境中

此处为以遗留问题，但是暂未探索

[Service]
Environment=LD_LIBRARY_PATH=/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:/opt/rh/devtoolset-7/root/usr/lib64/dyninst:

systemd service 也还未仔细研究

