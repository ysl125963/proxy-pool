# 待测试的网址
target_url = 'https://www.baidu.com/'
# 代理池中代理个数限定值，少于该值才执行爬取
proxy_enough_count = 1000
# 测试代理时每次请求最大数
test_request_count = 20
# 爬取代理及测试代理的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.157 Safari/537.36',
}

# 数据库设置
redis_host = 'localhost'
redis_port = 6379
redis_password = ''

# 测试开关
tester_enable = True
# 爬虫开关
crawler_enable = True
# API开关
api_enable = True
# 测试间隔时间
tester_interval = 60
# 爬虫间隔时间
crawler_interval = 20
