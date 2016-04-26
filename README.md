# TvCalendarShellNew
a new method to handle a TVCalendar datas

TVCalendar shell script 是一个用于从第三方获取美剧数据并存数数据库的脚本

##1.准备

###1.1环境

+ 支持python2.7的环境
+ 有一个MySQL/MariaDB数据库并有相应的账号密码
+ 在数据库中有一个如项目中.sql文件中要求的数据库结构
+ 安装python beautiful soup 4（针对最新版本可能会有警告，可以按照警告内容修改源代码）

###1.2 安装

脚本所在目录必须有写权限，复制整个脚本到一个目录下

##2.使用

建议使用后台运行

 `screen python start.py<True|False>`

其中如果是第一次执行脚本最后参数应当为True，之后每次运行使用False更有助于加速完成脚本

#####注：一般在网络畅通的情形下脚本运行时间在1-2个小时左右，可以使用计划任务使得程序自动运行

##3.维护
程序一般情况下不需维护，在程序所在目录下会有一个新的目录logs进入后可以看每天的错误日志（这些日志需要手动清理）

##4.引用
程序使用GPLv2.0协议发行，使用了Beautiful Soup模块。

##5.作者
[zhuyifan](https://github.com/zhuyf8899)
