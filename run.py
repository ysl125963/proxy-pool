"""控制是否抓取代理, 是否测试代理, 是否打开代理获取接口"""
from multiprocessing import Process
from api import app
from saver import Saver
from tester import Tester
import time
import settings


class Scheduler:
    def scheduler_tester(self):
        """
        定时测试代理
        :return: None
        """
        tester = Tester()
        while True:
            print('测试器开始运行...')
            tester.run()
            time.sleep(settings.tester_interval)

    def scheduler_crawler(self):
        """
        定时获取代理
        :return: None
        """
        saver = Saver()
        while True:
            print('开始抓取代理...')
            saver.run()
            time.sleep(settings.crawler_interval)

    def scheduler_api(self):
        """
        开启API
        :return: None
        """
        app.run()

    def run(self):
        print('代理池开始运行...')
        if settings.tester_enable:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        if settings.crawler_enable:
            getter_process = Process(target=self.scheduler_crawler)
            getter_process.start()
        if settings.api_enable:
            api_process = Process(target=self.scheduler_api)
            api_process.start()


if __name__ == '__main__':
    test = Scheduler()
    test.run()

