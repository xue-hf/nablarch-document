FROM docker.1ms.run/library/python:3.8.18-slim

WORKDIR /root

COPY requirements.txt /root/
COPY package*.json /root/
COPY patches /root/patches/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Sphinxのセットアップ
RUN pip install --no-cache-dir -r requirements.txt

RUN sed -i 's/http:\/\/deb.debian.org/https:\/\/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

## textlintのセットアップ
#RUN apt-get update
#
#RUN apt-get install -y curl \
#    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
#    && apt-get install -y nodejs npm --no-install-recommends \
#    && apt-get clean
#
#RUN npm config set registry https://registry.npmmirror.com/
#
#RUN npm install --registry https://registry.npmmirror.com/ && npm audit fix
