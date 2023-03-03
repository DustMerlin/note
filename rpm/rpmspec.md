# rpm spec

fg: no job control
可能为rpm spec 文件中，编译的命令不存在，所以导致的问题

%doc 
%license 
以上两个是从源码的文件夹中copy 文件到rpm包中，不经过buildroot

其余的都得先安装到 buildroot 目录，然后再使用 %files 经BUILDROOT 目录下的内容分配到具体的软件包中

%files 的目录得从 /目录copy 所以目录得写规范


%{_javadocdir}
%{_javadir}

%{_bin}
%{_lib}
%{_sbin}
%{_datadir}		/usr/share
以上目录都是根目录

在install 过程中在之前都需要添加 %{buildroot}%{_datadir}/%{name} 
如cp list %{buildroot}%{_datadir}/%{name} 
当然BUILDROOT 目录下的所有文件都必须得通过install 的方式去创建，并授予相应的权限

当然 %files 可以更精细的控制权限
目前还未 seata sentinel 精细的控制


使用spec 提供的宏编译和安装
%mvn_build

%mvn_install

此种方式需要本地安装依赖，目前使用网络源安装总会报错（网络报错，暂时没有办法）

%install 阶段应该由固定的文件目录

所以在%files 时也有固定的写法，具体的写法参考 fedora 官网 java 打包spec 规范
但是由于java 打包的必要性没那么高，其主要还是依赖mvn 处理，所以fedora 疑似废除mvn 依赖和java 相关的包
其实也没编译的必要,java 代码与平台架构无关，只需提供对应架构的java 运行时环境，既可以执行jar包

spec 只能方便安装，但是maven 依赖并不能直接从rpm 安装到系统环境中，起码目前没有很好的方法
mvn 命令也没有提供相应的命令，可以直接安装

mvn install 好像可以安装，但是与我想象中需要的安装方式并不相同，该方法需要指定能多参数，如果一一写在spec 中，内容及其繁杂
最终采取的方式是，将编译好的jar包，即java 字节码，安装到本地mvn 默认仓库中，该格式是通过mvn install 直接安装编译文件获取的
使用maven 依赖的坐标方式可以直接引入，如需直接使用jar 可以直接从相应目录下copy ,rpm -ql 可以查看软件包安装的内容

https://blog.csdn.net/thankna/article/details/111589310


mvn clean install
./mvn 命令脚本
编译方式可以从官方文档，README 文件，CI工程描述文件，配置项，脚本中搜索相应的内容
