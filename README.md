# crawler
> 毕业设计的爬虫模块

23-

### 使用虚拟环境

```bash
source venv/bin/activate
```

### 安装依赖包

```sh
pip install --upgrade pip

pip install -r requirements.txt
```

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

### 对 docker 节点打标签

```bash
$docker node update --label-add spider-role=crawler node1
```

### 构建网络

```bash
$make network
```

### 构建 nginx 反向代理

```bash
$make crawler-nginx
```

### 启动

```bash
$make crawler
```

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

## 待爬取网站

[新浪](https://www.sina.com.cn/)
[凤凰网](https://www.ifeng.com/)
[搜狐](http://news.sohu.com/)
[readhub](https://readhub.cn/topics)

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