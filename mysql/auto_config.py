# _*_coding:utf-8_*_
# 软件存放路径
software_dir = "/software/packages"
# mysql verson
version = ['mysql-5.1.73', 'mysql-5.5.45', 'mysql-5.6.26']
# mysql 现在 URL

mysql51_d_url = "http://192.168.1.234/serverpackages/Mysql-5.5/mysql-5.1.73.tar.gz"
mysql55_d_url = "http://192.168.1.234/serverpackages/Mysql-5.5/mysql-5.5.45.tar.gz"
mysql56_d_url = "http://192.168.1.234/serverpackages/Mysql-5.5/mysql-5.6.26.tar.gz"
# 准备工作
cmake33_d_url = "http://192.168.1.234/serverpackages/Mysql-5.5/cmake-3.3.2.tar.gz"
cmake_bin_path = "/usr/local/bin/cmake"
cmake_name = "cmake-3.3.2"
default_install_software = "wget tar ncurses  ncurses-devel  openssl openssl-devel zlib bison"
# 编译选项
install_directory = "-DCMAKE_INSTALL_PREFIX=/software/mysql"
data_directory = "-DMYSQL_DATADIR=/software/data"
character_set = "-DDEFAULT_CHARSET=utf8"
# 默认字符校对
default_encoding = "-DDEFAULT_COLLATION=utf8_unicode_ci"
# readline库
use_readline = "-DWITH_READLINE=1"
# DWITH_SSL
ssl_Storehouse = "-DWITH_SSL=system"
# 嵌入式服务器
embedded_Server = "-DWITH_EMBEDDED_SERVER=1"
# 启用加载本地数据
local_file = "-DENABLED_LOCAL_INFILE=1"
# 开启下载
download = "-DENABLE_DOWNLOADS=1"
# 安装myisam存储引擎
myisam = "-DWITH_MYISAM_STORAGE_ENGINE=1"
# 启用InnoDB、ARCHIVE和BLACKHOLE引擎支持
InnoDB = "-DWITH_INNOBASE_STORAGE_ENGINE=1"
ARCHIVE = "-DWITH_ARCHIVE_STORAGE_ENGINE=1"
BLACKHOLE = "-DWITH_BLACKHOLE_STORAGE_ENGINE=1"
# 调试模式
debug = "-DWITH_DEBUG=0"

# 编译选项为
compile_command = "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s && make && make install" % (
    cmake_bin_path, install_directory, data_directory, character_set, default_encoding, use_readline, ssl_Storehouse,
    embedded_Server,
    local_file, download, myisam, InnoDB, ARCHIVE, BLACKHOLE, debug)
# 获取 URL中的 mysql 版本
mysql51 = mysql51_d_url.split("//")[1].split('/')[3].split('.tar.gz')[0]
mysql55 = mysql55_d_url.split("//")[1].split('/')[3].split('.tar.gz')[0]
mysql56 = mysql56_d_url.split("//")[1].split('/')[3].split('.tar.gz')[0]
mysql_bin = install_directory.split('=')[1]
mysql_data = data_directory.split('=')[1]
