# _*_coding:utf-8_*_
__author__ = 'yulong'

server_ip = {
    "carrefour_test": {
        "backen_ip": ['172.31.1.100', '172.31.1.200'],
        "Front_ip": ['172.31.1.101', '172.31.1.201'],
        "Release_ip": ['172.31.1.160'],
        "Solr_ip": ['172.31.1.155']
    },
    "B2B2C_Test": {
        "Backen_IP": ['10.90.6.27', '10.90.6.31'],
        "Front_IP": ['10.90.6.25', '10.90.6.26'],
        "Solr_IP": ['10.90.6.28', '10.90.6.29', '10.90.6.30']
    }
}


class Chose(object):
    def select(self):
        tmp_list = []
        server_list = []
        action_list = []
        for key in server_ip:
            tmp_list.append(key)
        for index, value in enumerate(tmp_list):
            print index, value
        environment = raw_input("Please chose environment:")
        if environment.isdigit():
            environment = int(environment)
            for key in server_ip[tmp_list[environment]]:
                server_list.append(key)
        for index, value in enumerate(server_list):
            print index, value
        chose_group = raw_input("Please chose server_Group:")
        if chose_group.isdigit():
            chose_group = int(chose_group)
            for key in server_ip[tmp_list[environment]].get(server_list[chose_group]):
                action_list.append(key)
        print action_list


run = Chose()
run.select()
