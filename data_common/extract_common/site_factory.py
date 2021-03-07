# encoding=utf-8
import re
from data_common.utils.common import Common
from data_common.designs.singleton import SingletonType
from data_common.designs.factory import FactoryClass
from data_common.extract_common.sites.site_base import BaseSite
from data_common.extract_common import sites


class SiteFactory(metaclass=SingletonType):

    def __init__(self):
        self.site_list = {}
        self.init_sites()


    def init_sites(self):
        site_list = FactoryClass.get_factory_class_list(BaseSite, sites, attrs=['url_patterns'])
        for site in site_list:
            for pattern in site.url_patterns:
                domain = Common.get_domain(pattern, False)
                if domain not in self.site_list:
                    self.site_list[domain] = {}
                self.site_list[domain][pattern] = site

    def get_site(self, url):
        domain = Common.get_domain(url)
        patterns = self.site_list.get(domain, {})
        for pattern, site in patterns.items():
            if re.search(pattern, url):
                return site()
