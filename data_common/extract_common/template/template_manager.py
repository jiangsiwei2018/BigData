# encoding=utf-8
import re
from data_common.designs.singleton import SingletonType
from data_common.utils.file_util import FileUtil


class TemplateManager(metaclass=SingletonType):

    def __init__(self, template_file):
        self.templates = FileUtil.read_json(template_file)

    def get_template(self, url):
        for template in self.templates:
            for pattern in template['patterns']:
                if re.search(pattern, url):
                    return template