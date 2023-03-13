# so问题

ldconfig提示is not a symbolic link警告的去除方法

https://blog.csdn.net/kentyu001/article/details/53843050

ldconfig
ldconfig: /usr/local/lib/gliethttp/libxerces-c-3.0.so is not a symbolic link
问题分析：
因为libxerces-c-3.0.so正常情况下应该是一个符号链接,而不是实体文集件,修改其为符号链接即可
解决方法：
mv libxerces-c-3.0.so libxerces-c.so.3.0
ln -s libxerces-c.so.3.0 libxerces-c-3.0.so 

带数字的so 多的都是链接文件，而非实体文件，所以在copy 的时候不能随意复制

但是同样文件，只替换so ，可以不可直接使用，应该和替换文件的兼容性有关

因为安装的时候就只是把文件cp 到lib 目录中
如果rpath 路径没有去除的话，是可以正常找到的
如果去除了rpath 需要在ld.so.conf.d 目录中以单独的文件写明路径

在安装完成后的阶段还需要执行ldconfig 将so 文件加载

so undefined symbol 调查
http://events.jianshu.io/p/e6289b247cfb

nm -D 查询到的有可能是他需要的符号，而且其提供的，如U 开头的则是该so 需要的

!!! 需要了解so 详细的资料，目前认知的短板容易进入误区


可能的原因

    依赖库未找到
    这是最常见的原因，一般是没有指定查找目录，或者没有安装到系统查找目录里
    链接的依赖库不一致
    编译的时候使用了高版本，然后不同机器使用时链接的却是低版本，低版本可能缺失某些 api
    符号被隐藏
    如果动态库编译时被默认隐藏，外部代码使用了某个被隐藏的符号。
    c++ abi 版本不一致
    最典型的例子就是 gcc 4.x 到 gcc 5.x 版本之间的问题，在 4.x 编辑的动态库，不能在 5.x 中链接使用。
