FROM python:3.10.8

WORKDIR /usr/src/app
COPY ../../../Desktop/fsdownload .

RUN mkdir ~/.pip && touch ~/.pip/pip.conf && \
    echo "[global]" >> ~/.pip/pip.conf && \
    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/src/app

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
