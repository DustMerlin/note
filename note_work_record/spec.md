https://gitlabxa.uniontech.com/ut001698/rpmspecsample/-/blob/master/SuperSample.spec


# 创建 Spec 文件常见问题示例以及解决办法

# spec 文件格式
# spec 文件需要使用空格对齐，以本 spec 文件为例，全局变量定义和标签式文本定义，可以按照列来对齐

# ========== rust ==========
# 宏 __cargo 描述了 cargo 编译命令，包括 cargo_home 的定义，但是默认宏文本中不包含 -verbose 参数，我们往往需要编译过程输出详细信息，供问题定位，
# 可以通过如下方式修改 __cargo 宏，添加 -vv 来输出详细的 cargo 编译日志
%global         __cargo             %{?__cargo:%{__cargo} -vv}%{!?__cargo:%{_bindir}/env CARGO_HOME=.cargo RUSTC_BOOTSTRAP=1 %{_bindir}/cargo -vv}
# cargo 有一个内置的 %cargo_build 宏，这个宏是否可执行，受 __cargo_skip_build 变量影响，
# 需要在 spec 文件开头的位置设置这个变量的值为 0 来保证正确调用 cargo 命令编译 rust 项目。
%global         __cargo_skip_build  0

# ========== debug package ==========
# 某些语言的包可能不适合或者不能被 strip 命令处理来获取调试符号，可以使用如下命令来禁止 rpm 编译完成之后的 debug 包抽取生成，例如： rust、golang、java
# 注意：除非 C/C++ 的包具有极其复杂的 Makefile 文件，难以在编译参数中添加 -g 选项，或者难以修改 install 流程不使用 --strip 参数，否则禁止使用该指令。
# golang 不能生成 debug 信息的原因： rpm-build 工具包提供的 /usr/lib/rpm/debugedit 工具从二进制文件中读取 'BuildID[.*]' 时读取不到信息，因为 golang
# 的二进制文件中这个值是 'Go BuildID'，不符合 debugedit 工具检查规则。
%global         debug_package       %{nil}

# ========== nodejs ==========
# nodejs 的包有一个实际的名字，此处示例使用 echarts。实际名称定义使用如下指令：
# rpm 包名应为 nodejs-echarts，即定义 Name 为 nodejs-%{packagename}
%global         packagename         echarts

# ========== python ==========
# 某些软件包附带有一些 python 脚本，这些脚本被复制到 %{buildroot} 目录，install 流程结束之后，rpmbuild 系统会自动调用 brp-python-bytecompile 对 %{buildroot} 目录
# 中的 python 脚本进行编译操作，但是某些脚本此时可能不适合被编译，导致编译报错失败，可以使用如下指令禁止 install 流程之后编译 python 脚本：
%global         __os_install_post   %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
# python 的包有一个实际的名字，此处示例使用 kazoo，实际名称定义使用如下指令：
# rpm 包名应为 python-kazoo，即定义 Name 为 python-%{pypi_name}
%global         pypi_name           kazoo

# ========== github 项目 ==========
# 没有版本号或者使用某个正式版本之后的 commit 做源码
# 参考如下指令，从确切 commit 号上摘取前7位拼接 commit date 作为 spec文件中的 release 号的结尾
%global         commit              8678969f02c4679fa40abaa9c5d7afadec50ed84
%global         commit_date         20191219
%global         shortcommit         %(c=%{commit}; echo ${c:0:7})
%global         alphatag            .%{commit_date}git%{shortcommit}


# ========== bcond_with(out) ==========
# 只有 rpmbuild 命令带有 --with cond1 参数时，spec 中 %{?with_cond1} 是 1，其余情况都是 0
%bcond_with     cond1
# 只有 rpmbuild 命令带有 --without cond2 参数时，spec 中 %{?with_cond2} 是 0，其余情况都是 1
%bcond_without  cond2


# ========== 多行文本 ==========
# 多行文本指定折行是，参照如下写法，line1 结束则按 Enter 键继续再写 line2，一般用于描述 package 的 description
%global         multiline_text      %{expand:line1
line2.}
# 一行命令过长，需要折行并续接，写完一部分之后 使用两个 \ 符号然后按 Enter 键再继续写，宏展开之后每行后面都有一个 \ 被解释为连行符
%global         multiline_text      %{expand:begin... \\
...end}


# ========== 宏函数 ==========
# spec 文件中可能会出现多个子包具有逻辑顺序几乎相同的命令调用，此时可以通过定义一个全局函数的方式来代替高度相似性代码，定义函数的方式如下所示
# setup_mod 就是函数名，后面的 %{expand:******} 是函数体，函数体中的 %1 与 shell 函数的 $1 一样，代表第一个参数
%define         setup_mod()         %{expand:find %{_localstatedir}/log/%{name}/%1 -mindepth 1 -type d -exec chmod 775 {} \\;
find %{_localstatedir}/log/%{name}/%1 -type f -exec chmod 664 {} \\;}


# ========== jar包扫描 ==========
# mvn 构建时安装了 javapackages-local 作为编译依赖的时候，编译完成之后，会使用工具从 jar 包里面扫描 provides 和 requires，
# 请注意，除非你打包的 java 包是公共能力提供者，否则一定要添加如下两行定义，避免生成的 rpm 包提供符号与 java 公共能力提供者对应的包冲突
%undefine       __osgi_provides
%undefine       __osgi_requires


# ========== 依赖缺失导致 mvn_install 失败
# mvn_install 在安装 jar 包之后，会解析依赖，如果在编译环境中找不到所需依赖，该命令会直接失败，在无法引入大量依赖的情况下，可以禁用依赖扫描。
%undefine       __maven_requires


# ========== ldconfig ==========
# 某些软件包安装卸载之后需要运行 ldconfig，此时切记只能调用 ldconfig，而不能调用 /sbin/ldconfig 或者 /usr/sbin/ldconfig
# yum 源上 glibc 仅提供 ldconfig 符号，spec 文件中使用 /path/to/cmd 要求该全路径式文件必须有包显式提供才可以。
%define         post_ldconfig       %{expand:ldconfig || :}
%define         postun_ldconfig     %{expand:ldconfig || :}


