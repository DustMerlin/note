# firewall port

https://blog.csdn.net/GEGEGEHUI/article/details/125273910

linux系统防火墙开放端口
GEGEGEHUI
于 2022-06-14 10:47:42 发布 9071
收藏 46
文章标签： linux centos 网络
版权

在外部访问CentOS中部署应用时，需要通过防火墙管理软件,开端口,或者直接关闭防火墙进行解决(不建议)

常用命令：
systemctl start firewalld #启动
systemctl stop firewalld #停止
systemctl status firewalld #查看状态
systemctl disable firewalld #开机禁用
systemctl enable firewalld #开机启动

开放或关闭端口：
firewall-cmd --zone=public --add-port=80/tcp --permanent #开放80/tcp端口 （--permanent永久生效，没有此参数重启后失效）
firewall-cmd --zone=public --query-port=80/tcp #查看80/tcp端口
firewall-cmd --zone=public --remove-port=80/tcp --permanent #关闭80/tcp端口

批量开放或关闭端口：
firewall-cmd --zone=public --add-port=40000-45000/tcp --permanent #批量开放端口，打开从40000到45000之间的所有端口
firewall-cmd --zone=public --list-ports #查看系统所有开放的端口
firewall-cmd --zone=public --remove-port=40000-45000/tcp --permanent #批量关闭端口，关闭从40000到45000之间的所有端口

更新防火墙的设置：
firewall-cmd --reload #更新防火墙的设置，使上面的修改生效
————————————————
版权声明：本文为CSDN博主「GEGEGEHUI」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/GEGEGEHUI/article/details/125273910
