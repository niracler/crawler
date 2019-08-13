# crawler
> 毕业设计的爬虫模块, 琉璃神社爬虫， 新浪微博爬虫, 等后续是面向于游戏方面的资讯

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

### 新闻对象  

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

 - [x] 17173 https://www.17173.com/
 - [x] 巴哈姆特電玩資訊站 https://www.gamer.com.tw/
 - [ ] 3dmgame https://www.3dmgame.com/news/
 - [ ] 电玩巴士 https://www.tgbus.com/
 - [ ] 游侠网 https://www.ali213.net/
 - [ ] 游民星空 https://www.gamersky.com/news/
 - [ ] 机核网 https://www.gcores.com/news
 - [ ] 漫资讯 https://www.dongmanzx.com/
 - [ ] acg批评 http://www.acgpiping.net/
 - [ ] 半次元 https://bcy.net/
 - [ ] 果壳网 https://www.guokr.com/scientific/
 - [ ] 178网游 http://www.178.com/

### 打包命令
```bash
$ cd ..
$ tar -czvf crawler.tar.gz  --exclude=crawler/venv crawler
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