# ========== exclude requires ==========
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/
# 软件包安装在 /usr/lib64 目录中的 *kim*.so* 文件不显示在 provides 列表中
%global         __provides_exclude_from     %{?__provides_exclude_from:%{__provides_exclude_from}|}^(%{_libdir}/.*kim.*\\.so|%{_libdir}/.*kim.*\\.so.*)$
# 软件包对 libmesos-protobufs.so, libporotobuf.so, libmesos.so*, ..., libglog.so* 等的依赖不显示在 requires 列表中
# PLEASE NOTE: 每行不要超过两个屏蔽项，超过两个屏蔽项的时候，拆行写就都可以识别。单行过长疑似会发生屏蔽失效问题，不确定原因。
%global         __requires_exclude          %{?__requires_exclude:%{__requires_exclude}|}libmesos-protobufs.so|libprotobuf.so
%global         __requires_exclude          %{?__requires_exclude:%{__requires_exclude}|}libmesos.so*|libprocess.so*
%global         __requires_exclude          %{?__requires_exclude:%{__requires_exclude}|}libev.so*|libglog.so*
# 过滤掉 libstdc++.so.6(GLIBCXX_3.4.26)(64bit)
%global         __requires_exclude          %{?__requires_exclude:%{__requires_exclude}|}libstdc\\+\\+\.so\.6\\(GLIBCXX_3\.4\.26\\)\\(64bit\\)
# 使软件包不提供 libkim-api.so 相似的符号
%define         __provides_exclude          %{?__provides_exclude:%{__provides_exclude}|}libkim-api.so*
# 某些二进制编译出来之后，在自动扫描依赖阶段，会报告依赖 libc.so.6(GLIBC_PRIVATE)(64bit), glibc 不对外提供该私有符号，添加如下指令屏蔽Requires中的该项
%global         __filter_GLIBC_PRIVATE      1
# ========== 多线程编译 ==========
# %make_build 中默认有指定 -j N, 虚拟机上面没有指定 RPM_BUILD_NCPUS 时，N 默认为 1, 编译很慢，使用如下语句使用 cpu 数量个线程编译
# 注意：这是一个shell指令，请在 rpmbuild -bb/-ba 命令之前执行。
export RPM_BUILD_NCPUS=$(nproc)


# ========== 基本信息 ==========
# 最终生成 rpm 包的主包名，可以控制不生成主包。
Name:           SuperSample
# 开源软件的 release 版本号，如果是无 release 号的 github 项目，可以使用 0 作为版本号，可以保证项目有正式 release 之后的平滑升级
Version:        1.0.0
# 无 release 号的 github 项目，后面跟拼接的 git commit。前面的 1 在每次更新 spec 文件或者软件新增 patch 等操作之后需要 +1
# 一般软件包的 release 号不要带 %{?alphatag}。alphatag 变动的时候，左侧 release 前缀也要变更
# 注意：欧拉版上开发 rpm 软件包，不需要 %{?dist}，这是默认自动添加的。主动添加会导致产品标识重复出现在 rpm 包名上。
Release:        1%{?alphatag}
# 一个简短的软件描述，不允许使用句号结尾。
Summary:        short message
# 本地化配置，括号中写语言简写。支持项应存在于 /usr/share/locale
Summary(zh_CN): 中文的短描述
# License 缩写优先参考开源许可名录： https://opensource.org/licenses/alphabetical
# 开源许可名录中没有收录的 License 请参考：https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# 如果上述两个 URL 中无法找到对应 License，请考虑引入该软件是否会带来法律风险。
License:        Apache-2.0
# 注意： URL 和 Source0 标签值中与 Name 相同大小写的单词请使用 %{name} 替代，版本号使用 %{version} 替代
# URL 请提供软件供应商的网址，如果软件是托管在开源代码平台，没有官方网站，请写软件仓库地址
URL:            https://github.com/alibaba/canal.git
# Source0 是软件主源码包的合法下载地址。使用解析后的 URL 字符串，应该可以直接使用 wget 工具下载到对应文件。
# github 项目常见问题：实际 URL 下载到的文件名是扩展文件名，例如： 通过 https://xxxxxxx/v1.0.0.tar.gz 下载得到的是 name-1.0.0.tar.gz
# 可以修改 Source0 为：https://xxxxxxx/v1.0.0.tar.gz#/name-1.0.0.tar.gz
# 注意： Source0...999 如果是 URL 式的，则是取最后一个 / 之后的文本作为文件名来查找文件，否则认为整串文本都是文件名
Source0:        https://github.com/cloudflare/%{name}/archive/%{name}-%{version}.tar.gz
# node.js 软件包打包时，部分包可能是与架构无法的，此时不需要从 github 等代码托管平台下载源码，而是从 npmjs.org 下载源码，url 如下：
Source0:        https://registry.npmjs.org/%{packagename}/-/%{packagename}-%{version}.tgz
# 外部扩展资源，软件功能增强、附加配置文件等使用 Source1...100 引入 *.src.rpm。接受 URL 式文件名。
Source1:        name.conf
# 对开源代码做适配或者功能修复、增强等，使用 patch 文件而不是修改源码包或者在 prep、build 等阶段使用 sed 等文本编辑命令修改源文件。
# patch 文件编号必须从 0 开始，后续可以依次递增。特殊目的的 patch 文件，可以另起一个编号段，例如: Patch100...199
Patch0:         fix-issues-xxxxx.patch

# ========== 编译和安装依赖 ==========
# 可以禁止 rpmbuild 系统自动扫描安装依赖和提供符号列表。通过设置如下三个选项值为 no 可以达到目的。
# 使用 AutoReqProv 时，不要再使用 AutoReq 和 AutoProv。AutoReq 和 AutoProv 可以单独或一起使用。
# 禁止自动扫描安装依赖和提供符号列表。选项默认值 yes
AutoReqProv:    no
# 禁止自动扫描安装依赖。选项默认值 yes
AutoReq:        no
# 禁止自动扫描提供符号列表。选项默认值 yes
AutoProv:       no

