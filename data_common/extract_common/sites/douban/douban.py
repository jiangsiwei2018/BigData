# coding=utf-8
from data_common.utils.file_util import FileUtil
from data_common.extract_common.template.template_analysis import TemplateAnalysis
from data_common.extract_common.sites.site_base import BaseSite


class Douban(BaseSite):

    url_patterns = ['https://movie.douban.com']

    def __init__(self):
        super(BaseSite, self).__init__()
        self.template_file = FileUtil.get_abs_path(__file__, 'patterns.json')
        self.methods_file = FileUtil.get_abs_path(__file__, 'methods.py')

    def process(self, url, html):
        params = TemplateAnalysis(self.template_file, self.methods_file).process(url, html)
        params = self.process_step(params)
        return params

    def process_step(self, params):
        return params

