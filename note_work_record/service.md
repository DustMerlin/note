# service

https://blog.csdn.net/guoke312/article/details/120326890

如何编写一个Systemd Service

guoke312
于 2021-09-16 13:24:45 发布 1574
收藏 3
文章标签： linux shell
版权
0x01 什么是Systemd Service

    Systemd 服务是一种以 .service 结尾的单元（unit）配置文件，用于控制由Systemd 控制或监视的进程。简单说，用于后台以守护精灵（daemon）的形式运行程序。
    Systemd 广泛应用于新版本的RHEL、SUSE Linux Enterprise、CentOS、Fedora和openSUSE中，用于替代旧有的服务管理器service。
    基本命令：

systemctl command xxx.service
# 其中command可以是start、stop、restart、enable等，比如：
systemctl start httpd.service #启动Apache服务
systemctl stop httpd.service #停止Apache服务
systemctl restart httpd.service #停止Apache服务
systemctl enable mariadb.service #将MariaDB服务设为开机启动

0x02 Systemd Service 存放的位置

    Systemd Service 位于 /etc/systemd/system（供系统管理员和用户使用），/usr/lib/systemd/system（供发行版打包者使用），我们一般使用前者即可。

0x03 编写Systemd Service

    Systemd 服务的内容主要分为三个部分，控制单元（unit）的定义、服务（service）的定义、以及安装部分。

1. 定义控制单元 [Unit]

    在 Systemd 中，所有引导过程中 Systemd 要控制的东西都是一个单元。基本的用法如下：
    Description：代表整个单元的描述，可根据需要任意填写。
    Wants：本单元启动了，它“想要”的单元也会被启动。但是这个单元若启动不成功，对本单元没有影响。
    Requires: 这个单元启动了，那么它“需要”的单元也会被启动; 它“需要”的单元被停止了，它自己也活不了。但是请注意，这个设定并不能控制启动顺序，因为它“需要”的单元启动也需要时间，若它“需要”的单元启动还未完成，就开始启动本单元，则本单元也无法启动，所以不建议使用这个字段。
    OnFailure：若本单元启动失败了，那么启动这个单元作为折衷。
    Before/After：指定启动顺序。
    看一个实际的例子：

[Unit]
Description=Protect ARP list
Wants=network-online.target
After=network.target

    其中network.target代表有网路，network-online.target代表一个连通着的网络。

2. 定义服务本体 [service]

    在定义完了 Systemd 用来识别服务的单元后，我们来定义服务本体。基本的用法如下：

    Type：服务的类型，各种类型的区别如下所示
        simple：默认，这是最简单的服务类型。意思就是说启动的程序就是主体程序，这个程序要是退出那么一切皆休。
        forking：标准 Unix Daemon 使用的启动方式。启动程序后会调用 fork() 函数，把必要的通信频道都设置好之后父进程退出，留下守护精灵的子进程。
        oneshot：适用于那些被一次性执行的任务或者命令，它运行完成后便了无痕迹。因为这类服务运行完就没有任何痕迹，我们经常会需要使用 RemainAfterExit=yes。意思是说，即使没有进程存在，Systemd 也认为该服务启动成功了。同时只有这种类型支持多条命令，命令之间用;分割，如需换行可以用\。
        dbus：这个程序启动时需要获取一块 DBus 空间，所以需要和 BusName= 一起用。只有它成功获得了 DBus 空间，依赖它的程序才会被启动。
    ExecStart：在输入的命令是start时候执行的命令，这里的命令启动的程序必须使用绝对路径，比如你必须用/sbin/arp而不能简单的以环境变量直接使用arp。
    ExecStop：在输入的命令是stop时候执行的命令，要求同上。
    ExecReload：这个不是必需，如果不写则你的service就不支持restart命令。ExecStart和ExecStop是必须要有的。
    看一个实际的例子：

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/arp -f /etc/ip-mac
ExecReload=/sbin/arp -f /etc/ip-mac
ExecStop=/sbin/arp -d -a

    这里在start和restart的时候会读取并添加/etc/ip-mac文件中的ARP条目到ARP表中，而stop时清空ARP表。

3. 安装服务 [install]

    服务编写完之后还需要被systemd装载，定义安装单元各个字段如下：
    WantedBy：设置服务被谁装载，一般设置为multi-user.target
    Alias：为service设置一个别名，可以使用多个名字来操作服务。
    Also：在安装这个服务时候还需要的其他服务

4.完整的 Systemd Service 配置实例

    组合上面的三个模块，我们可以得到一个完整的 Systemd Service 配置实例：

[Unit]
Description=Protect ARP list
Wants=network-online.target
After=network.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/arp -f /etc/ip-mac
ExecReload=/sbin/arp -f /etc/ip-mac
ExecStop=/sbin/arp -d -a
[Install]
WantedBy=multi-user.target

0x04 总结

    Systemd Service 是一种替代/etc/init.d/下脚本的更好方式，它可以灵活的控制你什么时候要启动服务，一般情况下也不会造成系统无法启动进入紧急模式。所以如果想设置一些开机启动的东西，可以试着写 Systemd Service。当然了，前提是你使用的Linux发行版是支持它的才行。

仔细看了一下RemainAfterExit的作用：

RemainAfterExit=

Takes a boolean value that specifies whether the service shall be considered active even when all its processes exited. Defaults to no.

我想应该是我们使用了bash来执行一串命令，而bash在执行完这些指令后退出，所以systemd认为所有的它的子进程（包括它启动的uwsgi）也应该退出，所以给这些进程发送了TERM信号，要他们退出，在没有收到回应的情况下又发送了KILL信号，将这些进程强制退出。
