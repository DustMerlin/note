# shell cmd

## shell 判断


shell脚本[] [[]] -n -z 的含义解析
栗少
于 2021-11-21 18:58:05 发布 1211
收藏 2
文章标签： jenkins idea java
版权

在写脚本的时候，总是搞不懂[] [[]]的区别，这次写一个总结，把它掌握牢固

应用场景分析：

1、在中括号中，判断变量的值， 加不加双引号的问题？
-z 判断 变量的值，是否为空； zero = 0


 - 变量的值，为空，返回0，为true

 - 变量的值，非空，返回1，为false

 -n 判断变量的值，是否为空 name = 名字

 - 变量的值，为空，返回1，为false

 - 变量的值，非空，返回0，为true

 pid="123"

  [ -z "$pid" ] 单对中括号变量必须要加双引号

  [[ -z $pid ]] 双对括号，变量不用加双引号


  [ -n "$pid" ] 单对中括号，变量必须要加双引号

  [[ -z $pid ]] 双对中括号，变量不用加双引号

 2、多个条件判断，[] 和 [[]] 的区别？

 2.1：[[ ]] 双对中括号，是不能使用 -a 或者 -o的参数进行比较的；

 && 并且 || 或 -a 并且 -o 或者

 [[ ]] 条件判断 && 并且 || 或


 [[ 5 -lt 3 || 3 -gt 6 ]] 一个条件，满足，就成立 或者的关系 

 [[ 5 -lt 3 || 3 -gt 6 ]] 一个条件满足，就成立 或者的关系 


 [[ 5 -lt 3 ]] || [[3 -gt 6 ]] 

 [[ 5 -lt 3 ]] || [[3 -gt 6 ]] 写在外面也可以


 && 必须两个条件同时满足，和上述一样，这里想说明的问题的是：


 [[ 5 -lt 3]] -o [[ 3 -gt 6 ]] [[ 5 -lt 3 -o 3 -gt 6 ]] 

 [[ 5 -lt 3 -a 3 -gt 6 ]] [[ 5 -lt 3 -a 3 -gt 6 ]] 

 -a 和 -o就不成立了，是因为，[[]] 双对中括号，不能使用 -o和 -a的参数

 直接报错：


   2.2 [ ] 可以使用 -a -o的参数，但是必须在 [ ] 中括号内，判断条件，例如：
  

   [ 5 -lt 3 -o 3 -gt 2 ] 或者条件成立
  

   [5 -lt 3 ] -o [ 3 -gt 2] 或者条件， 这个不成立，因为必须在中括号内判断
  
   如果想在中括号外判断两个条件，必须用&& 和 || 比较
  

   [5 -lt 3 ] || [ 3 -gt 2] 
   [5 -gt 3 ] && [ 3 -gt 2] 成立
   
   相对的，|| 和 && 不能在中括号内使用，只能在中括号外使用
  

   3、当判断某个变量的值是否满足正则表达式的时候，必须使用[[ ]] 双对中括号
  
   单对中括号，直接报错：
  


————————————————
版权声明：本文为CSDN博主「李常明」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/keep_lcm/article/details/80551435




## shell

常用的：
[ -a FILE ] 如果 FILE 存在则为真。
[ -d FILE ] 如果 FILE 存在且是一个目录则返回为真。
[ -e FILE ] 如果 指定的文件或目录存在时返回为真。
[ -f FILE ] 如果 FILE 存在且是一个普通文件则返回为真。
[ -r FILE ] 如果 FILE 存在且是可读的则返回为真。
[ -w FILE ] 如果 FILE 存在且是可写的则返回为真。（一个目录为了它的内容被访问必然是可执行的）
[ -x FILE ] 如果 FILE 存在且是可执行的则返回为真。

不常用的：
[ -b FILE ] 如果 FILE 存在且是一个块文件则返回为真。
[ -c FILE ] 如果 FILE 存在且是一个字符文件则返回为真。
[ -g FILE ] 如果 FILE 存在且设置了SGID则返回为真。
[ -h FILE ] 如果 FILE 存在且是一个符号符号链接文件则返回为真。（该选项在一些老系统上无效）
[ -k FILE ] 如果 FILE 存在且已经设置了冒险位则返回为真。
[ -p FILE ] 如果 FILE 存并且是命令管道时返回为真。
[ -s FILE ] 如果 FILE 存在且大小非0时为真则返回为真。
[ -u FILE ] 如果 FILE 存在且设置了SUID位时返回为真。
[ -O FILE ] 如果 FILE 存在且属有效用户ID则返回为真。
[ -G FILE ] 如果 FILE 存在且默认组为当前组则返回为真。（只检查系统默认组）
[ -L FILE ] 如果 FILE 存在且是一个符号连接则返回为真。
[ -N FILE ] 如果 FILE 存在 and has been mod如果ied since it was last read则返回为真。
[ -S FILE ] 如果 FILE 存在且是一个套接字则返回为真。
[ FILE1 -nt FILE2 ] 如果 FILE1 比 FILE2 新, 或者 FILE1 存在但是 FILE2 不存在则返回为真。
[ FILE1 -ot FILE2 ] 如果 FILE1 比 FILE2 老, 或者 FILE2 存在但是 FILE1 不存在则返回为真。
[ FILE1 -ef FILE2 ] 如果 FILE1 和 FILE2 指向相同的设备和节点号则返回为真。


