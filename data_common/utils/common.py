# coding=utf-8
import hashlib
import subprocess
import re
from data_common.utils.log_util import Logger


class Common:

    suffix_list = ['com', 'cn', 'net']
    replace_list = ['\\w+', '.*', '.+', '[', ']',
                        '^', 'a-z', 'a-Z', 'A-Z']

    def __init__(self):
        pass

    @staticmethod
    def filter_host(host):
        for item in Common.replace_list:
            host = host.replace(item, '')
        return host

    @staticmethod
    def get_domain(url, _all=False):
        rest = url.split('//')[-1]
        host = rest.split('/')[0]
        host = Common.filter_host(host)
        for suffix in Common.suffix_list:
            pattern = f'(.*)\\.{suffix}'
            if re.search(pattern, host):
                res = re.findall(pattern, host)[0]
                return res.split('.')[-1]
        return host

    @staticmethod
    def get_md5(ss):
        if isinstance(ss, str):
            ss = ss.encode('utf-8')
        m2 = hashlib.md5()
        m2.update(ss)
        return m2.hexdigest()

    @staticmethod
    def get_filter_text(text):
        text = re.sub('[\\r|\\n\\t]', ' ', text)
        text = re.sub(' +', ' ', text)
        return text.strip()

    @staticmethod
    def execute(cmd):
        """
        @functions：execute
        @param cmd： 执行命令
        @return：执行成功返回True, 执行错误则返回False
        @summary：
        """
        Logger.info('Execute command:{cmd}'.format(cmd=cmd))
        subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        c, e = subp.communicate()
        for s in c.split('\n'):
            if subp.returncode != 0:
                Logger.error(s.strip())
            else:
                Logger.info(s.strip())
        for s in e.split('\n'):
            if subp.returncode != 0:
                Logger.error(s.strip())
            else:
                Logger.info(s.strip())
        if subp.stdin:
            subp.stdin.close()
        if subp.stdout:
            subp.stdout.close()
        if subp.stderr:
            subp.stderr.close()
        try:
            subp.kill()
        except:
            pass
        if subp.returncode != 0:
            Logger.error('Execute command:{cmd} failed'.format(cmd=cmd))
            return False
        return True

    @staticmethod
    def execute2(cmd):
        """
        @functions：execute
        @param cmd： 执行命令
        @return：执行成功返回True, 执行错误则返回False
        @summary：
        """
        Logger.getlogging().info('Execute command:{cmd}'.format(cmd=cmd))
        subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subp.wait()
        c = subp.stdout.readline()
        while c:
            if subp.returncode != 0:
                Logger.getlogging().info(c.strip())
            else:
                Logger.getlogging().info(c.strip())
            c = subp.stdout.readline()
        e = subp.stderr.readline()
        while e:
            if subp.returncode != 0:
                Logger.getlogging().error(e.strip())
            else:
                Logger.getlogging().error(e.strip())
            e = subp.stderr.readline()
        if subp.returncode != 0:
            Logger.error('Execute command:{cmd} failed'.format(cmd=cmd))
            return False
        return True

    @staticmethod
    def execute3(cmd):
        """使用file.cache缓存临时输出"""
        pass
if __name__ == '__main__':
    url = 'https://movie\\w+.douban.com'
    print(Common.get_domain(url))