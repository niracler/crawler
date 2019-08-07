FROM python:3.6

USER root
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

RUN pip3 install scrapyd

COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY scrapyd/scrapyd.conf /etc/scrapyd/
RUN mkdir /root/logs
RUN mkdir /root/items
COPY scrapyd/run.sh /run.sh
RUN chmod 777 /run.sh
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
EXPOSE 6800

CMD ["/run.sh"]