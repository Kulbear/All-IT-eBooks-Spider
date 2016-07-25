# -*- coding: utf-8 -*-
# 不用去看视频了，看我操作就行了
import random
import re
import time
import urllib.request

import conf as cf


class KanWoCaoZuo:
    BASE_URL = 'http://www.allitebooks.com'

    def __init__(self):
        self.start_page = 1
        self.headers = {
            'User-Agent': random.choice(cf.USER_AGENTS),
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.allitebooks.com/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

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
                    KanWoCaoZuo.BASE_URL + '/page/{}'.format(self.start_page), headers=self.headers)
                html = urllib.request.urlopen(req)
                doc = html.read().decode('utf8')
                alist = list(
                    set(re.findall(cf.BOOK_LINK_PATTERN, doc)))
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
    caozuo = KanWoCaoZuo()
    caozuo.build_proxy()
    caozuo.run()
