#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"

import httplib


def get_status_code(host, path="/"):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None


print get_status_code("10.151.255.10:8090", "/login")  # prints 404