内容较多，如需查看链接
https://blog.csdn.net/wxx_0124/article/details/95305625

字符串判断

[ -z STRING ] 如果STRING的长度为零则返回为真，即空是真
[ -n STRING ] 如果STRING的长度非零则返回为真，即非空是真
[ STRING1 ]　 如果字符串不为空则返回为真,与-n类似
[ STRING1 == STRING2 ] 如果两个字符串相同则返回为真
[ STRING1 != STRING2 ] 如果字符串不相同则返回为真
[ STRING1 < STRING2 ] 如果 “STRING1”字典排序在“STRING2”前面则返回为真。
[ STRING1 > STRING2 ] 如果 “STRING1”字典排序在“STRING2”后面则返回为真。

数值判断

[ INT1 -eq INT2 ] INT1和INT2两数相等返回为真 ,=
[ INT1 -ne INT2 ] INT1和INT2两数不等返回为真 ,<>
[ INT1 -gt INT2 ] INT1大于INT2返回为真 ,>
[ INT1 -ge INT2 ] INT1大于等于INT2返回为真,>=
[ INT1 -lt INT2 ] INT1小于INT2返回为真 ,<
[ INT1 -le INT2 ] INT1小于等于INT2返回为真,<=

逻辑判断

[ ! EXPR ] 逻辑非，如果 EXPR 是false则返回为真。
[ EXPR1 -a EXPR2 ] 逻辑与，如果 EXPR1 and EXPR2 全真则返回为真。
[ EXPR1 -o EXPR2 ] 逻辑或，如果 EXPR1 或者 EXPR2 为真则返回为真。
[ ] || [ ] 用OR来合并两个条件
[ ] && [ ] 用AND来合并两个条件

 其他判断

[ -t FD ] 如果文件描述符 FD （默认值为1）打开且指向一个终端则返回为真
[ -o optionname ] 如果shell选项optionname开启则返回为真


 IF高级特性：
双圆括号(( ))：表示数学表达式
在判断命令中只允许在比较中进行简单的算术操作，而双圆括号提供更多的数学符号，而且在双圆括号里面的'>','<'号不需要转意。

双方括号[[ ]]：表示高级字符串处理函数
双方括号中判断命令使用标准的字符串比较，还可以使用匹配模式，从而定义与字符串相匹配的正则表达式。

双括号的作用：
在shell中，[ $a != 1 || $b = 2 ]是不允许出，要用[ $a != 1 ] || [ $b = 2 ]，而双括号就可以解决这个问题的，[[ $a != 1 || $b = 2 ]]。又比如这个[ "$a" -lt "$b" ]，也可以改成双括号的形式(("$a"
 < "$b"))

实例
1：判断目录$doiido是否存在，若不存在，则新建一个

if [ ! -d "$doiido"]; then
　　mkdir "$doiido"
fi

2：判断普通文件$doiido是否存，若不存在，则新建一个

if [ ! -f "$doiido" ]; then
　　touch "$doiido"
fi

3：判断$doiido是否存在并且是否具有可执行权限

if [ ! -x "$doiido"]; then
　　mkdir "$doiido"
chmod +x "$doiido"
fi

4：是判断变量$doiido是否有值

if [ ! -n "$doiido" ]; then
　　echo "$doiido is empty"
　　exit 0
fi

5：两个变量判断是否相等

if [ "$var1" = "$var2" ]; then
　　echo '$var1 eq $var2'
else
　　echo '$var1 not eq $var2'
fi

6：测试退出状态：

if [ $? -eq 0 ];then
    echo 'That is ok'
fi

7：数值的比较：

if [ "$num" -gt "150" ];then
   echo "$num is biger than 150"
fi

8：a>b且a<c

(( a > b )) && (( a < c ))
[[ $a > $b ]] && [[ $a < $c ]]
[ $a -gt $b -a $a -lt $c ]

9：a>b或a<c

