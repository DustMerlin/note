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

## git merge

场景： 当本地修改push 到远端后，有想修改一些内容并追加到上一个commit 中

面对这种情况，目前我认知里有两种方式可以解决：
1.  git add ./git add -u
    git commit --amend
    git push -f
    以上这种情况可能会覆盖远程的仓库，不建议如此使用
    但是像gerrit amend 之后push 并不会冲突，因为commit 在审核阶段，并未真正的merge
    （gerrit 说法存疑，暂时暂时先这样，也懒得研究）

>    但一般情况下，可能并没有权限，或者为保护分支，或者明令要求不能使用-f 强制推送仓库，导致远端的存储仓库被强制覆盖

2.  所以第二种方式,当然git pull 操作是必要的
    在写代码前也应该如此，同步代码之后，合并冲突的该率会减小很多，但是多人协作免不了合并冲突

    git pull 合并冲突时会有提示

    根据冲突文件的标识，去做相应的修改,冲突标识如下
    >>>
    ===
    <<<
    仅需选定自己需要保留，删除标识和其他不需要内容即可

    git add 之前修改了的冲突的文件

    git merge --abort 会放弃当前的merge操作
    如果确定无误使用
    git merge --continue（该操作和cherry-pick 的操作极为相似，联系cherry-pick 操作时，也会用到）

    此时就会有一条merge 记录生成，git push 也可以成功了，因为我们已经解决了冲突了

    9e7f2d0 (HEAD -> main, origin/main) Merge branch 'main' of github.com:DustMerlin/note into main
    c8e2ffc vim settabstop
    95161ca vim settabstop


    commit 9e7f2d0a143b0c51773be414368e15e16b47a827 (HEAD -> main, origin/main)
    Merge: c8e2ffc 95161ca
    Author: MerlinDust <MerlinDust@foxmail.com>
    Date:   Fri Feb 24 10:01:41 2023 +0800

        Merge branch 'main' of github.com:DustMerlin/note into main

merlin@merlin:~/Documents/note$ git log -n5 --graph --oneline
*   9e7f2d0 (HEAD -> main, origin/main) Merge branch 'main' of github.com:DustMerlin/note into main
|\  
| * 95161ca vim settabstop
* | c8e2ffc vim settabstop
|/  
* 2afab72 some jenkins note
* 0c2ea37 anaconda and software_selection(tui)

从图形上看，是从main merge 到 origin/main

## git new branch to push origin 

    git push --set-upstream origin test

## 关联远端分支（自己瞎起的名字，而且可能还使用不成功）

    git branch -u origin/main

    执行此命令，需要注意当前所在的分支,可能需要一个远端存在的分支？
    此处再测试一下，但是并不过度深入，目前使用的场景不多，暂时不需要那么细致的了解
    测试结果： 当远端的分支不存在时，不能将本地的分支与远端不存在的关联
    所以还是需要使用 git push -u origin test 先推送test 分支
    
    git branch -u 的操作，应该是可以本地与远端项目关联的，仅为推测，不确定

    但是本地分支推动到远端的时候
    还是需要使用上一节中使用的命令,git push -u origin branch_name
 
    -u , --set-upsteream 的 缩写 

    可以显示 本地分支和远端分支的对应
    git branch -vv 
    * main 7c8508e [origin/main] set origin branch and push

    git branch -av
    * main                7c8508e set origin branch and push
    remotes/origin/main 7c8508e set origin branch and push

    使用git push -u oringin test 
    然后使用git branch -vv 
    即可看到 本地分支和远端分支的关联