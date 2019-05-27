"""测试代理是否对指定url可用"""
import aiohttp
import asyncio
import time
from db import RedisClient
from aiohttp.http_exceptions import HttpProcessingError
import settings


class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 单个代理
        :return: None
        """
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        real_proxy = 'http://' + proxy
        conn = aiohttp.TCPConnector(verify_ssl=False)
        try:
            async with aiohttp.ClientSession(headers=settings.headers, connector=conn) as session:
                print('正在测试', proxy)
                rsp = await session.get(settings.target_url, proxy=real_proxy, timeout=5)
                if rsp.status == 200:
                    self.redis.max(proxy)
                    print('代理可用', proxy)
                else:
                    self.redis.decrease(proxy)
                    print('代理请求失败', proxy)
                    raise HttpProcessingError(code=rsp.status, message=rsp.reason)
        except Exception as e:
            self.redis.decrease(proxy)
            print('代理请求失败', proxy)
            print(e.__cause__)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('开始测试...')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), settings.test_request_count):
                test_proxies = proxies[i:i + settings.test_request_count]
                task = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(task))
                time.sleep(5)
        except Exception as e:
            print('测试出现异常', e.args)


if __name__ == '__main__':
    test = Tester()
    test.run()