# 编译软件包时，编译环境需要具备的条件。尽量主动声明必备的编译依赖，不要依赖编译系统的默认配置。已知依赖包间自带依赖关系的包，可以不用全部列出
# 不要使用文件名作为编译依赖描述，而是提供这个文件的具体包名。例如：需要 /usr/sbin/useradd 文件，应该引入 shadow 包，而不是直接写文件全路径
BuildRequires:  gcc
# 使用 cmake 构建软件包，请引入下面的软件包，提供 cmake 编译宏
BuildRequires:  cmake-rpm-macros
# 编译 node.js 语言的包，请引入下面的软件包，提供 npm 编译宏
BuildRequires:  nodejs-packaging
# 编译 rust 语言的包，请引入下面的软件包，提供 rust 编译宏
BuildRequires:  rust-packaging
# 使用 mvn 编译，请引用如下编译依赖
BuildRequires:  maven-local
# 如果需要使用 mvn 宏，请引入下面的软件包，提供修改 pom 文件的宏：
BuildRequires:  javapackages-local
# 使用 ant 编译，请引用如下编译依赖
BuildRequires:  ant
# 编译 java 语言的包，还需要引入 java-devel，java 版本根据实际要求
BuildRequires:  java-1.8.0-devel
# 移除依赖。示例：安装 maven 会自动安装一些依赖包，但是该依赖包可能导致目标项目无法正常构建，需要在线重新下载该依赖包，可以使用 - 来删除该依赖，
# 效果等同与在环境中执行了 rpm -e --nodeps maven-artifact-transfer
BuildRequires:  -maven-artifact-transfer

# 软件安装依赖，可以认为是软件在环境中运行所需的依赖。请确保写在此处的包的确是软件运行所需，如果软件运行不需要该包，请不要列在此处
# 如 glibc 这种操作系统运行必备的软件包，不要列在此处，这是冗余的，示例为显式列出运行依赖
Requires:       zlib

# java 语言编写的软件包，请显式声明如下安装依赖
Requires:       javapackages-tools
# java 语言编写的软件包，需要提供 java 运行环境的，请声明如下安装依赖：
Requires:       java-1.8.0-headless
# 还有一些 java 语言软件包，可能需要用到 jps 等工具，需要安装 java-devel 包
Requires:       java-1.8.0-devel

# node.js 软件包，如果没有自动扫描到如下依赖，请显式声明：
Requires:       nodejs(engine)

# 不同架构可能需要不同的编译/安装依赖，使用 ifarch 做架构判断来提供对应依赖项
%ifarch aarch64
Requires:       edk2
%endif

%ifarch x86_64
Requires:       edk2-ovmf
%endif

# 提供 *.service 文件的软件包，即支持使用 systemd 作为服务管理工具的软件包，务必引入如下宏：
%{?systemd_requires}


# python、java、perl、nodejs、shell 等解释性语言可能需要编译为 noarch 的，即与架构无关
# 但是 python、nodejs 的软件包可能需要依赖 gcc/g++ 编译，这些包不要标记为 noarch 的。
BuildArch:      noarch
# 指定需要编译目标架构，编译环境架构不在该列表中的，不会触发编译操作。注意：UnionTech OS 中 ExclusiveArch 和 BuildArch 不能一起出现。
ExclusiveArch:  x86_64 aarch64

# ========== 冲突与废弃 ==========
# 指明本软件包与 sample2 不能共存
Conflicts:      sample2
# 指明本软件包与低于 1.5.0 版本的 sample3 不能共存
Conflicts:      sample3 < 1.5.0
# 注意：一般不要使用上面示例的冲突声明，应该使用依赖高版本来解决这种冲突问题
Requires:       sample3 >= 1.5.0
# 本软件包可能做了功能增强，现在可以提供 sample-tools > 2.1.0 的功能，单独的 sample-tools <= 2.1.0 的包不再需要，可以声明废弃
# 注意，软件包中声明 obsoletes 会导致被废弃的包无法通过 yum 源安装，通过 yum install sample-tools 安装的将会是当前包
Obsoletes:      sample-tools <= 2.1.0

# ========== 辅助功能 ==========
# 弱依赖
# 失去某些依赖后软件包的功能仍然正常可用，不会导致依赖关系断裂造成功能异常，区别如下：
# sample4 在 yum 源找不到或者已损坏，不影响 yum 安装主包
Recommends:     sample4
# yum 安装完成之后，可以卸载 sample5，不会导致主包被卸载
Supplements:    sample5

# 更弱依赖
# 一般做功能补充，功能增强，如plugins、addon，区别如下：
# 主包的运行如果有 sample6 的加入会更好用，使用 Enhances，yum 源上找不到 sample6 不会影响主包安装
Enhances:       sample6
# 主包运行依赖有多个包可以提供，使用 Suggests 建议 yum 优先选择 sample7 作为依赖提供者
Suggests:       sample7

# 主包的长描述，必须主动进行文本换行，每行文本长度不要超过80字符，因为某些单词过长，可以容忍超出几个字符。
%description
Long description.

%description -l zh_CN
中文的长描述。

# ========== 子包声明 ==========
# 两种方式声明子包名称，一种是后缀式，一种是全新声明，区别在于是否使用 -n 选项，如下：
# %package subpkg：后缀式，生成的包名是 %{name}-subpkg
# %package -n subpkg: 全新声明，生成的包名是 subpkg

# ========== python子包 ==========
# 子包声明
# 注意：除非无法替代，否则不得引入 python2 版本的包
%package        -n python3-%{pypi_name}
# 子包的简短描述，不允许使用句号结尾。
Summary:        %{name}'s python module subpackage
# 如果必要，需要依赖主包，如果主包是指定架构编译，即非 noarch 的，需要使用如下方式引用：
Requires:       %{name}%{_isa} = %{version}-%{release}
# 主包与架构无关，使用如下方式引用：
Requires:       %{name} = %{version}-%{release}
# 子包的长描述
%description    -n python3-%{pypi_name}
Long description for python module subpackage.


