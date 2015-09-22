#!/usr/bin/python
# -*- coding: UTF-8 -*-
contact_dic = {}


with file('/software/upload/contact_list2.txt') as f:
    for i in f.readlines():
        # 遍历文件内容，去掉行首行尾空格（行中间的空格不会去掉），将字符串转换为列表以空格分割
        line = i.strip().split()

        # 给字典contact_dic赋值 { key=name,values=empinfo}
        contact_dic[line[0]] = line[1:]

# for key,value in contact_dic.items


flag = True
while flag:
    name = raw_input("input emp_name:")
    if name in contact_dic.iterkeys():
        list = contact_dic[name]
        flag = False
        print list
        for index,k in enumerate(list):
            print index,k
    else:
        print "Not exits--------"
