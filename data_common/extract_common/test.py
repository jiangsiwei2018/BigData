# coding=utf-8
import re


class BaseSite:

    url_patterns = []

    def __init__(self):
        super(BaseSite, self).__init__()

    def process(self, url, html):
        params = {
            'url': url,
            'html': html,
            'params': ''
        }
        return params


class Douban(BaseSite):

    url_patterns = ['https://movie.douban.com']

    def __init__(self):
        super(BaseSite, self).__init__()

    def process(self, url, html):
        params = {
            'url': url,
            'html': html,
            'params': 'douban'
        }
        return params


class Tencent(BaseSite):

    url_patterns = ['https?://www.qq.com']

    def __init__(self):
        super(BaseSite, self).__init__()

    def process(self, url, html):
        params = {
            'url': url,
            'html': html,
            'params': 'qq'
        }
        return params


class Factory:

    def __init__(self):
        self.site_list = []

    def init_factory(self):
        self.site_list.append(Douban())
        self.site_list.append(Tencent())

    def get_site(self, url):
        for site in self.site_list:
            for pattern in site.url_patterns:
                if re.search(pattern, url):
                    return site
        return BaseSite()


if __name__ == '__main__':
    factory = Factory()
    factory.init_factory()
    url = 'https://www.qq.com'
    html = '<html></html>'
    site = factory.get_site(url)
    params = site.process(url, html)
    print(params)