# ========== 开发用子包 =========
# 子包声明，生成 name-devel 的 rpm 包，该包用于保存编译软件生成的 动态库和头文件 等
%package        devel
# 子包的简短描述，不允许使用句号结尾。
Summary:        Development files for %{name}
# 编译当前子包需要的依赖项，不安装该包不影响其他包编译
# 使用场景：子包是条件式编译，条件不满足则不生成当前子包，此时编译环境不安装该依赖包，节省编译环境开销
BuildRequires:  dfc-devel
# 注意： 某些软件的开发用子包不需要依赖主包，可以单独安装到操作系统中，仅供开发使用，请根据实际情况决定是否在此处依赖主包
# 开发用子包一般需要依赖主包，使用如下依赖声明:
Requires:       %{name}%{_isa} = %{version}-%{release}
# 子包的长描述
%description    devel
Long description for development subpackage.


# ========== 静态库子包 ==========
# 子包声明，生成 name-static 的 rpm 包，该包用于保存编译软件生成的 静态库 文件
%package        static
# 子包中允许单独设置版本号
Version:        subpackage-version
# 子包的简短描述，不允许使用句号结尾。
Summary:        %{name}'s static library subpackage
# 静态库子包一般需要依赖 devel 包(供开发人员使用需要有头文件)，使用如下依赖声明
Requires:       %{name}-devel%{_isa} = %{version}-%{release}
# 子包的长描述
%description    static
Long description for static library subpackage.


# ========== 文档子包 ==========
%package        doc
Summary:        documentation of package
# 可以在文档子包中声明生成文件与架构无关
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
Long description for doc subpackage.


# ========== Javasdoc ==========
%package        javadoc
Summary:        Javadoc for %{name}
Requires:       javapackages-filesystem
BuildArch:      noarch

%description    javadoc
This package contains the API documentation for %{name}.

# ========== 准备阶段 ==========
# setup 与 autosetup 二选一
%prep
# ========== autosetup ==========
# 解压 Source0 等源码包，默认解压 Source0，并自动应用补丁，额外参数：
# -pn  : 跳过 n 个路径前缀应用补丁
# -n   : 后续每一构建步骤的起始路径。源码包解压后目录不是 %{name}-%{version} 的，需要重新指定
# -c   : 源码包解压后不是一个目录，而是多个目录，使用该参数指定一个文件夹名，将解压后的文件存入该文件夹中。
# -a   : 切换目录后，解压指定序号的 Source [after]；
# -b   : 切换目录前，解压指定序号的 Source [before]；
# -T   : 禁止自动解压归档，可配合 -a 使用， -a 可重复出现
# -S   : 接收参数，调用 __scm_setup_*，例如 -S git,会在解压源码后调用 %{__scm_setup_git}
%autosetup

# 示例：不自动解压 Source0， 使用 -b 指定解压 Source0，目录名指定为 %{name}，切换目录后解压 Source1，然后执行 git 仓库初始化并跳过一个路径前缀应用补丁
%autosetup -v -T -b 0 -n %{name} -S git -a 1 -p1
# 示例： 不自动解压 Source0，指定解压文件到 %{name}-1 文件夹中，指定 rpmbuild 执行目录为 %{name}-1，解压 Source1 到 %{name}-1
%autosetup -v -T -c %{name}-1 -S git -a 1

# ========== setup ==========
# setup解压源码，不自动应用补丁
# -q : 不打印解压源码过程中的 tar 输出文本
# -n : 源码包解压后目录不是 %{name}-%{version} 的，需要重新指定
# -T : 不要执行解压默认源码操作
# -D : 解压源码前不要删除目录
# -c : 解压源码前创建目录，并切换到该目录
%setup -q -T -D -a 1
# 常用的 "-pNUM" 选项，向 patch 程序传递参数，表示跳过 NUM 个路径前缀。
%patch0 -p1
# 接受切换路径后应用补丁文件
pushd contrib >/dev/null || exit 1
%patch1 -p2
popd >/dev/null || :

# 附加文件处理
# 复制附加文件到源码目录，参与软件构建流程；contrib 是示例目录，请参照实际情况处理
%{__cp} %{SOURCE2} ./contrib/
# 解压附加文件到源码目录，参与软件构建流程；contrib 是示例目录，请参照实际情况处理
%{__tar} xf %{SOURCE3} -C ./contrib/

# 如果编译编译要求是在 git 仓中进行，请使用如下指令初始化本地 git 仓库，此时需要在编译依赖中附加 git 软件包
# 也可以通过 %autosetup -S git 的方式自动完成 git 本地仓创建
# 参数说明： -q 抑制不必要输出内容
%{__scm_setup_git} -q
# 某些软件可能还会检查 TAG，使用如下指令添加一个虚假的 TAG, 示例 TAG 是使用当前软件版本号
%{__git} tag -a %{version} -m "%{_vendor} build"

# 设置 github 代理
# 如果软件构建过程需要从 github 下载其他依赖组件，使用如下命令配置 github 代理，使用国内镜像站，加速构建
%{__git} config --global url."https://hub.fastgit.org/".insteadOf "https://github.com/"

# 设置 go 代理
# 如果是 go 语言编译的软件，编译需要在线下载依赖组件，使用如下命令配置 go 代理，加速构建
go env -w GO111MODULE=on
go env -w GOPROXY="https://goproxy.cn,https://goproxy.io,direct"
go env -w GOSUMDB="gosum.io+ce6e7565+AY5qEHUk/qmHc5btzW45JVoENfazw8LielDsaI+lEbq6"

# 设置 npm 代理
npm config set registry https://repo.huaweicloud.com/repository/npm/

# 设置 pip3 代理
pip3 config set global.index-url https://mirrors.huaweicloud.com/repository/pypi/simple
pip3 config set global.trusted-host https://mirrors.huaweicloud.com

# 修改 pom 文件中的 apache 存档地址为 huaweicloud
grep -r "https://archive.apache.org/dist" -l | grep -E "[\/]?pom.xml$" |
    xargs -I'{pomfile}' sed -i 's|https://archive.apache.org/dist/|https://repo.huaweicloud.com/apache/|g' '{pomfile}'


