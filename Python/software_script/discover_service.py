#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'Edward.Liu'
# dateTime:  '15/12/16'
#   motto:  'Good memory as bad written'



# Linux Service discover~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# improt libary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import psutil


# cache service~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Discover(object):
    def cache(self, servername):
        pid = psutil.pids()
        for serverid in pid:
            process = psutil.Process(serverid)
            if process.name() == servername:
                print "\033[31m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m"
                print "\033[32mServer%sStatus:\033[0m" % servername + "\t" + "\033[31m%s\033[0m" % process.status()
                print "\033[32mServer%sStart Path:\033[0m" % servername + "\t" + "\033[31m%s\033[0m" % process.exe()
                print "\033[32mServer%sStart CmdLine:\033[0m" % servername + "\t" + "\033[31m%s\033[0m" % process.cmdline()
                print "\033[32mServer%sStart User:\033[0m" % servername + "\t" + "\033[31m%s\033[0m" % process.username()
                print "\033[31m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m"


if __name__ == "__main__":
    S = Discover()
    while True:
        servername = raw_input("Please Input Cache Servers:").strip()
        if servername.isdigit():
            print "\033[32mPleae Input Server Names!!!!\033[0m"
        elif len(servername) == 0:
            print "\033[32mPleae Input Server Names!!!!\033[0m"
        else:
            S.cache(servername=servername)
            break
