#!/usr/bin/expect -f
########################## Linux 数组
environment=(172.31.1.100 172.31.1.101 172.31.1.200 172.31.2.230 172.31.1.160 192.168.1.200)
for index in ${!environment[*]}
do
	echo $index ${environment[$index]}
done
read -p "Enter your ip:" num
################################Linux 发送密码登陆服务器
set user root
set host ${environment[num]}
set password comall2014
set timeout -1

spawn ssh $user@$host
expect "*password:*"
send "$password\r"
interact
expect eof