(( a > b )) || (( a < c ))
[[ $a > $b ]] || [[ $a < $c ]]
[ $a -gt $b -o $a -lt $c ]

10：检测执行脚本的用户

if [ "$(whoami)" != 'root' ]; then
   echo  "You  have no permission to run $0 as non-root user."
   exit  1;
fi

上面的语句也可以使用以下的精简语句
[ "$(whoami)" != 'root' ] && ( echo "You have no permission to run $0 as non-root user."; exit 1 )

11：正则表达式

doiido="hero"
if  [[ "$doiido" == h* ]];then
    echo "hello，hero"
fi

============其他例子============
1、查看当前操作系统类型

#!/bin/sh

SYSTEM=`uname  -s`
if [ $SYSTEM = "Linux" ] ; then
   echo "Linux"
elif
    [ $SYSTEM = "FreeBSD" ] ; then
   echo "FreeBSD"
elif
    [ $SYSTEM = "Solaris" ] ; then
    echo "Solaris"
else
    echo  "What?"
fi

2、if利用read传参判断

#!/bin/bash
read -p "please  input a score:"  score
echo  -e "your  score [$score] is judging by sys now"
if [ "$score" -ge "0" ]&&[ "$score" -lt "60" ];then
    echo  "sorry,you  are lost!"
elif [ "$score" -ge "60" ]&&[ "$score" -lt "85" ];then
    echo "just  soso!"
elif [ "$score" -le "100" ]&&[ "$score" -ge "85" ];then
     echo "good  job!"
else
     echo "input  score is wrong , the range is [0-100]!"
fi

3、判断文件是否存在

#!/bin/sh
today=`date  -d yesterday +%y%m%d`
file="apache_$today.tar.gz"
cd  /home/chenshuo/shell

if [ -f "$file" ];then
    echo “”OK"
else
    echo "error  $file" >error.log
    mail  -s "fail  backup from test" loveyasxn924@126.com <error.log
fi

4、这个脚本在每个星期天由cron来执行。如果星期的数是偶数，他就提醒你把垃圾箱清理：

#!/bin/bash
WEEKOFFSET=$[ $(date +"%V") % 2 ]
if [ $WEEKOFFSET -eq "0" ]; then
   echo "Sunday evening, put out the garbage cans." | mail -s "Garbage cans out"  your@your_domain.org
fi

5、挂载硬盘脚本(windows下的ntfs格式硬盘)

#! /bin/sh
dir_d=/media/disk_d
dir_e=/media/disk_e
dir_f=/media/disk_f

a=`ls $dir_d | wc -l`
b=`ls $dir_e | wc -l`
c=`ls $dir_f | wc -l`
echo "checking disk_d..."
if [ $a -eq 0 ]; then
    echo "disk_d  is not exsit,now creating..."
    sudo  mount -t ntfs /dev/disk/by-label/software /media/disk_d
else
    echo "disk_d exits"
fi

echo  "checking  disk_e..."
if [ $b -eq 0 ]; then 
    echo "disk_e is not exsit,now creating..."
    sudo mount -t ntfs /dev/disk/by-label/elitor /media/disk_e
else
    echo  "disk_e exits"
fi

echo  "checking  disk_f..."
if [ $c -eq 0 ]; then
    echo  "disk_f  is not exsit,now creating..."
    sudo mount -t ntfs /dev/disk/by-label/work /media/disk_f
else
    echo "disk_f  exits"
fi




## sqlite 

在sqlite 中使用 .help 可以查看帮助文档
sql 语句安装语法需要; 结尾
读取数据库的操作，没有介绍，但是可以相信
通过搜索到的相关的信息，可以推断出第一种的使用方法

第二种方法，在观感上有些奇怪
在使用sqlite 命令的时候，感觉已经进入sqlite 环境
还能打开‘环境之外’的文件多少有点意外
但多少只是自己所理解，并非真是的情况

在sqlite 中无法使用常用的shell 命令也比较奇怪
主要还是因为可以读取文件却没法在sqlite 中直接查看
这可能时感到怪异的根源

可能有替换ls 的命令，还需测试测试
可以使用.cd 命令，但不知道如何确认是否正常
打开的数据库后，可以通过.databases查询已经打开的数据库的路径

sqlite3 x.db

sqlite3
>.open x.db

>.tables

> select * from post;


## gpg 

需要在系统中到处该环境变量，应该写入到bashrc 或 profile 文件中
在系统启动时可以到处，从而可以使用gpg 签名

export GPG_TTY=$(tty)

https://blog.csdn.net/qq_33154343/article/details/106030946

gpg 签名配置过程
https://gitee.com/help/articles/4248#article-header0 

 如何在 Gitee 上使用 GPG
GPG
GPG Key 生成与导出
Windows

    下载 https://gpg4win.org/

    生成 GPG Key

输入图片说明

输入用户名和邮箱，注意邮箱必须与 Gitee 提交邮箱一致

输入图片说明

    导出

输入图片说明
MacOS

    下载并安装 https://gpgtools.org/

    生成 GPG Key

输入用户名和邮箱，注意邮箱必须与 Gitee 提交邮箱一致

输入图片说明

    导出公钥

输入图片说明
Ubuntu 16.04/18.04

    安装

sudo apt install gnupg2  # Ubuntu 16.04
sudo apt install gnupg   # Ubuntu 18.04

    生成 GPG Key

$ gpg2 --full-gen-key     # Ubuntu 16.04 gpg 版本 < 2.1.17
$ gpg --full-generate-key # Ubuntu 18.04 gpg 版本 >= 2.1.17

请选择您要使用的密钥种类：
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (仅用于签名)
   (4) RSA (仅用于签名)
您的选择？ 1                                                   <- 选择密钥类型
RSA 密钥长度应在 1024 位与 4096 位之间。
您想要用多大的密钥尺寸？(3072) 3072
您所要求的密钥尺寸是 3072 位
请设定这把密钥的有效期限。
         0 = 密钥永不过期
      <n>  = 密钥在 n 天后过期
      <n>w = 密钥在 n 周后过期
      <n>m = 密钥在 n 月后过期
      <n>y = 密钥在 n 年后过期
密钥的有效期限是？(0) 1y                                       <- 有效期
密钥于 2020年05月04日 星期一 14时38分48秒 CST 过期
以上正确吗？(y/n) y                                            <- 确定

You need a user ID to identify your key; the software constructs the user ID
from the Real Name, Comment and Email Address in this form:
    "Heinrich Heine (Der Dichter) <heinrichh@duesseldorf.de>"

真实姓名： YOUR_NAME                                          <- 用户名
电子邮件地址： gitee@gitee.com                                 <- 邮箱，需要与 Gitee 提交邮箱保持一致
注释： Gitee GPG Key                                          <- 注释
您选定了这个用户标识：
    “YOUR_NAME (Gitee GPG Key) <gitee@gitee.com>”

更改姓名(N)、注释(C)、电子邮件地址(E)或确定(O)/退出(Q)？ O
gpg: 密钥 B0A02972E266DD6D 被标记为绝对信任
gpg: revocation certificate stored as 'xxx'
公钥和私钥已经生成并经签名。

pub   rsa3072 2019-05-05 [SC] [有效至：2020-05-04]
      8086B4D21B3118A83CC16CEBB0A02972E266DD6D                 <- Key ID
uid                      likui (Gitee GPG Key) <gitee@gitee.com>
sub   rsa3072 2019-05-05 [E] [有效至：2020-05-04]

    导出 GPG 公钥

gpg --armor --export 8086B4D21B3118A83CC16CEBB0A02972E266DD6D

GPG Key 配置与使用

    配置 Git

git config --global user.signingkey 8086B4D21B3118A83CC16CEBB0A02972E266DD6D

    添加到 Gitee 账户

输入图片说明

GPG 公钥验证状态，GPG 邮箱为当前用户已激活邮箱验证才能通过：

输入图片说明

    删除 仅移除 GPG 公钥，验证通过的 Commit 签名状态保持不变
    注销 移除 GPG 公钥并且将已验证的 Commit 签名状态修改为未验证

    使用 GPG 签名进行提交

git commit -S -m "YOUR COMMIT MESSAGE"
git log --show-signature # 查看签名状态

４．查看签名状态

输入图片说明

    Commit 验证通过的条件为：commit 提交邮箱与 commit GPG 签名所使用的公钥邮箱一致且GPG 公钥验证通过。

查看 GPG 公钥

    输入 https://gitee.com/\<username>.gpg

    选择用户个人资料右上角的设置页面进入安全设置 - GPG 公钥

    Gitee 平台 GPG 公钥: https://gitee.com/gitee.gpg



## git 使用

git config --global user.name "宋明亮"                                                              
git config --global user.email "songmingliang@uniontech.com"

mkdir remake-iso
cd remake-iso
git init 
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin git@gitee.com:DustMerlin/remake-iso.git
git push -u origin "master"

cd existing_git_repo
git remote add origin git@gitee.com:DustMerlin/remake-iso.git
git push -u origin "master"

fatal: 当前分支 master 没有对应的上游分支。
为推送当前分支并建立与远程上游的跟踪，使用

    git push --set-upstream origin master

创建develop 分支，以master 为基础，后期好合并回master 分支
git checkout -b develop master



## getopts 命令

如果需要快速读取参数来识别，这样一个功能
那么使用getopts 命令无疑是一个最好的选择

while getopts ":a:b:c" opt
do 
    case "$opt" in
	a) ARG=“${OPTARG}”;;
	b) ;;
	c) ;;
	?) ;;
    esac
done

以上为该代码的基本格式
通过getopts 读取命令行参数进行匹配
然后使用 $OPTARG 进行参数的读取 

格式： getopts optstring name [arg...]

如果需要读取命令行参数的值如 -a value 需要书写的optstring 格式为 a:
读取到的值会被存放在 OPTARG 变量中
如果optstrings 是以: 开头的，则optstring 中没有的参数将不会提示报错

目前getopts应该是只能识别单一的字符


getopts 过于副暂暂时不考虑
https://blog.csdn.net/weixin_43999327/article/details/118968405


## vim

``` bash 
?
# 把文件中的if都替换成 wj
:1,$s/if/wj/g 
:%s/if/wj/g


扩展资料：

1、将文中所有的字符串idiots替换成managers：

:1,$s/idiots/manages/g

也可以这么写：

:%s/idiots/manages/g

2、指定只在第5至第15行间进行替换，把dog替换成cat：

:5,15s/dog/cat/g

3、指定只在当前行至文件结尾间进行替换，把dog替换成cat：

:.,$s/dog/cat/g

4、指定只在后续9行内进行替换，把dog替换成cat：

:.,.+8s/dog/cat/g

https://www.zhongguojinrongtouziwang.com/business/202206/1328388.html

```

## git

### git stash

一、介绍

        git stash这个命令可以将当前的工作状态保存到git栈，在需要的时候再恢复。
二、使用场景

        当在一个分支的开发工作未完成，却又要切换到另外一个分支进行开发的时候，可以先将自己写好的代码，储存到 git 栈，进行另外一个分支的代码开发。这时候 git stash 命令就派上用场了！
三、常见方法：
1、git stash

        保存当前的工作区与暂存区的状态，把当前的修改的保存到git 栈，等以后需要的时候再恢复，git stash 这个命令可以多次使用，每次使用都会新加一个stash@{num}，num是编号
2、git stash save '注释'

        作⽤等同于git stash，区别是可以加⼀些注释， 执⾏存储时，添加注释，⽅便查找

git stash save 'test'

3、git stash pop

        默认恢复git栈中最新的一个stash@{num}，建议在git栈中只有一条的时候使用，以免混乱

        注：该命令将堆栈中最新保存的内容删除

4、git stash list

        查看当前stash的所有内容
5、git stash apply

        将堆栈中的内容恢复到当前分支下。这个命令不同于 git stash pop。该命令不会将内容从对堆栈中删除，也就是该命令能够将堆栈的内容多次运用到工作目录，适合用与多个分支的场景

        使用方法：git stash apply stash@{$num}
6、git stash drop 

        从堆栈中移除指定的stash

        使用方法：git stash drop stash@{$num}
7、git stash clear

        移除全部的stash
8、git stash show

     查看堆栈中最新保存的stash和当前⽬录的差异，显⽰做了哪些改动，默认show第一个存储

https://blog.csdn.net/lonely_fool/article/details/125681803


## popd pushd

https://www.zhangshilong.cn/work/97849.html

linux重命名文件夹命令,push和pop指令执行过程
admin 04-02 10:33 72次浏览

如在linux上执行过命令操作的人所知道的那样，目录切换用cd在频繁地在两个目录之间切换时被称为cd -

cd -为什么可以返回上一个目录？

效果与33558www.Sina.com/CD-CD$OldPwD相同

$ : CD工作/

~/work$:cd -

$:

$:cd -

~/work$ :

这样只能在两个目录之间切换。 那么，如果需要在多个目录之间进行进一步切换，该怎么办？ 一直是CD、CD、CD、

这个时候- 在此处等同于 $OLDPWD，保存了bash所记录的前一个目录，是个好选择

推式：将一个目录推入堆栈中进行保存，然后切换到该目录(方法与程序访问堆栈相同)

popd :离开堆栈，删除此最近的目录

dirs :存储在当前堆栈上的目录列表





https://www.qx6a.com/87884.html


Linux pushd/popd命令（pushd命令）

    LINUX
    1 个月前
    0
    37

cd Linux pushd/popd命令 pushd和popd是允许您使用目录堆栈并在Linux和其他类似Unix的操作系统中更改当前工作目录的命令 By myfreax 14 Aug 最新

pushd和popd是允许您使用目录堆栈并在Linux和其他类似Unix的操作系统中更改当前工作目录的命令。尽管pushd和popd是非常强大和有用的命令，但它们却被低估并且很少使用。

在本教程中，我们将向您展示如何使用pushd和popd命令导航系统的目录树。目录堆栈是您先前浏览过的目录的列表。使用dirs命令可以看到目录堆栈的内容。

使用pushd命令切换到目录时，目录会添加到堆栈中，而使用popd命令会从堆栈中删除目录。

当前工作目录始终位于目录堆栈的顶部。 当前工作目录是用户当前正在其中的目录文件夹。每次与命令行交互时，您都在一个目录中工作。

pwd命令可让您找出当前所在的目录。在文件系统中导航时，使用Tab键自动完成目录名称。在目录名称的末尾添加斜杠是可选的。

pushd，popd和dirs是shell内置程序，在不同的shell中其行为可能略有不同。我们将介绍命令的Bash内置版本。
pushd命令

pushd命令的语法是pushd [OPTIONS] [DIRECTORY]。其中OPTIONS是pushd命令的选项，DIRECTORY是可选参数，指定目录。

例如，要将当前目录保存到目录堆栈的顶部并同时切换到/var/www目录，您可以运行命令，这其实相当于使用cd命令切换目录：

    pushd /var/www

成功后，以上命令将打印目录堆栈。 ~是我们执行pushd命令的目录。~表示当前用户家目录。

pushd首先将当前工作目录保存到堆栈的顶部，然后切换到指定的目录。由于当前目录必须始终位于堆栈的顶部，因此更改后，新的当前目录将移至堆栈的顶部。

但不会保存在堆栈中。要保存它，您必须从中调用pushd。如果您使用cd切换到另一个目录，则堆栈的顶部将丢失。

pushd命令接受两个选项，+N和-N，可用于导航到堆栈的Nth目录。 +N选项更改为堆栈列表的Nth元素，从零开始从左到右计数。使用-N时，计数方向是从右到左。

为了更好地说明这些选项，请先运行命令dirs -l -v打印当前目录的堆栈，输出将显示目录堆栈的索引列表：

     0  /opt
     1  /usr/local
     2  /var/www
     3  /home/myfreax

如果要更改到/var/www目录，并将其移到堆栈的顶部。从上到下或从左到右计数时，目录的索引为2，请运行命令pushd +2

不带任何参数使用pushd时，将切换前上一目录，并使新的前一个目录成为当前目录。这与使用cd -命令时相同。

从下到上计数时，/var/www目录的索引为1，因此命令pushd -1。
popd命令

popd命令采用形式是popd [OPTIONS]。不带参数使用时，popd从堆栈中删除顶层目录，并导航到新的目录。

与pushd相同，popd也接受+N和-N选项，这些选项可用于删除堆栈的Nth目录。

假设我们有目录堆栈/opt /usr/local /var/www /etc/nginx ~。如果运行popd命令，它将从堆栈中删除/opt并切换到/usr/local目录。

    popd

输出将显示新的目录堆栈/usr/local /var/www /etc/nginx ~。

通常，您将使用cd命令从一个目录移动到另一个目录。但是，如果您在命令行上花费大量时间，则pushd和popd命令将提高您的生产率和效率。



## .gitignore

https://blog.csdn.net/nyist_zxp/article/details/119887324#2.1%C2%A0注释



Git 开发必备 .gitignore 详解！【建议收藏】
置顶
Linux猿
于 2021-08-24 13:05:38 发布 59555
收藏 393
分类专栏： Linux 技术 文章标签： git .gitignore .gitignore github gitlab git 管理
版权
华为云开发者联盟 该内容已被华为云开发者联盟社区收录，社区免费抽大奖🎉，赢华为平板、Switch等好礼！
加入社区
Linux 技术 专栏收录该内容
73 篇文章 130 订阅
订阅专栏

🎈 作者：Linux猿

🎈 简介：CSDN博客专家🏆，C/C++、面试、刷题、算法尽管咨询我，关注我，有问题私聊！

🎈 关注专栏：Linux （优质好文持续更新中……）🚀

目录

一、为什么使用 .gitignore ？

二、使用规则

2.1 注释

2.2 忽略文件

2.3 忽略目录

2.4 使用通配符

2.5 反向操作

2.6 双星号

2.7 其它规则

三、总结

在使用 git 管理项目过程中，.gitignore 文件是必备的文件，下面来详细说一说！
一、为什么使用 .gitignore ？

