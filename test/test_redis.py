import time
import redis

client = redis.Redis(host='10.42.30.245', port='6379', password='123456')

# for i in range(1, 285):
#     url = 'https://www.liuli.in/wp/page/' + str(i)
#     print(url)
#     client.lpush("shenshe:start_urls", url)

# client.lpush("weibo:start_urls", "https://weibo.cn/u/5829543885")

# while True:
#     data = client.getrange('weibo_redis:start_urls')
#     if not data:
#         print("结束")
#         break
#     print(f'我现在获取的数据为：{data.decode()}')
#     time.sleep(1)

data = client.llen('weibo_redis:start_urls')
print(data)
