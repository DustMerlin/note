# rpm

## 查询所有软件包，并导出 name 和 release-version 分离的内容，方便awk 处理或者其他文件获取数据

rpm -qa --qf '%{name} %{release}-%{version}\n'