# encoding=utf-8
from data_common.extract_common.template.template_methods import TemplateMethods

class Methods(TemplateMethods):

    @staticmethod
    def process_text(text, *args, **kwargs):
        print(text)