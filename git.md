# git 总结

## 日常使用补充

NAME
git-describe - Give an object a human readable name based on an available ref

SYNOPSIS
git describe [--all] [--tags] [--contains] [--abbrev=<n>] [<commit-ish>…​]
git describe [--all] [--tags] [--contains] [--abbrev=<n>] --dirty[=<mark>]
git describe <blob>

git describe命令显示离当前提交最近的标签。
使用语法
git describe [--all] [--tags] [--contains] [--abbrev=<n>] [<commit-ish>…​]
git describe [--all] [--tags] [--contains] [--abbrev=<n>] --dirty[=<mark>]


描述该命令查找从提交可访问的最新标记。 如果标签指向提交，则只显示标签。 否则，它将标记名称与标记对象之上的其他提交数量以及最近提交的缩写对象名称后缀。
默认情况下(不包括--all或--tags)git描述只显示注释标签。

示例如果符合条件的tag指向最新提交则只是显示tag的名字，否则会有相关的后缀来描述该tag之后有多少次提交以及最新的提交commit id。不加任何参数的情况下，git describe 只会列出带有注释的tag
$ git describe --tags
tag1-2-g026498b
Shell
2:表示自打tag tag1 以来有2次提交(commit)g026498b：g 为git的缩写，在多种管理工具并存的环境中很有用处；
//更多请阅读：https://www.yiibai.com/git/git_describe.html

