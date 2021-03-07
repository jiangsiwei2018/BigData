# coding=utf-8
from data_common.utils.file_util import FileUtil
from data_common.extract_common.template.template_analysis import TemplateAnalysis


class BaseSite:

    url_patterns = []

    def __init__(self):
        super(BaseSite, self).__init__()
        self.template_file = FileUtil.get_abs_path(__file__, 'patterns.json')

    def process(self, url, html):
        params = TemplateAnalysis(self.template_file).process(url, html)
        params = self.process_step(params)
        return params

    def process_step(self, params):
        return params