# ========== 编译阶段 ==========
# 软件编译构建阶段
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
%build
# 编译阶段如果需要借助操作用户的家目录暂存文件，请不要使用硬编码的方式指定用户家目录，而是使用 shell 变量 HOME
%{__mkdir_p} ${HOME}/lang
# ========== C/C++ ==========
# ---------------------------- 安全编译宏 ---------------------------- #
# 部分编译宏已经默认附带如下描述安全编译宏，请根据实际情况设置，避免重复设置
# C/C++ 软件务必应用安全编译选项，请根据软件 Makefile 配置，确认使用下列哪些选项。
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export FFLAGS="%{build_fflags}"
export LDFLAGS="%{build_ldflags}"
export FCFLAGS="%{optflags}"
# 如果需要导出上述 5 个选项中的大多数，可以直接使用如下宏，直接导出所有编译选项配置：
%set_build_flags
# 上述设置安全编译选项等的配置，不一定对当前正在编译的包生效。你需要对 Makefile 做进一步确认，
# 是否接受外部参数，或者预留了其他接收外部参数的 Makefile 变量，你需要根据实际情况调整，
# 可以选用如下指令代替上述导出编译参数的指令，具体使用的宏需要灵活调整：
export REAL_OPT="%{optflags}"
# C/C++编译优化级别默认是O2，在debug调试过程中经常会遇到变量已被优化的问题，
# 可以通过如下方法修改优化级别为O0，使局部变量不被优化。
export CFLAGS="$(echo "%{build_cflags}" | sed 's|\-O2|\-O0|g')"
export CXXFLAGS="$(echo "%{build_cxxflags}" | sed 's|\-O2|\-O0|g')"
export FFLAGS="$(echo "%{build_fflags}" | sed 's|\-O2|\-O0|g')"
export FCFLAGS="$(echo "%{build_fflags}" | sed 's|\-O2|\-O0|g')"
LDFLAGS="${LDFLAGS:-%{build_ldflags}}" ; export LDFLAGS
# ---------------------------- 安全编译宏 ---------------------------- #

# 使用 configure 文件配置软件编译设置，请务必使用宏，除非宏无法用于该软件。注意该宏已经附带上述安全编译宏！
%configure
# 使用 make 命令构建，务必使用宏，除非宏无法用于该软件
%make_build
# 使用 cmake 命令构建，务必使用宏，除非宏无法用于该软件。注意该宏已经附带上述安全编译宏！
# 一般的，cmake 构建是在一个隔离目录中进行，请使用如下指令，创建 build 目录，在 build 目录中执行构建
%{__mkdir_p} build && pushd build &>/dev/null || exit 1
%cmake ..
popd &>/dev/null || :


# ========== Java ==========
# 添加父 pom 引用到 pom 文件中
# %pom_add_parent groupId*:*artifactId[*:*version] [POM-location]
%pom_add_parent

# --------------------------
# 从 pom 文件中删除父 pom 引用
# %pom_remove_parent [POM-location]...
%pom_remove_parent

# --------------------------
# 设置 pom 文件中的父 pom 引用
# %pom_set_parent groupId:artifactId[:version] [POM-location]...
%pom_set_parent

# --------------------------
# 添加依赖到 pom 文件
# %pom_add_dep groupId*:*artifactId[:*version[:*scope]] [POM-location] [extra-XML]
%pom_add_dep

# --------------------------
# %pom_add_dep_mgmt groupId:articId[:*version[:*scope]] [POM-location] [extra-XML]
%pom_add_dep_mgmt

# --------------------------
# 修改 pom 文件或者 ivy 模块中的依赖
# %pom_change_dep [OPTIONS] SOURCE_ARTIFACT CHANGED_ARTIFACT [POM-location]... [extra-XML]
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
%pom_change_dep

# --------------------------
# 删除 pom 文件中的依赖项
# %pom_remove_dep [OPTIONS] [groupId]:[artifactId][:version[:scope]] [POM-location]...
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
# 示例：
%pom_remove_dep \
    io.netty:netty-tcnative:2.0.1.Final:test:osx-x86_64 \
    distribution/pom.xml

# --------------------------
# 添加插件引用到 pom 文件中
# %pom_add_plugin groupId:artifactId[:version] [POM-location]... [extra-XML]
%pom_add_plugin

# --------------------------
# 从 pom 文件中删除 manve 插件引用
# %pom_remove_plugin [OPTIONS] [groupId]:[artifactId][:version[:scope]] [POM-location]...
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
%pom_remove_plugin

# --------------------------
# 禁用 pom 文件中指定的项目模块
# %pom_disable_module module-name [POM-location]...
# 示例： 禁用 modules 中的 storage-elasticsearch
%pom_disable_module storage-elasticsearch contrib/pom.xml

# --------------------------
# 禁用完全符合 XPath 条件的 pom 文件中的模块
# %pom_xpath_disable XPath-expression [POM-location]...
%pom_xpath_disable

# --------------------------
# 添加代码到 xml 文件中
# %pom_xpath_inject XPath XML-code [XML-file-location]...
# 示例： 在 id 是 jconsole 的 profile 的 activation 属性块中添加 activeByDefault 属性和值
%pom_xpath_inject \
    'pom:project/pom:profiles/pom:profile[pom:id="jconsole"]/pom:activation' \
    '<activeByDefault>false</activeByDefault>' \
    pom.xml

# --------------------------
# 从 xml 文件中删除一个节点
# %pom_xpath_remove [OPTIONS] XPath [XML-file-location]...
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
%pom_xpath_remove

# --------------------------
# 使用给定的代码替换 xml 文件中的代码
# %pom_xpath_replace XPath XML-code [XML-file-location]...
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
%pom_xpath_replace

# --------------------------
# 使用给定内容修改 xml 文件中节点内容
# %pom_xpath_set XPath new-contents [XML-file-location]
# -r : 递归操作，只影响 pom.xml
# -f : 修改过程出错不抛出异常
# 示例：
%pom_xpath_set \
   'pom:project/pom:dependencies/pom:dependency[pom:artifactId="netty-transport-native-epoll"]/pom:classifier' \
   "linux-aarch_64" \
   exec/rpc/pom.xml
