
yum install seata 


cd /usr/share/seata/bin
./seata-server.sh

打开浏览器访问
http://localhost:7091 
查看 seata server是否启动

安装mysql 

yum install mysql-server

启动mysql 查看mysql的状态
systemctl start mysqld
systemctl status mysqld

命令行直接使用输入mysql，进入mysql 交互模式

当前情况，可能没有用户，或root 用户存在，但是不存在密码
第一步设置用户，并修改root 用户密码

如果需要远程访问需要先创建 root@'%' 用户和密码，并设置权限GRANT 
方便起见可以设置全部权限，但生产环境中不推荐，GRANT 可以精细的设置用户权限
可以按需去设置权限

如需可视化工具访问mysql,则需要根据不同情况去配置
如需远程访问则应该有如下的步骤：

1.先创建可以远程访问的用户，控制其相应的权限，创建用户名类似 root@'%'
即可root 用户以任意的ip 访问

2. 防火墙开放相应的端口，mysql 数据库默认的端口为3306,若不开放端口
则其只能在本地的localhost:3306 端口访问
使用mysql-connector 或者navicat 等可视化数据库工具可以更方便的操作
当然也可以直接使用命令行的方式操作数据库

3. 如果是在局域网内配置数据库，开放端口后即可在局域网内访问数据库

如果远程链接，不能在局域网内直接访问，可以使用ssh 隧道的方式进行来链接

以navicat 举例

配置ssh ，选择以密码或证书的方式
然后配置mysql 数据库，用户名和密码即可
在选择是必须勾选 use ssh tunnel 选项，才可以正常使用
其界面是分隔开的，很容易让人误以为不同界面功能都是单独的

使用Test Connection可以检测链接是否正常
如果链接正常则链路显示蓝色，否则为红色
勾选不同的链接方式上方的链路图片也会有相应的变化

这可能是做的比较好的地方
然后点击ok 即可，双击链接显示绿色则链接数据库
双击具体的数据库则会缓存相应的数据
当数据库数据发生变化时，需要刷新数据库

命令行方式更简单，先ssh 链接到可以访问数据库的机器，然后mysql 命令使用用户登陆即可 


为了简单起见，使用最简单的方式配置一个最小还的测试环境，测试seata能否正常运行

spring boot + jdbc + mysql

关于dubbo,spring cloud,nacos, 数据源配置，微服务，注册中心等更多特性的组合，可以参照官网进行配置

4. 创建测试代码需要使用的数据库和测试表

使用navicat 可视化工具创建，直接测试项目中附带的sql文件

选址执行SQL 文件选择或是Execute SQL file
选择需要执行的sql 文件

执行后可以


!!!待验证

mysql -uroot -p 登陆mysql

set names utf8
source test.sql 

https://blog.csdn.net/chengliang666/article/details/125522403



5. 使用maven 编译打包测试项目

在安装seata 时已经安装maven依赖，所以不需要额外的操作
mvn clean package
此处时使用安装的seata依赖和mvn 下载相关的依赖，进行测试项目的编译

find -name "*.jar"
找到对应的jar 文件，启动即可

java -jar test.jar

6. 如果不出意外，可以在seata 的服务端查询到相应的事物记录



使用jconsole 可以查看当前seata进程的状态
打开jconsole或者直接在命令行输入jconsole 即可启动

选择seata-server.jar 进程即可连接查看，可能会有安全连接失败，这可能时启动时，
没有加相应的参数启动有关,但是并不影响
点击不安全连接,稍等片刻即可连接成功


7. 配置nacos 注册中心

将seata服务注册到nacos管理 


