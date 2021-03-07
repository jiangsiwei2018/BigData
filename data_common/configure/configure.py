# -*- coding: utf-8 -*-

import time
import os
import socket
import configparser
from data_common.configure import constant
from data_common.designs.singleton import SingletonType


class Configure(metaclass=SingletonType):

    CONFIG_FILE_PATH = os.path.dirname(__file__) + '/setting.ini'

    def __init__(self):
        self.local_ip = None
        self.start_time = None
        self.config = configparser.ConfigParser()
        self.config.read(Configure.CONFIG_FILE_PATH)

    def get_config(self, domain, key):
        return self.config.get(domain, key)

    def get_start_time(self):
        if not self.start_time:
            self.start_time = int(time.time())
        return self.start_time

    def get_local_ip(self):
        if not self.local_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 0))
                IP = s.getsockname()[0]
            except:
                IP = '127.0.0.1'
            finally:
                s.close()
                print('Get Local IP: {ip}'.format(ip=IP))
                self.local_ip = IP
        return self.local_ip

    
if __name__ == '__main__':
    import os
    os.chdir('..')
    Configure().get_local_ip()
    print(Configure().get_config(constant.DATABASE_DOMAIN,
                                 constant.DATABASE_IP))
