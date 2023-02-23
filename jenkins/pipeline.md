# pipeline 

## agent

agent any

定义执行节点，有且仅有以下方式，企鹅必须使用',"暂未尝试，不知效果是否一致
agent { label 'host-master'}

## stages
    嵌套或多个并行 stage

### stage('name')

#### steps 
具体执行的步骤，可以多个

sh "remake-iso.sh"

> Jenkins 特有的环境变量输出，在其他环境无法执行
sh "printenv"

sh "/usr/bin/python3 pyhton/deal_json.py"

    使用上述方法执行python脚本，其余方式均不可行
    必须给出可以执行的绝对路径，实际还是以shell的方式执行
    不能直接使用python 命令执行

    但是可以嵌套，在shell 写好脚本，去执行python
    但仅在执行一句的情况下，使用sh 执行对应文件更简单

    以上操作都是在从节点的主机环境中执行
    所以需要执行额外的命令，需要在该环境中安装相应的软件包，提供相应的功能

参考资料：
https://www.jenkins.io/doc/book/pipeline/

https://www.51cto.com/article/684741.html

https://weread.qq.com/web/reader/12f320007184556612f32b6k1ff325f02181ff1de7742fc