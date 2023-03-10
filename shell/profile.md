# profile

问题： 在debian 系的系统一般没有root 用户

使用管理员用户 sudo su 切换到管理员权限之后

终端 $ 前非常长的路径显示，严重影响了终端的使用

况且dde 的终端本来就不好用

https://blog.csdn.net/ytang_/article/details/78753200

问题：linux下，命令行显示路径仅最后一个文件名，非常不方便，想显示完整路径。
环境背景：linux，无root权限，可sudo(为了服务器安全，一般只给管理员root账号和密码，普通账号仅sudo权限)
方法：修改环境变量PS1，vi编辑/etc/profile文件在最后加上一行语句。

命令行提示符完全显示完整的工作目录名称：
export PS1=’[\u@\h $PWD]$ '
命令行提示符只列出最后一个目录：
export PS1=’[\u@\h \W]$’
命令行提示符显示完整工作目录，当前用户目录会以 ~代替：
export PS1=’[\u@\h \w]$’
修改完成后，执行: source /etc/profile 使配置生效即可。
命令释义：
\u 显示当前用户账号
\h 显示当前主机名
\W 只显示当前路径最后一个目录
\w 显示当前绝对路径（当前用户目录会以 ~代替）
$PWD 显示当前全路径
\$ 显示命令行’$'或者’#'符号

解决方法:q! 退出，然后命令行输入 sudo !!，再次vi编辑即可。
sudo !! // 解释：sudo来执行上一条命令，’!!’ 表示上一条命令，linux中’!'的用法可以参见参考[3]
参考：
[1] Linux 修改命令提示符当前路径的显示方式
[2] VIM提文件权限问题:…e45 readonly option is set (add!to override)
[3] Linux命令行下”!”的十个神奇用法


————————————————
版权声明：本文为CSDN博主「一只小草」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ytang_/article/details/78753200


## 最终修改

安装自己的喜欢导出该变量

需要用户名，当前主机是什么其实不那么重要，大多数都会写locahost和没有一样

    export PS1=’[\u/\W]$’
    # 当前用户/当前所在目录的路径，这种写法自己最习惯，也最简洁

> 今日份满足自己的需求完成，对系统理解又深入一点点