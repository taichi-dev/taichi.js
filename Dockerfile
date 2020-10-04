FROM python:3.8

WORKDIR /app

ADD dockeroot /app

RUN cat /etc/apt/sources.list

#RUN cp sources.list /etc/apt/

RUN apt-get update

RUN apt-get install libtinfo5

#RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt
