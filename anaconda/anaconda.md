# anaconda 启动过程分析

sw 架构，图形无法启动，在该背景下不得不研究一下启动的过程，
好最终确定无法启动的原因

## anaconda 图形启动简要过程分析
核心内容为图形启动过程，终止到报错出现，未过度深入分析，
仅对过程有个大致了解，确定必要的参数作用和传递路径

### 代码分析

``` python
anaconda.py 

# anaconda 对象初始化
anaconda = Anaconda()

# 获取内核命令行参数
(opts,depr) = parse_arguments(boot_cmdline=kernel_arguments)
anaconda.set_from_opts(opts)

# 从内核命令行参数中获取ks 文件，如果存在的话
kspath = startup_utils.find_kickstart(opts)
ksdata # 上述路径获取ks 数据
anaconda.ksdata = ksdata
anaconda.payload.set_from_opts(opts)

··· 上述过程为可能必要的初始化参数，需要了解，一下直接跳转到图形部分

#anaconda.py +530
# 启动图形
display.setup_display(anaconda,opts)

#display.py +325
# 执行额外的图形操作
do_extra_X11_actions(options.runres,gui_mode=anaconda.gui_mode)

#display.py +194
# 使用子进程执行xrdb ，该命令由于文件不存在有报错，但是并非图形无法启动的核心原因
util.execWithRedirect("xrdb",["-nocpp","-merge","/etc/X11/Xresources"])

# 而报错则在上述子进程执行到等待命令结束时报错
# 进而很容易被误导，以为是xrdb报错导致，而其在日志中也有报错信息，

# 契机，在某次重复启动后，看到新的警告，gtk缺少符号，而不报错，则很奇怪
# 且出现了报错中一直出现的一个词 metacity,此前一直以为该名词仅为报错信息

# 在翻看 进程检测代码后，确定了报错的进程即为 metacity 进程
# process_watchers.py +79   
exn_message.append("%s exited %s" % (proc_name, status_str))

# 在代码中直接搜索metacity 
# display.py +167
childproc = util.startProgram(["metacity", "--display", ":1", "--sm-disable"],
                                  env_add={'XDG_DATA_DIRS': xdg_data_dirs})

# 且在安装环境中执行 metacity 也报出缺少符号的错误
# 基本可以断定是该处的问题，导致的目前的错误，但并不能保证解决之后没有其他的错误

```
### 问题分析

经过代码分析和测试之后，基本可以断定目前的问题所在

现在的问题就是metacity 调用的gtk 的gdk.so 需要 wl_proxy_marshal——flags

该符号 查阅到仅在1.20版及以上的wayland 中提供，

此时可以有三种想法：

metacity 问题
gtk 问题
wayland 问题

其实前两个无需考虑，但是做测试浪费了许多时间，
虽然现在这样说，但是认知里代码都源自euler
所以这三个应该都是一模一样，但是从符号出处来说
其他两个之间调用也无问题，wayland 出问题的概率更大

最终确定wayland 被改造过，使用euler的wayland 包成功解决问题

### 总结

报错信息可能包含核心的信息，所以先找到报错信息的出处
然后确定启动报错信息中变量的来源，可能可以更快定位问题

由于代码过多，类似上述浏览式的代码分析，可以应付很多问题场景
如果挨着顺序去看，或许能更早发现与metacity类似xrdb 的调用
去怀疑到问题的关键，但是时间不那么允许

有时想省时间，但却会消耗更多的时间，这本就是一个很难平衡的过程
毕竟永远不知道自己使劲的方向对不对，很可能一切都是白搭