"""定义爬取代理的类"""
import requests
from bs4 import BeautifulSoup
from concurrent import futures
import time


class Crawler:
    """
    爬取代理的类
    """
    def __init__(self):
        # 爬取代理方法的列表
        self.crawl_funcs = []
        for k in Crawler.__dict__:
            if 'crawl_' in k:
                self.crawl_funcs.append(k)

    @staticmethod
    def get_page(url):
        """
        爬取页面，用bs格式化
        :param url: 爬取网页url
        :return: 格式化后的源码
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.157 Safari/537.36',
        }
        rsp = requests.get(url, headers=headers).text
        soup = BeautifulSoup(rsp, 'lxml')
        return soup

    def get_proxies(self, crawl_func):
        """
        收集爬取的代理，以列表形式返回
        :param crawl_func: 方法名
        :return: 代理列表
        """
        proxies = []
        for proxy in eval("self.{}()".format(crawl_func)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_xicidaili(self, page_count=5):
        """
        爬取西刺代理
        :param page_count: 爬取页面数
        :return:
        """
        url = 'https://www.xicidaili.com/nn/'
        urls = [url + str(i) for i in range(1, page_count+1)]
        with futures.ThreadPoolExecutor(5) as executor:
            soups = executor.map(self.get_page, urls)
        for soup in soups:
            trs = soup.select('tr')
            trs = trs[1:]
            for tr in trs:
                ip = tr.select('td')[1].get_text()
                port = tr.select('td')[2].get_text()
                yield ':'.join((ip, port))

    def crawl_kuaidaili(self, page_count=5, wait=3):
        """
        爬取快代理
        :param page_count: 爬取页面数
        :param wait: 快代理好像有一定的反爬措施，短时间内多次请求不给响应，所以设置一定的延迟
        :return: 代理
        """
        url = 'https://www.kuaidaili.com/free/inha/'
        urls = [url + str(i) for i in range(1, page_count+1)]
        for url in urls:
            soup = self.get_page(url)
            trs = soup.select('tbody tr')
            for tr in trs:
                ip = tr.select('td')[0].get_text()
                port = tr.select('td')[1].get_text()
                yield ':'.join((ip, port))
            time.sleep(wait)


if __name__ == '__main__':
    test = Crawler()
    xicidaili = test.get_proxies('crawl_xicidaili')