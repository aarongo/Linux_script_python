# _*_coding:utf-8_*_
__author__ = 'lonnyliu'
import pexpect


class AutoPassword(object):
    def __init__(self, command, passd):
        self.command = command
        self.passd = passd

    def start(self):
        print "\033[32mRunning ....................\033[0m"
        # --------执行Linux 系统命令--------
        child = pexpect.spawn(self.command)
        # --------探测屏幕输出信息--------
        child.expect("password for yulong:")
        # "-------发送密码-------"
        child.sendline(self.passd)
        # "-------收集结果-------"
        child.expect(pexpect.EOF)
        print "-------------------------\033[32m结果为 \033[0m-------------------------",child.before


if __name__ == "__main__":
    while True:
        password = "aarongo"
        # 执行单个命令时可以写死
        # com = "sudo /home/yulong/.pyenv/versions/2.7.10/bin/python2.7 /home/yulong/.pyenv/versions/2.7.10/bin/sslocal -c /etc/shadowsocks.json -d start"

        # 执行多条命令 与while Ture 结合
        com = "sudo" + " " + str(raw_input("Please Input Commands:"))
        run = AutoPassword(com, password)
        run.start()
        if com.endswith("quit"):
            print "--------\033[31m退出该SHELL \033[0m--------"
            break
