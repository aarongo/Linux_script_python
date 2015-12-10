#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/5'
#   motto:  'Good memory as bad written'

import paramiko


def remote_scp(host_ip, remote_path, local_path, username, password):
    t = paramiko.Transport((host_ip, 22))

    t.connect(username=username, password=password)  # 登录远程服务器

    sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议

    src = remote_path

    des = local_path

    sftp.get(src, des)

    t.close()


remote_scp('10.90.10.100', '/software', '/software/packages', 'root', 'aarongo')
