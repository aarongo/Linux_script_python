# _*_coding:utf-8_*_
#######################Mysql###################
# 软件存放路径
software_dir = "/software/packages"
# mysql verson
version = ['mysql-5.1.73', 'mysql-5.5.45', 'mysql-5.6.26']
# mysql 现在 URL

mysql51_d_url = "http://124.200.96.150:8081/serverpackages/Mysql-5.5/mysql-5.1.73.tar.gz"
mysql55_d_url = "http://124.200.96.150:8081/serverpackages/Mysql-5.5/mysql-5.5.45.tar.gz"
mysql56_d_url = "http://124.200.96.150:8081/serverpackages/Mysql-5.5/mysql-5.6.26.tar.gz"
# 准备工作
cmake33_d_url = "http://124.200.96.150:8081/serverpackages/Mysql-5.5/cmake-3.3.2.tar.gz"
cmake_bin_path = "/usr/local/bin/cmake"
cmake_name = "cmake-3.3.2"
default_install_software = "wget tar ncurses  ncurses-devel  openssl openssl-devel zlib bison"
# 编译选项
install_directory = "-DCMAKE_INSTALL_PREFIX=/software/mysql"
data_directory = "-DMYSQL_DATADIR=/software/data/mysql"
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
#######################Msyql End########################################

###############################memcached################################
# memcached url
memcached_url = "http://172.31.1.160/serverpackages/Memcacehd/memcached-1.4.24.tar.gz"
# libevent zlib库 url
libevent_url = "http://172.31.1.160/serverpackages/Memcacehd/libevent-2.0.22-stable.tar.gz"
zlib_url = "http://172.31.1.160/serverpackages/Memcacehd/zlib-1.2.8.tar.gz"

# 获取软件包名
libevent_pack_name = libevent_url.split('//')[1].split('/')[3]
zlib_pack_name = zlib_url.split('//')[1].split('/')[3]
memcached_pack_name = memcached_url.split('//')[1].split('/')[3]
# 软件名称
libevent_name = libevent_url.split('//')[1].split('/')[3].split('.tar.gz')[0]
zlib_name = zlib_url.split('//')[1].split('/')[3].split('.tar.gz')[0]
memcached_name = memcached_url.split('//')[1].split('/')[3].split('.tar.gz')[0]
# 编译安装选项-- libevent
libevent_parameters = "--prefix=/usr/local/libevent"
libevent_dir = "/usr/local/libevent"
# 编译安装选项--zlib
zlib_paramenters = "--prefix=/usr/local/zlib"
zlib_dir = "/usr/local/zlib"
# 编译安装memcached 选项
memcached_install_dir = "/software/memcached"
memcached_parameters = "--prefix=%s --with-libevent=/usr/local/libevent" % memcached_install_dir
memcached_prot = [11211, 11212, 11213, 11214]
###################################Memcached End################################

###################################Mongodb######################################
# mongodb url
mongodb_url = "http://172.31.1.160/serverpackages/Mongodb/mongodb-linux-x86_64-rhel62-3.0.6.gz"
# 软件包名称
mongodb_pack_name = mongodb_url.split('//')[1].split('/')[3]
mongodb_name = mongodb_url.split('//')[1].split('/')[3].split('.gz')[0]
# 安装路径
mongodb_default_dir = "/software/mongodb3"
mongodb_bin_home = "%s/bin" % mongodb_default_dir
mongodb_data_dir = "/software/data/mongodb"
mongodb_config = """
systemLog:
 destination: file
###日志存储位置
 path: /software/data/mongod.log
 logAppend: true
storage:
##journal配置
 journal:
  enabled: true
##数据文件存储位置
 dbPath: /software/data/mongodb
##是否一个库一个文件夹
 directoryPerDB: true
##数据引擎
 engine: wiredTiger
##WT引擎配置
 wiredTiger:
  engineConfig:
##WT最大使用cache（根据服务器实际情况调节）
   cacheSizeGB: 10
##是否将索引也按数据库名单独存储
   directoryForIndexes: true
##表压缩配置
  collectionConfig:
   blockCompressor: zlib
##索引配置
  indexConfig:
   prefixCompression: true
#后台运行
processManagement:
 fork: true
##端口配置 默认监听所有
net:
 port: 27017
"""