# 对比 xmlstarlet 命令：
xmlstarlet ed -L \
   -N N="http://maven.apache.org/POM/4.0.0" \
   -u '//N:dependencies/N:dependency[N:artifactId="netty-transport-native-epoll"]/N:classifier' \
   -v "linux-aarch_64" \
   exec/rpc/pom.xml


# --------------------------
# 指定自定义 xmvn 配置选项，mvn_config 宏将自定义配置选项添加到 xmvn 反应器配置中。
%mvn_config resolverSettings/metadataRepositories/repository target-metadata.xml


# 使用 maven 构建的项目可能需要设置代理仓库，为了避免修改 pom.xml 文件，建议使用本仓库提供的 build_maven_settings.xml 文件作为 source 文件
# 然后针对不同架构启用不同的配置文件，aarch64 必须使用 aarch64_profile, 其他架构默认走 common_profile。
# 在 mvn 命令行使用 -P 指定 profile 的生效顺序是逆序的。例如 -Pa,b,c 生效顺序是 c,b,a，文件内部则是同一 profile 中的定义顺序。
%define mvn_postfix %{expand:-s %{_sourcedir}/build_maven_settings.xml \\
%ifarch aarch64
    -P aarch64_profile
%endif
}

mvn clean install \
%if %{?with_skiptests} # 跳过执行测试用例
    -DskipTests \
%endif
%if %{?with_skipbuildtests} # 跳过编译和执行测试用例
    -Dmaven.test.skip=true \
%endif
    %{mvn_postfix}

# 某些软件的编译依赖可能无法从 maven 仓库获取。此时，可以添加你的目标文件为一个 SOURCE，然后使用 mvn 命令安装到编译环境的本地仓库路径
# 参照如下示例，提供你的目标文件对应的必要信息，选取你的本地文件，mvn命令会将你的文件正确的安装到本地仓库路径。
mvn install:install-file \
    -DgroupId=io.grpc \
    -DartifactId=protoc-gen-grpc-java \
    -Dversion=1.14.0 \
    -Dclassifier=linux-aarch_64 \
    -Dpackaging=exe \
    -Dfile=%{SOURCE1} \
    %{mvn_postfix}

# 要生成 mvn(name) 这样的符号，并且编译的 jar 包具有 maven metadata, 使用如下命令编译：
%mvn_build -b -f -- %{mvn_postfix}


# ========== go ==========


