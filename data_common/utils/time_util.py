# -*- coding: utf-8 -*-
import re
import copy

import time
from dateutil import parser
from datetime import datetime, timedelta


class TimeUtility:
    
    DEFAULT_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_FORMAT_DEFAULT = '%Y-%m-%d'
    TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'
    # 2016-11-20 16:20:00
    TIME_FORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S'
    # 2016-11-20T16:20:00+08：00
    UTC_FORMAT_DEFAULT = '%Y-%m-%dT%H:%M:%S+08:00'
    
    BEFORE_PATTERNS = [
        u'(\d+)\s*年\s*(\d+)\s*月\s*(\d*)\s*日',
        u'(\d+)\s*月\s*(\d+)\s*日\s*(\d+)\s*年',
        u'(\d+)月(\d+)日.(\d{4})',
        u'(\d+)\s*月\s*(\d*)\s*',
        u'(\d+)-(\d+)-?(\d*)',
        u'(\d+)/(\d+)/?(\d*)'
    ]
    SECOND_PATTERNS = [
        u'(\d+)\s*时\s*(\d+)\s*分\s*(\d*)\s*[秒]?',
        u'(\d+):(\d+):?(\d*)\s?(AM|PM)?']
    
    UN_NOMAL_FORMAT1 = {
        u'今天':{'days':0},
        u'昨天': {'days': -1},
        u'昨日': {'days': -1},
        u'前天': {'days': -2},
        u'一天前': {'days': -1},
        u'两天前': {'days': -2},
        u'三天前': {'days': -3},
        u'一年前': {'days': -1*365},
        u'两年前': {'days': -2*365},
        u'三年前': {'days': -3*365},
        u'刚刚': {'seconds': 0},
        u'半小时前': {'seconds': -30*60}
    }
    
    UN_NOMAL_FORMAT2 = {
        u'(\d+).*年前': {'days': -365},
        u'(\d+).*月前': {'days': -30},
        u'(\d+).*天前': {'days': -1},
        u'(\d+).*小时前': {'hours': -1},
        u'(\d+).*分钟前': {'seconds': -60},
        u'(\d+).*秒前': {'seconds': -1}
    }
    
    FLAG_PATTERNS = ['\n', '\t', '\r']

    @staticmethod
    def get_uniform_time(string, _format=DEFAULT_FORMAT): 

        if isinstance(string, str):
            string = TimeUtility.str_filter(string)
        if not str(string).strip():
            return None
        new_str = None
        try:
            if re.search('|'.join(TimeUtility.BEFORE_PATTERNS + TimeUtility.SECOND_PATTERNS), string):
                new_str = TimeUtility.get_format_time(string, _format)
            elif re.search('\d{8,}', string):
                # ***20160529212940***
                temp = re.findall('\d{8,}', str(string))[0]
                new_str = TimeUtility.get_format_time(temp, _format)
        except:
            new_str = None
        try:
            # 时间戳
            if not new_str and (int(string) or int(string) == 0):
                new_str = TimeUtility.get_int_format_time(string, _format)
        except:
            # traceback.print_exc()
            new_str = None
        if not new_str:
            new_str = TimeUtility.unnomal_format(string, _format)
        if not new_str:
            new_str = TimeUtility.get_format_time(string, _format)
        if not new_str:
            new_str = TimeUtility.nomal_format(string, _format)
        return new_str

    @staticmethod
    def get_format_time(string, _format=DEFAULT_FORMAT):
        try:
            return datetime.strftime(parser.parse(string), _format) 
        except:
            return None

    @staticmethod
    def nomal_format(string, _format=DEFAULT_FORMAT):
        before = ''
        second = ''
        for pattern in TimeUtility.BEFORE_PATTERNS:
            if re.search(pattern, string):
                num_str = re.findall(pattern, string)[0]
                num_str = [item for item in num_str if item]
                if len(num_str[-1]) > 4:
                    continue
                before = '-'.join(num_str)
                break
        for pattern in TimeUtility.SECOND_PATTERNS:
            if re.search(pattern, string):
                num_str = re.findall(pattern, string)[0]
                num_str = [item for item in num_str if item]
                second = ':'.join(num_str)
                if num_str[-1] == u'AM' or num_str[-1] == u'PM':
                    second = ':'.join(num_str[:-1])+' '+num_str[-1]
                break
        new_str = before + ' ' + second
        if not new_str.strip():
            return None
        return TimeUtility.get_format_time(new_str, _format)
    
    @staticmethod
    def unnomal_format(string, _format=DEFAULT_FORMAT):     
        for pattern in TimeUtility.UN_NOMAL_FORMAT1:
            if re.search(pattern, string):
                temp_dict = copy.deepcopy(TimeUtility.UN_NOMAL_FORMAT1[pattern])
                new_str = (datetime.now() + timedelta(**temp_dict)).strftime(_format)
                if re.search(u'天|日', string):
                    second = TimeUtility.nomal_format(string)
                    if second:
                        new_str = new_str[:10] + ' ' + second[-8:]
                return TimeUtility.get_format_time(new_str, _format)
        for pattern in TimeUtility.UN_NOMAL_FORMAT2:
            if re.search(pattern, string):
                temp_int = re.findall(pattern, string)[0]
                temp_dict = copy.deepcopy(TimeUtility.UN_NOMAL_FORMAT2[pattern])
                tempkey = temp_dict.keys()[0]
                temp_dict[tempkey] = temp_dict[tempkey] * int(temp_int)
                new_str = (datetime.now() + timedelta(**temp_dict)).strftime(_format)
                return TimeUtility.get_format_time(new_str, _format)

    @staticmethod
    def get_int_format_time(int_time, _format=DEFAULT_FORMAT):
        if int(int_time) > 10000000000:
            int_time = int(int_time) / 1000
        return time.strftime(_format, time.localtime(int(int_time)))
    
    @staticmethod
    def get_int_time(string, _format=DEFAULT_FORMAT):
        return int(time.mktime(time.strptime(string, _format)))
        
    @staticmethod
    def get_current_date(_format=DATE_FORMAT_DEFAULT):
        return time.strftime(_format)   

    @staticmethod
    def get_uniform_date_before(delta, _format=DEFAULT_FORMAT):
        return TimeUtility.get_uniform_time(str(datetime.now() - timedelta(days=int(delta))), format)
    
    @staticmethod
    def get_date_before(delta, _format=DEFAULT_FORMAT):
        return (datetime.now() - timedelta(days=int(delta))).strftime(format)
    
    @staticmethod
    def str_filter(string):
        for flag in TimeUtility.FLAG_PATTERNS:
            string = string.replace(flag, '').strip()
        return string
    
    @staticmethod
    def day_compare(t1, t2, days, _format=DEFAULT_FORMAT):
        if datetime.strptime(t1, _format) - datetime.strptime(t2, _format) <= timedelta(days):
            return True
        return False

    @staticmethod
    def compare_now(cur_time, days):
        """时间cur_time比现在小多少天,即cut_time是否是在当前时间的days之内"""
        now = TimeUtility.get_date_before(0)
        return TimeUtility.day_compare(now, cur_time, days)

    @staticmethod
    def isleap(year):
        is_leap = False
        if year % 100 == 0 and year % 400 == 0:
            is_leap = True
        elif year % 100 != 0 and year % 4 == 0:
            is_leap = True
        return is_leap



if __name__ == '__main__':
    t = '2017-12-23 17:21:01'
    print(TimeUtility.get_uniform_time(t, '%Y/%m/%d'))
