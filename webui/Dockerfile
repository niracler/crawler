FROM python:3.6

USER root
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir /projects
COPY webui/scrapydweb_settings_v9.py scrapydweb_settings_v9.py

EXPOSE 5000

CMD ["scrapydweb"]