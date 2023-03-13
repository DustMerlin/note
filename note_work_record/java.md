# java

## .mvn/jvm.config

https://maven.apache.org/configure.html

服务器上内存所剩余不多了，用mvn打包报内存不足。解决办法就要把vm options中内存设置小一些。
.mvn/jvm.config文件：

从 Maven 3.3.1+ 开始，您可以通过${maven.projectBasedir}/.mvn/jvm.config文件定义 JVM 配置，这意味着您可以在每个项目基础上定义构建选项。该文件将成为您项目的一部分，并将与您的项目一起签入。所以不再需要MAVEN_OPTS,.mavenrc文件。因此，例如，如果您将以下 JVM 选项放入${maven.projectBasedir}/.mvn/jvm.config文件中

  -Xmx2048m -Xms1024m -XX:MaxPermSize=512m -Djava.awt.headless=true

    1

您无需在不同配置中使用这些选项MAVEN_OPTS或在不同配置之间切换。

这样配置完成后就可以正常打包了。

VM Options: -Xms512m -Xmx1024m 可以设置不同的大小根据实际情况设置

本质应该是限制jvm 使用内存
这些可以设定的参数，暂未仔细研究

> mavan 打包出现问题，大概可能是内存不足，以上方法解决


## java 执行程序，传递参数，获取


https://blog.csdn.net/u014486725/article/details/124054806

 IDEA 中设置
ParamDemo这个带main方法的类，设置VM Options为-DvmParam="hello"，设置Program arguments为a b c。

    public class ParamDemo {
     
        public static void main(String[] args) {
            //获取系统参数
            String vmParam = System.getProperty("vmParam");
            System.out.println("vmOption的参数为：" + vmParam);
            //获取main方法的参数
            for (int i = 0; i < args.length; i++) {
                System.out.println("main方法参数为：" + args[i]);
            }
        }
    }

执行main方法结果如下：

    vmOption的参数为：hello
    main方法参数为：a
    main方法参数为：b
    main方法参数为：c


System.getProperty("vmParam") 该方式获取

java -jar xxx.jar -DvmParam="hello"  a b c  将代码打成jar包使用命令执行是同样的效果。


