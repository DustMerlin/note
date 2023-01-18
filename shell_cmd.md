# 常用命令总结

## top 

统计信息区：

前五行是当前系统情况整体的统计信息区。下面我们看每一行信息的具体意义。
第一行，任务队列信息，同 uptime 命令的执行结果，具体参数说明情况如下：

14:06:23 — 当前系统时间

up 70 days, 16:44 — 系统已经运行了70天16小时44分钟（在这期间系统没有重启过的吆！）

2 users — 当前有2个用户登录系统

load average: 1.15, 1.42, 1.44 — load average后面的三个数分别是1分钟、5分钟、15分钟的负载情况。

load average数据是每隔5秒钟检查一次活跃的进程数，然后按特定算法计算出的数值。如果这个数除以逻辑CPU的数量，结果高于5的时候就表明系统在超负荷运转了。
第二行，Tasks — 任务（进程），具体信息说明如下：

系统现在共有206个进程，其中处于运行中的有1个，205个在休眠（sleep），stoped状态的有0个，zombie状态（僵尸）的有0个。
第三行，cpu状态信息，具体属性说明如下：

5.9%us — 用户空间占用CPU的百分比。

3.4% sy — 内核空间占用CPU的百分比。

0.0% ni — 改变过优先级的进程占用CPU的百分比

90.4% id — 空闲CPU百分比

0.0% wa — IO等待占用CPU的百分比

0.0% hi — 硬中断（Hardware IRQ）占用CPU的百分比

0.2% si — 软中断（Software Interrupts）占用CPU的百分比

备注：在这里CPU的使用比率和windows概念不同，需要理解linux系统用户空间和内核空间的相关知识！
第四行,内存状态，具体信息如下：

32949016k total — 物理内存总量（32GB）

14411180k used — 使用中的内存总量（14GB）

18537836k free — 空闲内存总量（18GB）

169884k buffers — 缓存的内存量 （169M）
第五行，swap交换分区信息，具体信息说明如下：

32764556k total — 交换区总量（32GB）

0k used — 使用的交换区总量（0K）

32764556k free — 空闲交换区总量（32GB）

3612636k cached — 缓冲的交换区总量（3.6GB）

备注：

第四行中使用中的内存总量（used）指的是现在系统内核控制的内存数，空闲内存总量（free）是内核还未纳入其管控范围的数量。纳入内核管理的内存不见得都在使用中，还包括过去使用过的现在可以被重复利用的内存，内核并不把这些可被重新使用的内存交还到free中去，因此在linux上free内存会越来越少，但不用为此担心。

如果出于习惯去计算可用内存数，这里有个近似的计算公式：第四行的free + 第四行的buffers + 第五行的cached，按这个公式此台服务器的可用内存：18537836k +169884k +3612636k = 22GB左右。

对于内存监控，在top里我们要时刻监控第五行swap交换分区的used，如果这个数值在不断的变化，说明内核在不断进行内存和swap的数据交换，这是真正的内存不够用了。
第六行，空行。
第七行以下：各进程（任务）的状态监控，项目列信息说明如下：

PID 
USER
PR      进程优先级
NI      nice值，负数高优先级，正数低优先级
VIRT    进程使用虚拟内存总量 KB        VIRT=SWAP+RES
RES     进程私用的，未被患处的物理内存大小 KB RES=CODE+DATA
SHR     共享内存大小 KB
S       进程状态
    D   不可中断的睡眠状态
    R   运行
    S   睡眠
    T   跟踪/停止
    Z   僵尸进程
%CPU    上次更新到现在的CPU时间占比
%MEM    进程使用的物理内存占比
TIME+   进程使用的CPU时间统计 1/100s
COMMAND 进程名称（命令名/命令行）

top -c  显示完整的COMMAND
top -S  以积累模式显示程序信息
top -n2 设置更新次数，更新两次后停止更新显示
top -d3 设置更新时间，每3s更新一次
top -p  指定pid 显示

