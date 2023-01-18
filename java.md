# Java

javadoc -encoding UTF-8 -charset UTF-8 
某些情况下必须指定字符集，才能正确的生存javadoc，不然会直接报错
https://jiuaidu.com/jianzhan/972918/

-d 参数 可以指定生存的目录

目前只是学会了搜集所有的java 文件去生成doc

使用目录去生存doc 的方式，目前还没有理解清楚，也没有测试清楚

jconsole 命令,控制终端，完成

java -cp 启动参数，配置jconsole 远程链接java 进程

https://blog.csdn.net/D420941934/article/details/120473194

java 需要学习的内容:

javac 编译

java 启动命令 相关详细的内容需要

jvm 启动参数

jconsole 查看



下面开始命令方法运行jar文件，

输入java -jar xxx.jar，

输入java -Dfile.encoding=UTF-8 -jar xxx.jar，

输入java -Dfile.encoding=UTF-8 -Ddistributed_worker_id=1 -jar xxx.jar





&&&&&jar包的四种运行方式&&&&&
#1、直接启动： java -jar demo.jar
这种启动方式适合自己测试，因为一般部署在Linux上，这种方式关闭会话窗口或者ctrl+c都会关闭Java

#2、后台启动：java -jar demo.jar &
这种方式会在后台静默运行，关闭会话窗口会中断Java，和上一种一样，这两个日志都是打印在窗口的，关闭会话就没了

#3、nohup启动：nohup java -jar demo.jar &
这种会把日志打印到nohup.out文件中，但只会打印标准输出不会打印错误输出，关闭通过pid号来kill掉

#4、nohup启动：nohup java -jar demo.jar>/root/demo.log 2>&1 &
这种会把普通输出和错误输出都打印到demo.log中






mvn 命令学习

http://www.manongjc.com/detail/29-czhnvibtfztnxih.html

显示maven版本：

mvn -version/-v
显示详细错误 信息:

mvn -e
运行任何检查，验证包是否有效且达到质量标准:

mvn verify
1.编译源代码：

mvn compile
2.编译测试代码：

mvn test-compile
3.运行测试

mvn test
4.打包

mvn package
5.清除产生的项目：

mvn clean
6.只打包不测试

mvn -Dtest package
7.只测试不编译，也不测试编译

mvn test -skipping compile -skipping test-compile
8.查看当前项目已被解析的依赖：

mvn dependency:list
9.上传到私服

mvn deploy
10.配置好了之后执行

mvn clean install -Dmaven.test.skip=false
就能运行那些测试的类了

    给任何目标添加maven.test.skip 属性就能跳过测试 :

mvn install -Dmaven.test.skip=true
12.mvn compile与mvn install、mvn deploy的区别

    mvn compile，编译类文件
    mvn install，包含mvn compile，mvn package，然后上传到本地仓库
    mvn deploy,包含mvn install,然后，上传到私服

13.常用命令:

　　1>. 跳过测试:-Dmaven.test.skip(=true)
　　2>. 指定端口:-Dmaven.tomcat.port=9090
　　3>. 忽略测试失败:-Dmaven.test.failure.ignore=true 当然,如果你的其它关联项目有过更新的话,一定要在项目根目录下运行mvn clean install来执行更新,再运行mvn tomcat:run使改动生效.
14.mvnDebug tomcat:run

这条命令主要用来远程测试,它会监听远程测试用的8000端口,在eclipse里打开远程测试后,它就会跑起来了,设断点,调试
15.mvn dependency:sources

故名思义,有了它,你就不用到处找源码了,运行一下,你项目里所依赖的jar包的源码就都有了

原文地址：https://www.cnblogs.com/nanao/p/16067663.html 