# ========== rust ==========
# cargo 编译时需要从 crates-io 下载一些依赖包。因为 github 访问不稳定，所以在编译用户的家目录设置 registry 代理，来加速下载：
%{__mkdir_p} "$HOME/.cargo"
%{__cat} << EOF > "$HOME/.cargo/config"
[source.crates-io]
replace-with = 'ustc'
[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"
EOF
export CARGO_HOME="$HOME/.cargo"
# 使用 ustc 代理可能报告“无法解析主机: crates”，此时使用如下指令导出环境变量，禁止 http 并发下载即可：
export CARGO_HTTP_MULTIPLEXING=false
# 调用 cargo 的宏开始编译。注意： cargo_build 宏上自带 CARGO_HOME 是 ./cargo 目录
# 要使用刚创建的 cargo 配置影响 cargo_build 宏，请将 config 文件创建到 ./cargo 目录中
%cargo_build


# ========== nodejs ==========



# ========== python ==========
%py3_build


# ========== bazel ==========
bazel build \
    --local_ram_resources=8192 \        # 指定编译使用的内存资源，单位 MB
    --local_cpu_resources=1 \           # 指定编译使用的 CPU 资源，单位 thread
    --repository_cache=../BAZEL_CACHE \ # 指定下载的资源存储路径
    standard-opts...                    # 编译该软件需要提供的标准参数


# ========== 测试阶段 ==========
# 执行软件包内建测试用例
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
%check
# Nothing .......


# ========== 安装阶段 ==========
# 安装目标文件到 buildroot 目录
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
# 注意： 禁止复制文件到 %{buildroot}/opt/%{name} 或者 %{buildroot}%{_prefix}/local/%{name} 目录，这违反了 FHS 定义
%install
# 创建目录
# 强烈建议使用 install -d 指令创建目录，而不是 mkdir，install 指令可以显示的控制目录文件夹的权限配置，而 mkdir 被动地受 umask 影响
install -d -p -m 0755 %{buildroot}%{_bindir}
# 示例： 创建一个 /usr/share/SuperSample/example 文件夹，uid 是 1000， gid 是1000 的用户和组可以访问该文件夹，并具有完全操作权限
install -d -m 0770 -o 1000 -g 1000 %{buildroot}%{_datadir}/%{name}/example

# 安装文件
# 强烈建议使用 install -D，例如 install -D file1 folder1/folder2/target, 会自动创建 folder1/folder2 目录，然后复制 file1 文件为 target
# 参数说明：
# -D : 创建目标前导路径
# -p : 复制源文件的时间戳到目标文件
# -m : 精确的权限控制，可执行文件为 0755，配置文件为 0644，或者更小权限 0600 等
# 额外说明：示例中 %{_libexecdir} 目录用于安装非用户直接执行二进制文件，具体请参阅 FHS 说明
install -D -p -m 0750 ./release/sample_tool %{buildroot}%{_libexecdir}/%{name}/bin

# 创建符号链接
# 如下示例，假设 jar 项目的配置文件移动到 /etc 目录，需要在项目家目录创建一个 conf 目录保证功能正常，此时创建符号链接，使 conf 指向
# /etc/sw_name，请使用如下指令创建符号链接， -T 参数可以保证创建的符号链接名为 conf，如果此处已经存在一个 conf 文件夹，则会创建失败
%{__ln_s} -f -T %{_sysconfdir}/%{name} conf

# ========== nodejs ==========
# 需要先创建软件包安装目录
install -d -p -m 0755 %{buildroot}%{nodejs_sitelib}/%{packagename}
# 使用 npm_config_prefix 指定安装目录，将 SOURCE0 作为安装输入
npm_config_prefix=%{buildroot}%{_prefix} npm install -g %{SOURCE0}


# ========== python ==========
%py3_install


# ========== java ==========
# 编译生成 jar 包的，一般使用如下命令安装
%mvn_install

# 其他 maven 构建的软件包，解压 target 中生成的 tar.gz 或 zip 包之后，复制结果文件到目标目录
# 此类软件大多属于架构无关的，如果是功能软件，请使用如下示例指令，cp 命令需要根据实际情况做调整
install -d -p -m 0755 %{buildroot}%{_datadir}/%{name}
%{__cp} -a target/%{name}/* %{buildroot}%{_datadir}/%{name}/
# 需要调整的项目：
# conf 文件应该安装到 /etc 目录
install -d -p -m 0755 %{buildroot}%{_sysconfdir}/%{name}
%{__cp} -a target/%{name}/conf/* %{buildroot}%{_sysconfdir}/%{name}/
# 从编译结果中删除 conf 目录后
%{__rm} -rf target/%{name}/conf
# 复制剩余文件到 %{_datadir}/%{name}/ 目录中
%{__cp} -a target/%{name}/* %{buildroot}%{_datadir}/%{name}/
# 此时需要链接 conf 文件到 %{_datadir}/%{name}/ 目录中，保证功能完整性。
pushd %{buildroot}%{_datadir}/%{name} >/dev/null || :
%{__ln_s} -f -T %{_sysconfdir}/%{name} conf
popd >/dev/null || :

# arm 适配中，某些编译完成的 jar 包可能缺少 aarch64 架构的动态库，可以使用 jar 命令来更新这类 jar 包完成适配
# 用法 jar uf target.jar newfile(s)
# 示例1：给目标 jar 包插入一个文件，结果：jar 包中多出一个文件 librocksdbjni-linux64.so
# jar uf heron-apiserver.jar librocksdbjni-linux64.so
# 示例2：给目标 jar 包插入一个文件，包含路径，结果：jar 包中多出一个文件 root/.jar/librocksdbjni-linux64.so
# jar uf heron-apiserver.jar /root/.jar/librocksdbjni-linux64.so
# 示例3：给目标 jar 包插入一个文件，包含路径，结果：jar 包中多出一个文件 .jar/librocksdbjni-linux64.so
# jar uf heron-apiserver.jar -C /root/ .jar/librocksdbjni-linux64.so

# 使用 mvn_install 安装的包，会生成 maven-metadata, 此时可能解析出大量的依赖。如果 maven 无法找到合适的依赖，会在元数据文件中标记为 UNKNOWN
%{__sed} -i '/UNKNOWN/d' %{buildroot}%{_datadir}/maven-metadata/%{name}.xml

# ========== go ==========
# go 语言编译结果可能不在源码目录，而是位于 ${HOME}/go/bin 目录中
# go 编译出来的二进制可能含有 debugging symbols and sections，这会导致文件很大，但是又无法提供 debugsource 和 debuginfo，
# 可以在安装文件的时候直接压缩二进制，建议使用如下指令安装目标文件：
install -D -p -m 0755 --strip ./release/go_bin %{buildroot}%{_bindir}/go_bin

# ========== shebang lines ==========
# 即脚本文件开始的执行环境声明，如 #!/bin/env bash 或者 #!/usr/bin/env bash，需要更改为 #!/usr/bin/bash
# 如下指令可以更改 bash 环境声明的此类文件首行声明，但可能有某些文件不规范，无法使用该指令修改，强烈建议使用 patch 文件完成该修改
pushd %{buildroot} >/dev/null || :
%{__grep} -rE "^#\![/usr ]{0,4}/bin/env bash" -l | xargs sed -i '1s@^.*env bash.*$@#\!/usr/bin/bash@'
# python
%{__grep} -rE "^#\![/usr ]{0,4}/bin/env python[23]?$" -l | xargs sed -i '1s@^.*env python.*$@#\!/usr/bin/python3@'
# perl
%{__grep} -rE "^#\![/usr ]{0,4}/bin/env perl" -l | xargs sed -i '1s@^.*env perl.*$@#\!/usr/bin/perl@'
popd >/dev/null || :

# ========== rpath ==========
# rpath 是 二进制文件运行首先查找动态链接的说明，rpmbuild 编译生成的包常见该问题，可以从二进制文件中删除 rpath
# 打包合理的情况下，二进制运行所需的动态库会安装到 runpath 中，删除 rpath 不会影响正常功能。
find %{buildroot} -type f -exec file {} \; | %{__grep} "\<ELF\>" | awk -F ':' '{print $1}' | xargs -i chrpath --delete {}

# 静态库和库信息记录文件
# 主要涉及如下两种文件：
# .la: 使用libtool编译出的库文件，其实是个文本文件，记录同名动态库和静态库的相关信息
# .a : 静态库，其实就是把若干o文件打了个包
# 如果不需要打包静态库和 la 文件，使用如下宏：
%delete_la_and_a
# 宏展开：find %{buildroot} -type f -name "*.la" -delete ; find %{buildroot} -type f -name "*.a" -delete

# 如果需要打包静态库，删除 la 文件，使用如下宏：
%delete_la
# 宏展开：find %{buildroot} -type f -name "*.la" -delete


# ========== 安装事务 ==========
# 一般包括 pre、preun、post、postun、pretrans、posttrans
# 强烈建议避免使用 pretrans、posttrans 事务
# 常用四种事务可以通过参数控制是何种操作，参数值解释如下：
# |---------------------|----------------|-----------------|-----------------|-----------------|----------------|----------------|
# |                     | %pretrans      | %pre            | %preun          | %post           | %postun        | %posttrans     |
# |---------------------|----------------|-----------------|-----------------|-----------------|----------------|----------------|
# |Initial installation | 0              | 1               | not applicable  | 1               | not applicable | 0              |
# |Upgrade              | 0              | 2               | 1               | 2               | 1              | 0              |
# |Un-installation      | not applicable | not applicable  | 0               | not applicable  | 0              | not applicable |
# |---------------------|----------------|-----------------|-----------------|-----------------|----------------|----------------|

# ========== 安装前 ==========
%pre
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
# 如果软件安装后，需要使用某一指定用户，可以在该阶段完成用户创建，创建用户不考虑是 init 还是 upgrade
# 方式1：使用 useradd 命令直接添加
if ! getent group "%{group_name}" >/dev/null; then
    groupadd -r "%{group_name}"
fi

if ! getent passwd "%{user_name}" >/dev/null; then
    # 需要指定用户运行家目录，使用 -d 参数指定，一般使用 %{_datadir}/%{name} 或者 %{_sharedstatedir}/%{name}
    useradd -r -g "%{group_name}" -d "%{_datadir}/%{name}" -s \
        "%{_sbindir}/nologin" -c "%{name}" "%{user_name}"
    # 用户仅用作 systemd 进程拥有者，可以不指定家目录，使用 -M 参数
    useradd -r -g "%{group_name}" -M -s "%{_sbindir}/nologin" -c "%{name}" "%{user_name}"
fi
# 方式2： 借助如下宏直接创建一个用户名与组名同名的用户，效果等同 useradd -r -M -s /sbin/nologin -c "%{name}" %{name}
%sysusers_create_inline u %{user_name} - -
# 该事务逻辑适用类型使用参数判断
if test "$1" = "1"; then
    echo "Init"
elif test "$1" = "2"; then
    echo "Upgrade"
fi


# ========== 卸载前 ==========
%preun
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
# 支持 systemd 管理服务的软件，务必调用如下宏：
%systemd_preun %{name}.service
# 该事务逻辑适用类型使用参数判断
if test "$1" = "0"; then
    echo "Uninstall"
elif test "$1" = "1"; then
    echo "Upgrade"
fi



# ========== 安装后 ==========
%post
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
# 支持 systemd 管理服务的软件，务必调用如下宏：
%systemd_post %{name}.service
# 如果软件包安装完成后，在用户使用软件前需要做一些处理，比如重新生成一个 checksum 值，可以在此处处理
# 也可以在此处来刷新安装目录中某些文件的权限，创建一些必要的符号链接等
# 另有一些软件可能经过版本更新之后，发生了功能接口变更，需要在此处调用新集成的软件升级脚本，来更新用户的配置文件和数据文件等

# 该事务逻辑适用类型使用参数判断
if test "$1" = "1"; then
    echo "Init"
elif test "$1" = "2"; then
    echo "Upgrade"
fi


# ========== 卸载后 ==========
%postun
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
# 支持 systemd 管理服务的软件，务必调用如下宏：
%systemd_postun_with_restart %{name}.service
# 如果软件包在安装后，使用事务创建了符号链接，可以在此处来删除
# 删除软件使用过程中生成的某些文件，需要确认这些文件删除后不会造成客户损失

# 该事务逻辑适用类型使用参数判断
if test "$1" = "0"; then
    echo "Uninstall"
elif test "$1" = "1"; then
    echo "Upgrade"
fi


# ========== 子包事务 ==========
# 为指定包创建安装、卸载事务，可以指定包名，示例为 python3-%{pypi_name} 包创建安装后事务
%post -n python3-%{pypi_name}
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
echo "Do nothing..."


# 示例为 %{name}-devel 包创建卸载后事务
%postun devel
# 注意： 该阶段支持使用 shell 代码进行流程控制，但请注意编码规范问题，避免重复、冗余代码，保证逻辑清晰、安全。
echo "Do nothing..."


%files
%license LICENSE licenses/Apache-License licenses/GPL-License
# 注意：如下使用 %doc doc/ 包含的文件，无法使用 %exclude 排除，如果要包含一个目录中的文件，又要排除部分内容，方法有二：
# 1. 从目录中删除不想要的文件
# 2. 将目标文件安装到 %{_pkgdocdir} 目录中
%doc README.md doc/ example
# 声明目录是当前包所有，该声明仅添加目录到打包文件列表，不包含目录中文件
%dir %{_sysconfdir}/%{name}
# 包含目录中文件，可以使用通配符。etc 目录中的配置文件一般需要配置为 noreplace。标记为 config 的文件不安装到 etc 目录，rpmlint 会报告警。
%config(noreplace) %{_sysconfdir}/%{name}/*
# 对文件进行精确权限控制，示例中设置 /etc/rc.d/init.d/SuperSample 文件权限为 -rw-r----- user group
%attr(0640, %{user_name}, %{group_name}) %{_initrddir}/%{name}
# node.js 语言软件包，打包文件一般使用如下指令：
%dir %{nodejs_sitelib}/%{packagename}
%{nodejs_sitelib}/%{packagename}/*
# 软件编译安装结果，在某个系统目录中仅有有数的几个文件，尽量直接列出所有文件，而不是使用通配符
%{_bindir}/sample_parser
%{_libdir}/libsample.so.%{sover}
# 确认某文件不会打包到任何一个包中，在此处使用 exclude 排除。文件已安装但未打包针对所有 %files 而言，而不是某一个。
%exclude %{_sbindir}/srv_sample
# 某些软件包可能在编译安装阶段会自动安装 doc 文件，此时如果需要指定 doc 文件安装目录，请使用 _pkgdocdir 宏，并在打包时列出所有文件：
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/README.txt


%files devel
%dir %{_includedir}/sample
%{_includedir}/sample/*.h
%{_libdir}/libsample.so


%files -n python3-%{pypi_name}
# 当前包全局权限控制，使用如下指令设置:
# defattr(file_perm, user, group, folder_perm)
# 如下示例使用方法：
# 所有文件权限为 -rwxr-x--- root root
# 所有目录权限为 drwxr-xr-x root root
# 注意: 如果仅设置文件(夹)所有者是 root:root，请勿添加该声明，rpm 包由 root 用户安装，默认缺省用户是 root 用户。
%defattr(0750, root, root, 0755)
# python 语言软件包，打包文件一般使用如下指令：
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}*egg*
# 架构相关
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}*egg*


%changelog
* Tue Jul 06 2021 He Rengui <herengui@uniontech.com> - 1.0.0-1
- sample init