top 交互式命令

    h 显示帮助画面，给出一些简短的命令总结说明

    k 终止一个进程。

    i 忽略闲置和僵死进程。这是一个开关式命令。

    q 退出程序

    r 重新安排一个进程的优先级别

    S 切换到累计模式

    s 改变两次刷新之间的延迟时间（单位为s），如果有小数，就换算成m s。输入0值则系统将不断刷新，默认值是5 s

    f或者F 从当前显示中添加或者删除项目

    o或者O 改变显示项目的顺序

    l 切换显示平均负载和启动时间信息

    m 切换显示内存信息

    t 切换显示进程和CPU状态信息

    c 切换显示命令名称和完整命令行

    M 根据驻留内存大小进行排序

    P 根据CPU使用百分比大小进行排序

    T 根据时间/累计时间进行排序

    W 将当前设置写入~/.toprc文件中


top 界面

b 高亮显示当前进程

1 监控每个逻辑CPU的情况

top 默认CPU 占用量排序
x 打开或关闭高亮CPU 占用

shift < 或 shift > 改变排序

————————————————
版权声明：本文为CSDN博主「zoujiangMr」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/m0_51627713/article/details/118091336


## tar 命令

https://blog.csdn.net/weixin_39860757/article/details/111107720


tar -zxvf 解压 -C 指定目录解压
tar -zcvf tar.gz 压缩


## 防火墙

https://blog.csdn.net/GEGEGEHUI/article/details/125273910

对于本地localhost 相应端口启动的http 服务，如果在防火墙开放其端口，即可在统一网段之间互相访问


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


## shell 学习相关的内容

grep sed awk 详细学习


## cp 命令

强制覆盖

cp -rf 与 rm 类似
cp 交互模式是由于 alias cp='cp -i'

yes | cp -r pom.xml . 如果是交互模式，yes命令也不行

在命令前添加反斜线 
\cp -r pom.xml . 

取消 alias 即可直接覆盖
unlias cp 
cp -r pom.xml .


## nohub

nohup 是 no hang up 的缩写，意思是不挂断

seata 的运行脚本本身就是后台运行的，所以使用nohup 的作用并不大
只是将将输出到控制台的信息输出到了nohun.out 文件中了

## 安装mysql 

yum install mysql-server 

启动mysql服务
systemctl restart mysqld

mysql 即可登陆，但是当前状态可能不存在用户
所以使用mysql 直接登陆了

设置root 用户和密码，此时该用户还没有权限
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';

此种方式可以修改密码，但是此次并未使用
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Root_123';

查看MySQL 初始化的密码策略,如果没有则为空
SHOW VARIABLES LIKE 'validate_password%';

设置修改密码策略
set global validate_password.check_user_name=OFF
set global validate_password.length=4;
set global validate_password.mixed_case_count=0;
set global validate_password.number_count=0;
set global validate_password.policy=LOW;
set global validate_password.special_char_count=0;

    validate_password.dictionary_file 指定密码验证的文件路径

    validate_password.length 固定密码的总长度

    validate_password.mixed_case_count 整个密码中至少要包含大/小写字母的总个数

    validate_password.number_count 整个密码中至少要包含阿拉伯数字的个数

    validate_password.policy 指定密码的强度验证等级，默认为 MEDIUM

    LOW：只验证长度
    MEDIUM：验证长度、数字、大小写、特殊字符
    STRONG：验证长度、数字、大小写、特殊字符、字典文件

    validate_password_special_char_count 整个密码中至少要包含特殊字符的个数
————————————————
版权声明：本文为CSDN博主「编程洪同学」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_44402184/article/details/122113037

当前系统无默认的密码规则，所以直接可以设置成简单密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';

为root 用户授予所有的权限
grant all on *.* to 'root'@'localhost';
关键字理应大写，以示区分，但是大小写并不影响mysql语法大小写不敏感

!!! 此时授权的部分的内容还需要仔细研究，root 没法正常授权，起码目前看来无法直接远程登陆
其实该测试以下，但是docker 启动的花，可以方便的使用远程登陆，navicat ssh 隧道，远程链接
可能是mysql 的docker 镜像有额外的配置
当前创建的root 的用户权限有问题，提示无法创建root@'%'用户
所以先创建root@'%' 可以匹配任意host 的用户然后再授权，授予全部的权限（偷懒如此，其实该精细的控制权限）



立即刷新生效
flush privileges; 

flush privileges; 
use mysql;
mysql 的相关数据都存储在该数据库中
使用sql 命令可以查询相应的内容

查询用户的信息
select host,user,authentication_string from user;

查看用户的权限 用户名@主机名,且用户必须存在
show grants for root@localhost;
