# _*_coding:utf-8_*_
__author__ = 'lonnyliu'
import pexpect, getpass


class AutoPassword(object):
    def __init__(self, sys_user, command, passd):
        self.sys_user = sys_user
        self.command = command
        self.passd = passd

    def start(self):
        print "\033[32mRunning ....................\033[0m"
        # --------执行Linux 系统命令--------
        child = pexpect.spawn(self.command)
        # --------探测屏幕输出信息--------
        child.expect(self.sys_user)
        # "-------发送密码-------"
        child.sendline(self.passd)
        # "-------收集结果-------"
        child.expect(pexpect.EOF)
        print "-------------------------\033[32m结果为 \033[0m-------------------------", child.before

if __name__ == "__main__":
    while True:
        sys_user_info = "password for" + " " + getpass.getuser()
        password = "aarongo"
        com = "sudo" + " " + str(raw_input("Please Input Commands:"))
        run = AutoPassword(sys_user_info, com, password)
        run.start()
        if com.endswith("quit"):
            print "--------\033[31m退出该SHELL \033[0m--------"
            break