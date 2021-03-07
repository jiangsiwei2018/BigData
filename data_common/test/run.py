# encoding=utf-8
from data_common.extract_common.run_extract import run_extract
from data_common.utils.log_util import Logger


if __name__ == '__main__':
    import os
    import json
    url = 'https://movie.douban.com/subject/26348103/'
    path = os.path.dirname(__file__) + '/html.txt'
    with open(path, 'r', encoding='utf-8') as fp:
        html = fp.read()
    result = run_extract(url, html)
    print(result)
    json.dumps(Logger.info(result))