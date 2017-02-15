# -*- coding: utf-8 -*-
import re
import time
import urllib.request

import conf as cf

BASE_URL = 'http://www.allitebooks.com'

class MyCrawler:

    def __init__(self, base_url=cf.BASE_URL, header=cf.FAKE_HEADER, start_page=1):
        self.base_url = base_url
        self.start_page = start_page
        self.headers = header

    # 链接代理
    def build_proxy(self):
        proxy = cf.PROXY
        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    def fetch_book_name_list(self):
        while True:
            try:
                req = urllib.request.Request(
                    self.base_url + '/page/{}'.format(self.start_page), headers=self.headers)
                html = urllib.request.urlopen(req)
                doc = html.read().decode('utf8')
                alist = list(set(re.findall(cf.BOOK_LINK_PATTERN, doc)))
                print('Now working on page {}\n'.format(self.start_page))
                time.sleep(20)
                self.start_page += 1
                self.fetch_download_link(alist)
            except urllib.error.HTTPError as err:
                print(err.msg)
                break

    def fetch_download_link(self, alist):
        f = open('result.txt', 'a')
        for item in alist:
            req = urllib.request.Request(item)
            html = urllib.request.urlopen(req)
            doc = html.read().decode('utf8')
            url = re.findall(cf.DOWNLOAD_LINK_PATTERN, doc)[0]
            print('Storing {}'.format(url))
            f.write(url + '\n')
            time.sleep(7)
        f.close()

    def run(self):
        self.fetch_book_name_list()


if __name__ == '__main__':
    mc = MyCrawler()
    # mc.build_proxy()
    mc.run()
