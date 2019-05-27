"""爬取代理，存入数据库"""
from db import RedisClient
from crawler import Crawler
import settings


class Saver:
    """
    爬取代理，并且存入redis数据库
    """
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断代理池中的代理数是否已经足够
        """
        if self.redis.count() >= settings.proxy_enough_count:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for crawl_func in self.crawler.crawl_funcs:
                proxies = self.crawler.get_proxies(crawl_func)
                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    test = Saver()
    test.run()
