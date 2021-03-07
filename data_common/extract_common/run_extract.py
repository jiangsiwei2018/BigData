# coding=utf-8
from data_common.extract_common.site_factory import SiteFactory

def run_extract(url, html):
    site = SiteFactory().get_site(url)
    return site.process(url, html)