# -*- coding: utf-8 -*-
# 不用去看视频了，看我操作就行了
import urllib.request
import re
import time
#from bs4 import BeautifulSoup


class KANWOCAOZUO:
    MIN_PAGENUM = 105
    MAX_PAGENUM = 620
    BASE_URL = 'http://www.allitebooks.com'
    BOOK_LINK_PATTERN = 'href="(.*)" rel="bookmark">'
    DOWNLOAD_LINK_PATTERN = '<a href="(.*)" target="_blank">Download PDF'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    HEADERS = {
        'User-Agent': USER_AGENT,
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.allitebooks.com/',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
    }

    def __init__(self):
        pass

    def build_proxy(self):
        proxy = {'http': "http://127.0.0.1:9743/"}
        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    def fetch_book_name_list(self):
        for i in range(KANWOCAOZUO.MIN_PAGENUM, KANWOCAOZUO.MAX_PAGENUM + 1):
            req = urllib.request.Request(
                KANWOCAOZUO.BASE_URL + '/page/{}'.format(i), headers=KANWOCAOZUO.HEADERS)
            html = urllib.request.urlopen(req)
            doc = html.read().decode('utf8')
            alist = list(
                set(re.findall(KANWOCAOZUO.BOOK_LINK_PATTERN, doc)))
            print('Now working on page {}\n'.format(i))
            self.fetch_download_link(alist)

    def fetch_download_link(self, alist):
        f = open('result.txt', 'a')
        for item in alist:
            req = urllib.request.Request(item)
            html = urllib.request.urlopen(req)
            doc = html.read().decode('utf8')
            url = re.findall(KANWOCAOZUO.DOWNLOAD_LINK_PATTERN, doc)[0]
            print('Storing {}'.format(url))
            f.write(url + '\n')
            time.sleep(5)
        f.close()

    def run(self):
        self.fetch_book_name_list()

a = KANWOCAOZUO()
a.build_proxy()
a.run()
