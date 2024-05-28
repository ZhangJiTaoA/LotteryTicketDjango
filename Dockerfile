FROM python:3.10.8

WORKDIR /usr/src/app

# 使用 HTTPS 协议访问容器云调用证书安装
RUN apt install ca-certificates -y

COPY . .

RUN mkdir ~/.pip && touch ~/.pip/pip.conf && \
    echo "[global]" >> ~/.pip/pip.conf && \
    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt &&\
    python manage.py migrate

ENV PYTHONPATH=/usr/src/app

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