在一些项目中，我们不想让本地仓库的所有文件都上传到远程仓库中，而是有选择的上传，比如：一些依赖文件（node_modules下的依赖）、bin 目录下的文件、测试文件等。一方面将一些依赖、测试文件都上传到远程传输量很大，另一方面，一些文件对于你这边是可用的，在另一个人那可能就不可用了，比如：本地配置文件。

为了解决上述问题，git 引入了 .gitignore 文件，使用该文件来选择性的上传文件。
二、使用规则
2.1 注释

注释使用 # 开头，后面跟注释内容。如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件
out
*.exe
linuxy@linuxy:~/linuxGit$

上例中，以 # 开头的便是注释。
2.2 忽略文件

（1）忽略文件和目录

例如：folderName : 表示忽略 folderName 文件和 folderName 目录，会自动搜索多级目录，比如：*/*/folderName。

来看一个简单的例子，本地仓库的目录结构如下所示：

linuxy@linuxy:~/linuxGit$ tree
.
├── folder
│   └── file1
└── src
    ├── folder
    └── utils
        └── folder

3 directories, 3 files
linuxy@linuxy:~/linuxGit$

其中，.gitignore 文件内容如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件

folder
linuxy@linuxy:~/linuxGit$ 

故在本地仓库中，同名的 folder 目录、src/folder 文件、src/utils/folder 文件都会被忽略，即：不会被提交到远程仓库中。

（2）仅忽略文件

模式如下所示：

folderName

!folderName/

仅忽略 folderName 文件，而不忽略 folderName 目录，其中，感叹号“!”表示反向操作。

来看一个简单的例子，本地仓库的目录结构如下所示：

linuxy@linuxy:~/linuxGit$ tree
.
├── folder
│   └── file1
└── src
    ├── folder
    └── utils
        └── folder

3 directories, 3 files
linuxy@linuxy:~/linuxGit$

其中，.gitignore 文件内容如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件

folder
!folder/
linuxy@linuxy:~/linuxGit$

故在本地仓库中，src/folder 文件、src/utils/folder 文件会被忽略，而同名的 folder 目录不会被忽略。
2.3 忽略目录

模式如下所示：

folderName/

忽略 folderName 目录，包括：

（1）当前目录下的foldernName，例如：folderName/；

（2）多级目录下的 folderName，例如：*/*/folderName/；

来看一个简单的例子，本地仓库的目录结构如下所示：

linuxy@linuxy:~/linuxGit$ tree
.
├── folder
│   └── file1
└── src
    ├── folder
    └── utils
        └── folder

3 directories, 3 files
linuxy@linuxy:~/linuxGit$

其中，.gitignore 文件内容如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件

folder/
linuxy@linuxy:~/linuxGit$

故在本地仓库中，folder 目录会被忽略，而同名的 src/folder 文件和 src/utils/folder 文件不会被忽略。
2.4 使用通配符

常用的通配符有：

（1）星号“*” ：匹配多个字符；

（2）问号“?”：匹配除 ‘/’外的任意一个字符；

（3）方括号“[xxxx]”：匹配多个列表中的字符；

来看一个简单的例子，本地仓库的目录结构如下所示：

linuxy@linuxy:~/linuxGit$ tree
.
├── src
│   ├── add.c
│   ├── add.i
│   └── add.o
├── test.c
├── test.i
└── test.o

1 directory, 6 files
linuxy@linuxy:~/linuxGit$

其中，.gitignore 文件内容如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件

*.[io]
linuxy@linuxy:~/linuxGit$

故在本地仓库中，test.i文件、test.o文件、src/add.o文件、src/add.i文件会被忽略，而 test.c文件和add.c 文件不会被忽略。注意：这里忽略的匹配模式是多级目录的。
2.5 反向操作

模式如下所示：

!匹配模式 

表示之前忽略的匹配模式再次包含在跟踪内容里。

例如在仅忽略文件时提到的模式：

folderName

!folderName/

表示仅忽略 folderName 文件，而不忽略 folderName 目录。
2.6 双星号

斜杠后紧跟两个连续的星号"**"，表示多级目录。

来看一个简单的例子，.gitignore文件的内容如下所示：

linuxy@linuxy:~/linuxGit$ cat .gitignore 
# this is .gitignore file.
# 以下是忽略的文件

src/**/file
linuxy@linuxy:~/linuxGit$

可以表示忽略 src/folder1/file 、src/folder1/folder2/***/foldern/file 等。
2.7 其它规则

（1）空行不匹配任何文件；

（2）git 跟踪文件，而不是目录；

（3）在 .gitignore 文件中，每行表示一种模式；

（4）如果本地仓库文件已被跟踪，那么即使在 .gitignore 中设置了忽略，也不起作用。

