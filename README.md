# crawler
> 毕业设计的爬虫模块, 琉璃神社爬虫， 新浪微博爬虫

## 如何团队项目保持同步(重要)

- 第一次时需要,与团队仓库建立联系

```
git remote add upstream https://github.com/ghost-of-fantasy/crawler.git
```

- 工作前后要运行这几条命令,和团队项目保持同步

```
git fetch upstream
git merge upstream/master
```

## 安装并进行单机测试

### 安装依赖包

```sh
pip install --upgrade pip

pip install -r requirements.txt
```

### 尝试运行程序

```bash
scrapy crawl shenshe
```

## 爬虫设计

### 文章对象  

|Key|Value|  
|:---:|:---:|  
|website|网站的名称|
|url|文章链接|
|title|文章内容|
|content|文章内容|
|category|文章类型|
|publish_time|发布时间|

### 新浪微博爬虫设计

> 像是新浪微博这样的，是账号越多越好

1. 先爬取个人信息
2. 将这个人所关注的人也加到待爬序列中

微博用户(放在redis的List里面)

|Key|Value|
|:---:|:---:|
|user_id|用户ID|
|nickname|用户昵称；|
|weibo_num|微博数；|
|following|关注数；|
|followers|粉丝数；|

关系网络(放在redis的List里面)

|Key|Value|
|:---:|:---:|
|user_id|用户ID|
|follow_id|他关注的用户ID|

微博内容(放在redis的List里面)

|Key|Value|
|:---:|:---:|
|user_id|用户ID|
|weibo_content|存储用户的所有微博|
|weibo_place|存储微博的发布位置|
|publish_time| 存储微博的发布时间|
|up_num|存储微博获得的点赞数|
|retweet_num|存储微博获得的转发数|
|comment_num|存储微博获得的评论数|
|publish_tool|存储微博的发布工具|

## 待爬取网站

[新浪](https://www.sina.com.cn/)
[凤凰网](https://www.ifeng.com/)
[搜狐](http://news.sohu.com/)
[readhub](https://readhub.cn/topics)

## 使用swarm模式启动

### CentOS7 关闭防火墙

关闭
```bash
$systemctl stop firewalld.service
```

禁止开机启动
```bash
$systemctl disable firewalld.service
```

### 连接 redis

```bash
$redis-cli -h 172.28.7.40 -p 6379 -a 123456
```

## docker swarm 模式分布式部署

### 初始化 swarm 集群

```bash
$docker swarm init
```

然后将子节点连上

### 修改hostname

```bash
$sudo hostnamectl set-hostname <newhostname>
```

### 构建网络

```bash
$make network
```

### 构建 nginx 反向代理

```bash
$make spider-nginx
```

### 启动

```bash
$make spider
```

### 测试redis以及mongodb

redis

```bash
$sudo pacman -S redis # 安装redis
$redis-cli -h centos-l5-vm-01.niracler.com  -p 6379 -a 123456
$SET runoobkey redis  #OK
$redis 127.0.0.1:6379> GET runoobkey #"redis"
```

mongodb [客户端下载](https://robomongo.org/download)(测试文件在test中)

## 启动Web UI

```
scrapydweb
```

效果
http://plrom.niracler.com:5000/1/jobs/

## 假如使用自制镜像，需要以下操作

### 添加hosts

```bash
$echo "172.28.7.40 inner.registry" >> /etc/hosts
```

```bash
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
  "https://kfwkfulq.mirror.aliyuncs.com",
  "https://2lqq34jg.mirror.aliyuncs.com",
  "https://pee6w651.mirror.aliyuncs.com"
  ],
  "insecure-registries" : ["127.0.0.0/8","192.168.0.0/16","172.16.0.0/12","10.0.0.0/8"]
}
EOF
```

```bash
systemctl restart docker
```

## 参考文章

- [使用 Docker Swarm 搭建分布式爬虫集群](https://www.kingname.info/2018/10/13/use-docker-swarm/)
- [分布式网络数据抓取系统设计与实现](https://www.jianshu.com/p/fb028ad74798)
- [分布式爬虫的部署之Scrapyd分布式部署](https://juejin.im/post/5b0e1a8ff265da092100709f)
- [scrapy-redis](https://github.com/rmax/scrapy-redis)
- [小白进阶之Scrapy第三篇（基于Scrapy-Redis的分布式以及cookies池）](https://cuiqingcai.com/4048.html)
- [如何简单高效地部署和监控分布式爬虫项目](https://juejin.im/post/5bebc5fd6fb9a04a053f3a0e)
- [news-please](https://github.com/fhamborg/news-please)
- [who did what, when, where, why, and how?](https://github.com/fhamborg/Giveme5W1H)
- [台湾新闻爬虫](https://github.com/TaiwanStat/Taiwan-news-crawlers)
- [基于给定事件关键词，采集事件资讯，对事件进行挖掘和分析。](https://github.com/liuhuanyong/EventMonitor)
- [An array field in scrapy.Item](https://stackoverflow.com/questions/29227119/an-array-field-in-scrapy-item)
- [Scrapy 使用写死的cookie 来爬需要登录的页面](https://blog.csdn.net/fox64194167/article/details/79775301)
- [新浪微博爬虫，用python爬取新浪微博数据](https://github.com/dataabc/weiboSpider)
- [scrapy爬取新浪微博+cookie池](https://blog.csdn.net/m0_37438418/article/details/80819847)
- [Scrapyd手册](https://scrapyd.readthedocs.io/en/stable/install.html)
- [Scrapyd configuration when installing from pip or Github](https://github.com/scrapy/scrapyd/issues/104)