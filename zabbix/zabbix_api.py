#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/29'
#   motto:  'Good memory as bad written'

import json
import urllib2
from urllib2 import URLError


class zabbix_api:
    def __init__(self):
        self.url = 'http://10.90.6.34:8080/api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "Admin",  # 修改用户名
                "password": "zabbix"  # 修改密码
            },
            "id": 0
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m 用户认证失败，请检查 !\033[0m", e.code
        else:
            response = json.loads(result.read())
            result.close()
            # print response['result']
            self.authID = response['result']
            return self.authID
zabbix = zabbix_api()
print zabbix.user_login()