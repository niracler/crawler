FROM python:3.6

USER root
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

COPY . ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["scrapy"]
#CMD ["crawl", "shenshe_redis"]