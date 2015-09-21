#!/usr/bin/python
# _*_coding:utf-8_*_
"""           15-9-18
          author = 'yulong'
    Good memory than rotten written
"""
import datetime
import subprocess
import os
import pexpect


class Mysql_Backup(object):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H")
    delete_day_ago = 5
    db_host = "localhost"
    db_user = 'root'
    db_password = 'comall2014'
    db_name = "cybershop_test"
    mysqldump_bin_home = "/usr/bin/mysqldump"
    local_backup_dir = "/software/mysql_back"
    remote_user = 'root'
    remote_password = 'comall2014'
    remote_host = '172.31.1.160'
    remote_backup_dir = "/install/backup/mysql_backup"
    command = "%s -u%s -p%s --host=%s %s > %s/%s-%s.sql" % (
        mysqldump_bin_home, db_user, db_password, db_host, db_name, local_backup_dir, db_name, now)

    def backup(self):
        ret = -1
        print "\033[32m***********String Mysql Backing************"
        db_back = subprocess.Popen(self.command, shell=True)
        db_back.wait()
        path = self.local_backup_dir
        if len(os.listdir(path)) == 0:
            print "\033[31m ***************Mysql Backup Is Failed***************\033[0m"
        else:
            print "\033[32m ***************Mysql Backup Is Successful***************\033[0m"
            ret = 0
        return ret

    def send_sql_files(self):
        ###########remote###############
        path = self.local_backup_dir
        #############################
        # 传送文件到远程,遍历目录下的所有文件赋值给files 之后传送fiels
        for files in os.listdir(path):
            scp_command = "scp %s/%s %s@%s:%s" % (
                path, files, self.remote_user, self.remote_host, self.remote_backup_dir)
        print "\033[32m**********Running Scp To Remote Server....................\033[0m"
        child = pexpect.spawn(scp_command)
        child.expect("password:")
        child.sendline(self.remote_password)
        child.expect(pexpect.EOF)
        print "\033[32m***************Msyql BackUp Result***************\033[0m", child.before
        # 判断远程文件是否传送成功
        remote_command = """ssh %s@%s "ls %s/%s" """ % (
            self.remote_user, self.remote_host, self.remote_backup_dir, files)
        '''使用pexpect.run 发送密码的方式 执行远程命令进行判断备份文件是否存在 command_output(命令输出）exitstatus(命令执行状态）
            当命令成功时返回的状态码为0,当Linux exitcode 不是0的时候 exitstatus返回不等于0,即可判断远程文件是否传送成功
        '''
        command_output, exitstatus = pexpect.run(remote_command,
                                                 events={'(?i)password': 'comall2014\n'}, withexitstatus=1)
        if exitstatus == 0:
            command_rm = "rm -rf %s/*" % self.local_backup_dir
            print "\033[32m**********Delete LocalHost Files**********\033[0m"
            subprocess.call(command_rm, shell=True)
            print "\033[32m************************************************\033[0m"
        else:
            print "\033[31m******************Send Files Failed********************\033[0m"

    def days_delete_agos(self):
        # 执行远程命令删除备份机上的5天前的备份(保留5天的备份）此处comall2014需要更改
        command = """ssh %s@%s "find %s -mtime +%s -name '*.sql' -exec rm -rf {} \;" """ % (
            self.remote_user, self.remote_host,
            self.remote_backup_dir, self.delete_day_ago)
        command_output, exitstatus = pexpect.run(command,
                                                 events={'(?i)password': 'comall2014\n'}, withexitstatus=1)
        if exitstatus != 0:
            print "\033[32m***************Delete 5 days BackFiles Failed**************\033[0m"
        else:
            print "\033[31m**************Delete 5 Days BackFiles Sucessful OR Don't Exist 5 Days BackFiles*************\033[0m"


if __name__ == "__main__":
    run_start = Mysql_Backup()
    run_start.days_delete_agos()
    if run_start.backup() == 0:
        run_start.send_sql_files()
