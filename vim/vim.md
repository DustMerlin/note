# vim

vim 自定义配置，插件

## 需求

今天写Jenkinsfile 使用vim tab 太长了
而且没有高亮插件，检测

如果能开发一个对应的功能还不错，可以熟悉一下vim插件的开发

但是还是先检索一下有没有现成的功能可以直接实现

## 解决 tab 问题

修改 ～/.vimrc 
添加 set tabstop=4 4空格=tab

!!该文件只和vim显示有关,并不会影响文件本身内容