（5）.gitignore 文件也会被上传的到远程仓库，所以，同一个仓库的人可以使用同一个.gitignore 文件。
三、总结

在使用 git 过程中，掌握 .gitignore 的使用很重要，可以减少不必要的文件上传到远程。



## json 字符串反序列化为对象 
http://www.techiedelight.com/zh/deserialize-json-string-into-python-object/

# 文件使用with 的方式打开，见 remake 项目的问题
将 JSON 字符串反序列化为 Python 对象

这篇文章将讨论如何将 JSON 字符串反序列化为 Python 对象。
1.使用 json 图书馆

这个想法是使用 loads() 从函数 json 将 JSON 字符串解析为 Python 对象的库。它提出了 JSONDecodeError 如果 JSON 字符串无效。

import json
 
if __name__ == '__main__':
 
    json_str = '{"name": "John", "age": 18}'
 
    obj = json.loads(json_str)
    print((obj['name'], obj['age']))    # ('John', 18)
 

下载  运行代码
2.使用 simplejson 图书馆

另一个简单的选择是使用 simplejson 库，它提供了显着的性能优势超过 json 图书馆。你可以使用它的 loads() 将字符串反序列化为 Python 对象的函数。该功能还提高了 JSONDecodeError 当 JSON 字符串无效时。

import simplejson
 
if __name__ == '__main__':
 
    json_str = '{"name": "John", "age": 18}'
 
    obj = simplejson.loads(json_str)
    print((obj['name'], obj['age']))    # ('John', 18)
 

下载代码
3.使用 ast 模块

另一种可行的方法是使用 ast.literal_eval 用于安全地将字符串评估为 Python 对象。这是一个工作示例：

import ast
 
if __name__ == '__main__':
 
    json_str = '{"name": "John", "age": 18}'
 
    obj = ast.literal_eval(json_str)
    print((obj['name'], obj['age']))    # ('John', 18)
 

下载  运行代码
4.使用 requests 图书馆

最后，如果你需要解析一个 HTTP 请求的响应，你可以使用 requests 库，如下图：

import requests
 
if __name__ == '__main__':
 
    url = "https://jsonplaceholder.typicode.com/todos/1"
 
    obj = requests.get(url).json()
    print(obj)


### json 



json文本的反序列化,转化为python对象
单叼红中
于 2022-08-24 22:55:53 发布 166
收藏
文章标签： json
版权

#1.json文本在内存中存在

import json

x='{"name": "kevin","age": 18}'   #json文本

#如何把json文本转化成python对象(字典)

result=json.loads(x)  #转化成字典dict

print(type(result))   #查看类型

#2.json文本在本地磁盘文件中存在

import json

with open("test_dataa.json", mode="rt", encoding="utf8") as x:

    result=json.load(x)  #转化成字典dict

    print(type(result))  #查看类型

#3.json文本在从网络HTTP响应中获取,涉及到网络io

import requests

url = "http://120.24.208.55:8080/admin/login"

payload = {
            "password": "macro123",
            "username": "admin"
          }

res=requests.post(url=url,json=payload).json()    #获取HTTP中响应body的json文本,自动的帮助转化成python对象

print(type(res))#查看类型

https://blog.csdn.net/liuaoxiang/article/details/126514410 

# 可能并不好用
https://blog.csdn.net/qq_58635232/article/details/127742509


## python 字符串匹配

Python字符串匹配—-6种方法的使用「建议收藏」
发布于2022-09-01 16:27:44阅读 4130

大家好，又见面了，我是你们的朋友全栈君。

1. re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none。

import re

line="this hdr-biz 123 model server 456"
pattern=r"123"
matchObj = re.match( pattern, line)

2. re.search 扫描整个字符串并返回第一个成功的匹配。

import re

line="this hdr-biz model server"
pattern=r"hdr-biz"
m = re.search(pattern, line)

3. Python 的re模块提供了re.sub用于替换字符串中的匹配项。

import re

line="this hdr-biz model args= server"
patt=r'args='
name = re.sub(patt, "", line)

4. compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用。

import re

pattern = re.compile(r'\d+') 

5. re.findall 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。

import re

line="this hdr-biz model args= server"
patt=r'server'
pattern = re.compile(patt)
result = pattern.findall(line)

6. re.finditer 和 findall 类似，在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。

import re

it = re.finditer(r"\d+","12a32bc43jf3")
for match in it:
  print (match.group() )

发布者：全栈程序员栈长，转载请注明出处：https://javaforall.cn/140950.html原文链接：https://javaforall.cn

# in 关键字判断
https://m.elecfans.com/article/1815106.html
