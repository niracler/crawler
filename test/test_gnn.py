import redis

client = redis.Redis(host='127.0.0.1', port='6379', password='123456')
base_url = 'https://gnn.gamer.com.tw/?yy={yy}&mm={mm}'

# for yy in range(2001, 2020):
#     for mm in range(1, 13):
#         url = base_url.format(yy=yy, mm=mm)
#         print(url)
#         client.lpush("gnn_redis:start_urls", url)


for yy in range(2020, 2021):
    for mm in range(1, 2):
        url = base_url.format(yy=yy, mm=mm)
        print(url)
        client.lpush("gnn_redis:start_urls", url)
