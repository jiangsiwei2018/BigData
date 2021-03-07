# coding=utf-8
import re


class RegexUtility:
    # 默认的ID正则表达式
    ID_REGEX = r'[^\w_\-][\'\"]{0,1}%s[\'\"]{0,1}\s*[%s]\s*[\'\"]{0,1}([\w_\-]+)[\'\"]{0,1}[^\w_\-]'

    @staticmethod
    def findall(reg, _str):
        rec = re.compile(reg)
        return re.findall(rec, _str)

    @staticmethod
    def get_id(name, content, split='=:'):
        reg = RegexUtility.ID_REGEX % (name, split)
        rec = re.compile(reg)
        try:
            values = re.findall(rec, content)
            if len(values) > 0:
                return values[0]
        except:
            pass
        return ''

    @staticmethod
    def match(reg, _str):
        return re.match(reg, str)

    @staticmethod
    def search(reg, _str):
        return re.search(reg, _str)


if __name__ == '__main__':
    import re
    print(re.findall('^f.*d$', 'food'))

    import traceback
    try:
        1/0
    except Exception as e:
        print(traceback.print_exc())