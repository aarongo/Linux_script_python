# _*_coding:utf-8_*_
import socket
import sys
from paramiko.py3compat import u
import time

# windows does not have termios...
try:
    import termios
    import tty

    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, usr, ip):
    if has_termios:
        posix_shell(chan, usr, ip)
    else:
        windows_shell(chan)


def posix_shell(chan, user, ip):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd_list = []
        cmd = ''
        f = file("audit_%s.log" % time.strftime("%Y_%m_%d %H:%M"), 'wb')
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n***********\033[31m退出当前服务器 \033[0m***********\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                if not x == '\r':
                    cmd += x
                else:
                    cmd_format = "%s\t%s\t%s\t%s\n" % (user, ip, time.strftime("%Y-%m-%d %H:%M:%S"), cmd)
                    cmd_list.append(cmd)
                    cmd_format_tuple = (user, ip, cmd, time.strftime("%Y-%m-%d %H:%M:%S"))
                    f.write(cmd_format)
                    #cmd_list.append(cmd_format_tuple)
                    cmd = ''
                chan.send(x)
        f.close()
        print cmd_list

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        f.close()


# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF 退出当前服务器***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
